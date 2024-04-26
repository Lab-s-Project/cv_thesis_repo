#==============================#
# Author: KONG Vungsovanreach  #
# Date: 2024-04-25             #
#==============================#

#import all required modules
from modules.xstream import Stream
from modules.xenum import StreamType
from detection.core import DLModel
import cv2

#strating point of the detection
if __name__ == '__main__':
    stream = Stream(stream_type = StreamType.file)
    stream.set_file_location('./assets/videos/vid001.mp4')
    # stream.display()
    frames = stream.extract_frames()
    dlmodel = DLModel()
    # model = dlmodel.load_model()

    dlmodel.pred_frame_list(frames)
    dlmodel.save_prediction('vid01.mp4')