# import argparse
# import time
# from pathlib import Path

# import torch
# from options.train_options import TrainOptions
# from loaders import aligned_data_loader
# from models import pix2pix_model

# import cv2
# import torch.backends.cudnn as cudnn
# from numpy import random

# from models.experimental import attempt_load
# from utils.datasets import LoadStreams, LoadImages
# from utils.general import check_img_size, check_requirements, check_imshow, non_max_suppression, apply_classifier, \
#     scale_coords, xyxy2xywh, strip_optimizer, set_logging, increment_path, save_one_box
# from utils.plots import colors, plot_one_box
# from utils.torch_utils import select_device, load_classifier, time_synchronized

import dtodepth
import detect
from IPython.display import Image, clear_output  # to display images

def main():
	imgProf=dtodepth.profundidad()
  Image(imgProf, width=60)

if __name__ == '__main__':
    main()