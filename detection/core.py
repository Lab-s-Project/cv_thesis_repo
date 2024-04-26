#==============================#
# Author: KONG Vungsovanreach  #
# Date: 2024-04-25             #
#==============================#

#import all required modules
from ultralytics import YOLO
import sys, cv2, os
import numpy as np
sys.path.append('..')
from modules.xenum import ModelType
from modules import xconst

class DLModel():
    def __init__(self, model_type = ModelType.yolov8n):
        self.model_type = model_type
        self.model = None
        self.frames = []

    def load_model(self):
        self.model = YOLO(f'{xconst.DL_MODEL_ROOT}/{self.model_type.value}.pt')
        return self.model

    def pred_frame_list(self, frames):
        if not self.model: self.load_model()
        for i in frames:
            res = self.model(i, verbose=False, classes=[0, 2])
            pred = res[0].plot()
            self.frames.append(pred)
            cv2.imshow('Prediction', pred)

            key = cv2.waitKey(1)
            if key == ord('q'):
                break
        cv2.destroyAllWindows()

    def save_prediction(self, filename):
        num_frames, height, width, _ = np.array(self.frames).shape
        codec_id = "mp4v" # ID for a video codec.
        fourcc = cv2.VideoWriter_fourcc(*codec_id)
        out = cv2.VideoWriter(os.path.join(xconst.PRED_SAVE_DIR, filename), fourcc=fourcc, fps=30, frameSize=(width, height))

        for i in range(num_frames):
            out.write(np.array(self.frames)[i, :, :, :])
        out.release()