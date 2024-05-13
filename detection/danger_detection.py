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
        self.result = result
        for idx, xbox in enumerate(self.result.xboxes):
            leg_xc, leg_yc = self.result.leg_xcyc[idx]
            if Point((leg_xc, leg_yc)).within(self.risk_areas):
                self.result.xboxes[idx].is_danger = True
        return result
