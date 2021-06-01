
import torch
from options.train_options import TrainOptions
from loaders import aligned_data_loader
from models import pix2pix_model
import sys
import cv2
BATCH_SIZE = 1
#sys.argv[0]='--input=single_view'
opt = TrainOptions().parse()  # set CUDA_VISIBLE_DEVICES before import torch

video_list = 'data/images/'
save_path = 'outfile'
eval_num_threads = 2
video_data_loader = aligned_data_loader.DAVISDataLoader(video_list, BATCH_SIZE)
video_dataset = video_data_loader.load_data()
# print('========================= Video dataset #images = %d =========' %
#       len(video_data_loader))

model = pix2pix_model.Pix2PixModel(opt)

torch.backends.cudnn.enabled = True
torch.backends.cudnn.benchmark = True
best_epoch = 0
global_step = 0

# print(
#     '=================================  BEGIN VALIDATION ====================================='
# )
#
# print('TESTING ON VIDEO')

model.switch_to_eval()

def profundidad():
  imatges = []
  for i, data in enumerate(video_dataset):
    print(i)
    stacked_img = data[0]
    targets = data[1]
    im = model.run_and_save_DAVIS(stacked_img, targets, save_path, video_list)

    # im = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)

    imatges.append(im)
  return imatges