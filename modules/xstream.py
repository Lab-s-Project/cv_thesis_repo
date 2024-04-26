#==============================#
# Author: KONG Vungsovanreach  #
# Date: 2024-04-25             #
#==============================#

#import all required modules
from .xenum import StreamType
from .xutils import xmsg, xerr
from tqdm import tqdm
import cv2
import os

#class for managing stream
class Stream(object):
    def __init__(self, stream_type: StreamType):
        self.stream_type = stream_type
        self.file_location = None
        self.cap = None

    #set file for loading cap from (eg. video file)
    def set_file_location(self, loc):
        self.file_location = loc
    
    #get capture object
    def get_cap(self):
        return self.cap

    #load capture object using cv2
    def load_cap(self):
        #release cap if the app tries to reload the cap
        if self.cap: self.cap.release()
        if self.stream_type is StreamType.usb:
            self.cap = cv2.VideoCapture(0)
        elif self.stream_type is StreamType.file:
            if not self.file_location:
                xerr('please set file location before loading Cap.')
            else:
                self.cap = cv2.VideoCapture(self.file_location)
        xmsg('cap loading completed.')
        return self.cap
    
    #check and validate cap
    def validate_cap(self):
        self.load_cap()
        if not self.cap.isOpened():
            xerr('cap is not opened.')
            return False
        else:
            return True

    #display the captured frames
    def display(self, wh=(720, 480)):
        if not self.validate_cap(): return 0
        
        xmsg('start streaming video.')
        while self.cap.isOpened():
            success, frame = self.cap.read()

            if not success:
                xerr('cannot read frame or video reach the end.')
                return 0
            
            frame = cv2.resize(frame, wh)
            cv2.imshow('Video Streaming', frame)

            key = cv2.waitKey(1)
            if key == ord('q'):
                break

        self.cap.release()
        cv2.destroyAllWindows()

    #extract frame from video file
    def extract_frames(self):
        if self.stream_type is not StreamType.file:
            xerr('only stream_type=file can extract frame from file.')
            return None
        else:
            if not self.validate_cap(): return 0
            total_frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
            pbar = tqdm(total=total_frames, desc="Extracting frames", position=0, leave=True)
            extracted_frames = []
            cap = self.load_cap()
            xmsg(f'start extracting frames | total frames: {total_frames}')
            for frame_idx in range(total_frames):
                success, frame = cap.read()
                if not success: break
                extracted_frames.append(frame)
                pbar.update(1)
            return extracted_frames
        