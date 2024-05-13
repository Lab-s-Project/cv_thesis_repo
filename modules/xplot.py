#==============================#
# Author: KONG Vungsovanreach  #
# Date: 2024-04-25             #
#==============================#

#import all required modules
import cv2, time
from .xconst import color

#base class for plotting result
class XPlot(object):
    def __init__(self, result, config):
        self.result = result
        self.config = config
        self.bb_thickness = 1
        self.text_thickness = 2
        self.font = cv2.FONT_HERSHEY_SIMPLEX
        self.font_scale = 0.8
        
    @property
    def boxes(self): #return all predicted boxes
        return self.result.boxes

    @property
    def xboxes(self):
        return self.result.xboxes

    @property
    def img(self): #return original input image
        return self.result.img

    def plot(self):
        #iterate over all boxes and plot detail
        for idx, xbox in enumerate(self.xboxes):
            x1, y1, x2, y2 = self.result.xyxy[idx]
            x, y, w, h = self.result.xyxy[idx]
            xc, yc = self.result.xcyc[idx]
            leg_xc, leg_yc = self.result.leg_xcyc[idx]
            class_id = self.result.cls[idx]
            class_name = self.result.names[class_id]
            class_color, class_bg_color, bb_color = color.WHITE, color.GREENISH, color.GREENISH
            cls_label_x1y1, cls_label_x2y2 = (xc-7, yc-15), (xc+37, yc+12)

            #start plot the bounding box and label
            if xbox.is_danger:
                class_bg_color = color.RED
                bb_color = color.RED

            #dynamic class label background width
            if class_id == 0: 
                cls_label_x1y1, cls_label_x2y2 = (xc-7, yc-15), (xc+82, yc+12)
                # cv2.rectangle(self.img, (x1, y2-20), (x2, y2), bb_color, thickness=self.bb_thickness, lineType=cv2.LINE_AA)
                if self.config.bottom_point: cv2.circle(self.img, (leg_xc, leg_yc), 3, class_bg_color, -1, cv2.LINE_AA)

                # cv2.circle(self.img, (leg_xc, leg_yc), 30, bb_color, 1, cv2.LINE_AA)
                if self.config.bottom_ellipse:
                    cv2.ellipse(self.img, (leg_xc, leg_yc), (20, 20), 0, 30, 150, bb_color, 2)
                    cv2.ellipse(self.img, (leg_xc, leg_yc), (15, 15), 0, 30, 150, bb_color, 2)
            
            elif class_id == 2:
                if self.config.bottom_point: cv2.circle(self.img, (leg_xc, leg_yc), 3, class_bg_color, -1, cv2.LINE_AA)
                pass

            #plot the line between person and car which locates in the risk area
            if self.config.distance_line:
                for person in self.result.distance_line_data.persons:
                    for car in self.result.distance_line_data.cars:
                        cv2.line(self.img, person, car, color.GREENISH, thickness=1, lineType=cv2.LINE_AA) 

            #plot the bounding box, label background, class label
            if self.config.bounding_box: cv2.rectangle(self.img, (x1, y1), (x2, y2), bb_color, thickness=self.bb_thickness, lineType=cv2.LINE_AA)
            if self.config.class_label:
                cv2.rectangle(self.img, cls_label_x1y1, cls_label_x2y2, class_bg_color, -1)
                cv2.putText(self.img, class_name, (xc-5, yc+5), self.font, self.font_scale, color.WHITE, self.text_thickness)
            if self.config.danger_level:
                cv2.rectangle(self.img, (0, 0), (220, 35), color.GREENISH, -1)
                cv2.putText(self.img, f'Danger Level: {max(self.result.danger_level)}', (10, 25), self.font, self.font_scale, color.WHITE, 2)

        time.sleep(0.03)
        return self.img