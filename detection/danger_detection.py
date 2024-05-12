#==============================#
# Author: KONG Vungsovanreach  #
# Date: 2024-04-25             #
#==============================#

#import all required modules
from shapely.geometry import Polygon, Point
import copy

#base class for danger detection
class DangerDetection(object):
    def __init__(self, risk_areas):
        self.risk_areas = Polygon(risk_areas[0])
        print(self.risk_areas)
    
    def detect(self, result):
        new_boxes = []
        for idx, box in enumerate(result.xboxes):
            xc, yc = result.xcyc[idx]
            new_box = copy.deepcopy(box)
            if Point((xc, yc)).within(self.risk_areas):
                print('jol hai jol hai')
                new_box.danger = True
            new_boxes.append(new_box)
        result.xboxes = new_boxes
        for idx, box in enumerate(result.xboxes):
            if box.danger:
                print(box.danger)
        
        return result
