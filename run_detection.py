#==============================#
# Author: KONG Vungsovanreach  #
# Date: 2024-04-25             #
#==============================#

#import all required modules
from modules.xstream import Stream
from modules.xenum import StreamType, ModelType
from detection.core import DLModel
import cv2

#strating point of the detection
if __name__ == '__main__':
    #define stream object
    stream = Stream(stream_type = StreamType.file)
    stream.set_file_location('./assets/videos/vid001.mp4')

    #start prediction
    dlmodel = DLModel(model_type = ModelType.yolov8n, stream=stream)
    dlmodel.detect(extract=False, save_file=True)