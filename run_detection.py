#==============================#
# Author: KONG Vungsovanreach  #
# Date: 2024-04-25             #
#==============================#

#import all required modules
from modules.xstream import Stream
from modules.xenum import StreamType, ModelType, PolygonType
from modules.xutils import Config, add_polygon
from modules.xpolygon import XPolygon
from detection.core import DLModel
import cv2

#strating point of the detection
if __name__ == '__main__':
    # #global vars
    config = Config()
    config.cam_windows_size = (1080, 720)
    config.show_windows_size = (1080, 720)

    # #define stream object
    stream = Stream(stream_type = StreamType.file)
    stream.set_file_location('./assets/videos/vid001.mp4')
    cap = stream.get_cap()

    polygon = XPolygon(cap=cap, 
                       polygon_type=PolygonType.line, 
                       show_windows_size=config.show_windows_size)
    polygons_list = polygon.draw()

    # while cap.isOpened():
    #     success, frame = cap.read()
    #     if not success:
    #         break
    #     frame = cv2.resize(frame, config.show_windows_size)
    #     frame = add_polygon(frame, polygons_list)
    #     cv2.imshow('Prediction - Realtime', frame)

    #     key = cv2.waitKey(1)
    #     if key == ord('q'):
    #         break
    # cap.release()
    # cv2.destroyAllWindows()

    #start prediction
    dlmodel = DLModel(model_type = ModelType.yolov8n, stream=stream, config=config)
    dlmodel.set_risk_area(polygons_list)
    dlmodel.detect(extract=True)
    
    


    