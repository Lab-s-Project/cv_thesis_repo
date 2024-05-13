#==============================#
# Author: KONG Vungsovanreach  #
# Date: 2024-04-25             #
#==============================#

#import all required modules
from shapely.geometry import Polygon, Point
import sys, math, cv2
#change dir to import modules
sys.path.append('..')
from modules.xutils import xmsg, xerr
from modules.xcustom_class import MSL

#base class for danger detection
class DangerDetection(object):
    def __init__(self, risk_areas):
        self.risk_areas = Polygon(risk_areas[0])
        self.track_hist = MSL(max_size=5)
        self.in_polygon_cls = MSL(max_size=50) #list of all object that locates in the polygon
        xmsg(f'polygon: {self.risk_areas}')

    
    def detect(self, result):
        self.result = result
        self.track_hist.push(self.result)
        person_objects, car_objects = [], []
        for idx, (cl, xbox) in enumerate(zip(self.result.cls, self.result.xboxes)):
            leg_xc, leg_yc = self.result.leg_xcyc[idx]
            
            #if it is a person and step into the polygon
            if Point((leg_xc, leg_yc)).within(self.risk_areas):
                self.in_polygon_cls.push(int(cl))
                if int(cl) == 0:
                    person_objects.append(idx)
                    self.result.xboxes[idx].is_danger = True
                    self.result.danger_level.append(1)
                elif int(cl)== 2:
                    car_objects.append(idx)
        #when there are both person and car in the risk area
        if len(list(set(self.in_polygon_cls.get_list()))) == 2: self.result.danger_level.append(2)

        #check distance between each person and each object in the risk area
        if len(person_objects) > 0:
            for person_idx in person_objects:
                leg_xc, leg_yc = self.result.leg_xcyc[person_idx]
                _, _, person_width, _ = self.result.xywh[person_idx]
                self.result.distance_line_data.persons.append((leg_xc, leg_yc))
                for car_idx in car_objects:
                    wheel_xc, wheel_yc = self.result.leg_xcyc[car_idx]
                    self.result.distance_line_data.cars.append((wheel_xc, wheel_yc))

                    #calculate between each person and each car
                    dx = leg_xc - wheel_xc
                    dy = leg_yc - wheel_yc

                    # Apply the Euclidean distance formula
                    distance = math.sqrt(dx**2 + dy**2)
                    if distance < (person_width * 4):
                        self.result.danger_level.append(3)
                        # print(f'{person_width} | {distance}')



        self.in_polygon_cls.empty()
        return self.result