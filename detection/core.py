#==============================#
# Author: KONG Vungsovanreach  #
# Date: 2024-04-25             #
#==============================#

#import all required modules
import numpy as np
import RPi.GPIO as GPIO
from .xresult import XResult
from ultralytics import YOLO
from datetime import datetime
import sys, cv2, os, uuid, time, pickle
from .danger_detection import DangerDetection

#change dir to import modules
sys.path.append('..')
from modules import xconst
from modules.xplot import XPlot
from modules.xgpio import XGPIO
from modules.xenum import ModelType, StreamType
from modules.xutils import xmsg, xerr, add_polygon

#class handler for deep learning model operation
class DLModel():
    def __init__(self, model_type = ModelType.yolov8n, stream = None, config=None):
        self.model_type = model_type
        self.stream = stream
        self.config = config
        self.model = None
        self.preds = []
        self.risk_areas = None
        self.current_danger = 0

    #load yolo model for detection
    def load_model(self):
        xmsg('loading yolo model from .pt file.')
        self.model = YOLO(f'{xconst.DL_MODEL_ROOT}/{self.model_type.value}.pt')
        xmsg('yolo model loaded successfully.')
        return self.model

    #add polygon to the prediction
    def set_risk_area(self, coords):
        self.risk_areas = coords
        self.dangerD = DangerDetection(self.risk_areas)

    #predict the list of frames extracted from video file
    def detect(self, extract=True, save_file = False, filename=None):
        #load model if it is not loaded yet
        if not self.model: self.load_model()
        xgpio = XGPIO(pins=[5, 12, 18])
        #extract the frames before prediction instread of realtime prediction
        if (self.stream.stream_type is StreamType.file) and extract:
            frames = self.stream.extract_frames()
            for idx, i in enumerate(frames):
                res = self.model(i, verbose=False, classes=xconst.DETECT_YOLO_CLASS, conf=0.7)
                # res = self.model.track(i, tracker='bytetrack.yaml', verbose=False, classes=xconst.DETECT_YOLO_CLASS, persist=True)
                res = self.dangerD.detect(result=XResult(res))
                max_danger_level = max(res.danger_level)
                if max_danger_level != self.current_danger:
                    xgpio.current_state = GPIO.LOW if max_danger_level > 0 else GPIO.HIGH
                    self.current_danger = max_danger_level
                pred = XPlot(result=res, config=xconst.plot_config).plot()
                pred = cv2.resize(pred, self.config.show_windows_size)
                polygon_color = (0, 0, 255) if max(res.danger_level) != 0 else (255, 0, 0)
                if self.risk_areas: pred = add_polygon(pred, self.risk_areas, color=polygon_color)
                self.preds.append(pred)
                cv2.imshow('Prediction - Frame extracted', pred)
                key = cv2.waitKey(1) & 0xFF
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
                res = self.dangerD.detect(result=XResult(res))
                max_danger_level = max(res.danger_level)
                if max_danger_level != self.current_danger:
                    xgpio.current_state = GPIO.LOW if max_danger_level > 0 else GPIO.HIGH
                    self.current_danger = max_danger_level
                pred = XPlot(result=res, config=xconst.plot_config).plot()
                pred = cv2.resize(pred, self.config.show_windows_size)
                polygon_color = (0, 0, 255) if max(res.danger_level) != 0 else (255, 0, 0)
                if self.risk_areas: pred = add_polygon(pred, self.risk_areas)
                self.preds.append(pred)
                cv2.imshow('Prediction - Realtime', pred)
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q'):
                    break
            cap.release()

        #clean the cv2 and gpio after prediction completed.
        cv2.destroyAllWindows()
        xgpio.release()

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

        #prepare videowriter object
        num_frames, height, width, _ = np.array(self.preds).shape
        codec_id = "mp4v" # ID for a video codec.
        fourcc = cv2.VideoWriter_fourcc(*codec_id)
        out = cv2.VideoWriter(os.path.join(xconst.PRED_SAVE_DIR, filename), fourcc=fourcc, fps=7, frameSize=(width, height))

        #write frames into file one by one
        start_time = time.time()
        for pred_frame in self.preds:
            out.write(pred_frame)
        out.release()

        #calculate saving time
        end_time = time.time()  # Record end time
        saving_time = end_time - start_time
        xmsg(f'file successfully saved as: "{filename}" | Saving time: {saving_time} seconds')