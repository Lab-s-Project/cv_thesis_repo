#==============================#
# Author: KONG Vungsovanreach  #
# Date: 2024-04-25             #
#==============================#

#import all required modules
from .xutils import Config

DL_MODEL_ROOT='./assets/models'
PRED_SAVE_DIR='./assets/videos/predictions'

#yolo classes for detection
DETECT_YOLO_CLASS=[0, 1] #person and car

#constant value for plotting
color = Config()
color.GREENISH=(0, 181, 6)
color.RED=(0, 0, 255)
color.WHITE=(255, 255, 255)

#gpio & light tower color
danger_pin_num = {
    1: 18,
    2: 5,
    3: 12
}

pin_num_color = {
    danger_pin_num[1]: 'green',
    danger_pin_num[2]: 'yellow',
    danger_pin_num[3]: 'red'
}

#plotting configuratiion
plot_config = Config()
plot_config.bounding_box=False
plot_config.class_label=True
plot_config.distance_line=True
plot_config.bottom_point=True
plot_config.danger_level=True
plot_config.bottom_ellipse=True

DEVELOPMENT=False