#==============================#
# Author: KONG Vungsovanreach  #
# Date: 2024-04-25             #
#==============================#

#import all required modules
from ultralytics import YOLO
import sys, cv2, os, uuid
from datetime import datetime
import numpy as np
sys.path.append('..')
from modules.xenum import ModelType, StreamType
from modules import xconst
from modules.xutils import xmsg, xerr, add_polygon

#class handler for deep learning model operation
class DLModel():
    def __init__(self, model_type = ModelType.yolov8n, stream = None, config=None):
        self.model_type = model_type
        self.stream = stream
        self.config = config
        self.model = None
        self.frames = []
        self.risk_areas = None

    #load yolo model for detection
    def load_model(self):
        self.model = YOLO(f'{xconst.DL_MODEL_ROOT}/{self.model_type.value}.pt')
        return self.model

    #add polygon to the prediction
    def set_risk_area(self, coords):
        self.risk_areas = coords

    #predict the list of frames extracted from video file
    def detect(self, extract=True, save_file = False, filename=None):
        #laod model if it is not loaded yet
        if not self.model: self.load_model()
        
        #extract the frames before prediction instread of realtime prediction
        if (self.stream.stream_type is StreamType.file) and extract:
            frames = self.stream.extract_frames()
            for i in frames:
                res = self.model(i, verbose=False, classes=xconst.DETECT_YOLO_CLASS)
                pred = res[0].plot()
                self.frames.append(pred)
                pred = cv2.resize(pred, self.config.show_windows_size)
                if self.risk_areas: pred = add_polygon(pred, self.risk_areas)
                cv2.imshow('Prediction - Frame extracted', pred)
                key = cv2.waitKey(1)
                if key == ord('q'):
                    break
        else:
            cap = self.stream.get_cap()
            while cap.isOpened():
                success, frame = cap.read()
                if not success:
                    xerr('cannot read frame or video reach the end.')
                    break
                res = self.model(frame, verbose=False, classes=[0, 2])
                pred = res[0].plot()
                self.frames.append(pred)
                pred = cv2.resize(pred, self.config.show_windows_size)
                if self.risk_areas: pred = add_polygon(pred, self.risk_areas)
                cv2.imshow('Prediction - Realtime', pred)
                key = cv2.waitKey(1)
                if key == ord('q'):
                    break
            cap.release()
        cv2.destroyAllWindows()

        #save prediction into mp4 file
        if save_file:
            if not filename:
                unique_id = str(uuid.uuid4())
                timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
                filename = f"{unique_id[:5]}_{timestamp}.mp4"
            self.save_prediction(filename)

    #save the prediction result into mp4 file
    def save_prediction(self, filename):
        #validate the stream type
        if self.stream.stream_type is not StreamType.file:
            xerr('only stream_type=file can be saved as a file.')
            return 0 
        xmsg(f'wait - start saving prediction into file: "{filename}"')
        num_frames, height, width, _ = np.array(self.frames).shape
        codec_id = "mp4v" # ID for a video codec.
        fourcc = cv2.VideoWriter_fourcc(*codec_id)
        out = cv2.VideoWriter(os.path.join(xconst.PRED_SAVE_DIR, filename), fourcc=fourcc, fps=30, frameSize=(width, height))

        #write frames into file one by one
        for i in range(num_frames):
            out.write(np.array(self.frames)[i, :, :, :])
        out.release()
        xmsg(f'file successfully saved as: "{filename}"')