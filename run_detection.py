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
    #global vars
    config = Config()
    config.cam_windows_size = (1280, 720)
    config.show_windows_size = (1280, 720)

    # #define stream object
    stream = Stream(stream_type = StreamType.file, config = config)
    stream.set_file_location('./assets/videos/vid001.mp4')
    cap = stream.get_cap()

    # polygon = XPolygon(cap=cap, 
    #                    polygon_type=PolygonType.line, 
    #                    show_windows_size=config.show_windows_size)
    # polygons_list = polygon.draw()
    # print(polygons_list)
    polygons_list=[[(928, 218), (737, 190), (435, 155), (195, 143), (30, 315), (373, 350), (740, 396), (903, 427), (929, 219)]]
    
    #start prediction
    dlmodel = DLModel(model_type=ModelType.yolov8l, 
                      stream=stream, 
                      config=config)
    dlmodel.set_risk_area(polygons_list)
    dlmodel.detect(extract=True, save_file=True)