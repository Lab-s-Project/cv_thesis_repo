#==============================#
# Author: KONG Vungsovanreach  #
# Date: 2024-04-25             #
#==============================#

#import all required modules
import cv2, time

#base class for plotting result
class XPlot(object):
    def __init__(self, result, bb_color = (0, 181, 6), bb_thickness=1):
        self.result = result
        # self.danger_detail = danger_detail
        self.bb_color = bb_color
        self.bb_thickness = bb_thickness
        self.text_color = (255, 255, 255)
        self.text_thickness = 1
        self.font = cv2.FONT_HERSHEY_SIMPLEX
        self.font_scale = 0.8
        self.center_color = (0, 0, 255)
        
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
            class_color, class_bg_color, bb_color = (255,255,255), (0, 181, 6), (0, 181, 6)
            cls_label_x1y1, cls_label_x2y2 = (xc-7, yc-15), (xc+37, yc+12)

            #start plot the bounding box and label
            if xbox.is_danger:
                class_bg_color = (0, 0, 255)
                bb_color = (0, 0, 255)

            #dynamic class label background width
            if class_id == 0: 
                cls_label_x1y1, cls_label_x2y2 = (xc-7, yc-15), (xc+82, yc+12)
                # cv2.rectangle(self.img, (x1, y2-20), (x2, y2), bb_color, thickness=self.bb_thickness, lineType=cv2.LINE_AA)
                cv2.circle(self.img, (leg_xc, leg_yc), 3, (255,0,0), -1, cv2.LINE_AA)

                cv2.circle(self.img, (leg_xc, leg_yc), 30, bb_color, 1, cv2.LINE_AA)
            
            elif class_id == 2:
                pass

            #plot the bounding box, label background, class label
            # cv2.rectangle(self.img, (x1, y1), (x2, y2), bb_color, thickness=self.bb_thickness, lineType=cv2.LINE_AA)
            cv2.rectangle(self.img, cls_label_x1y1, cls_label_x2y2, class_bg_color, -1)
            cv2.putText(self.img, class_name, (xc-5, yc+5), self.font, self.font_scale, self.text_color, self.text_thickness)

        time.sleep(0.03)
        return self.img