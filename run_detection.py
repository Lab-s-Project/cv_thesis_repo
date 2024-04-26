#==============================#
# Author: KONG Vungsovanreach  #
# Date: 2024-04-25             #
#==============================#

#import all required modules
from modules.xstream import Stream
from modules.xenum import StreamType

#strating point of the detection
if __name__ == '__main__':
    stream = Stream(stream_type = StreamType.file)
    stream.set_file_location('./assets/videos/vid001.mp4')
    # stream.display()
    print(stream.extract_frames())
    stream.display()