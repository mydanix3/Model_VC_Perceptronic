# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import argparse
import os
from util import util
from argparse import Namespace

class BaseOptions():
    def __init__(self):
        self.parser = argparse.ArgumentParser()
        self.initialized = False

    def initialize(self):
      self.initialized = True

    def parse(self):
        if not self.initialized:
            self.initialize()
        
        self.opt = Namespace(batchSize=8, beta1=0.5, checkpoints_dir='./checkpoints/', continue_train=False, display_freq=100, display_id=1, display_winsize=256, fineSize=256, gpu_ids='0,1,2,3', human_data_term=0, identity=0.0, input='single_view', lambda_A=10.0, lambda_B=10.0, loadSize=286, lr=0.0004, lr_decay_epoch=8, lr_policy='step', max_dataset_size='inf', mode='Ours_Bilinear', model='pix2pix', nThreads=2, name='test_local', ndf=64, ngf=64, niter=100, niter_decay=100, no_flip=False, no_html=False, no_lsgan=False, norm='instance', output_nc=3, phase='train', pool_size=50, print_freq=100, save_epoch_freq=5, save_latest_freq=5000, serial_batches=False, simple_keypoints=0, use_dropout=False, which_epoch='latest', which_model_netG='unet_256')
        self.opt.isTrain = self.isTrain  # train or test
        str_ids = self.opt.gpu_ids.split(',')
        self.opt.gpu_ids = []
        for str_id in str_ids:
            id = int(str_id)
            if id >= 0:
                self.opt.gpu_ids.append(id)

        args = vars(self.opt)

        print('------------ Options -------------')
        for k, v in sorted(args.items()):
            print('%s: %s' % (str(k), str(v)))
        print('-------------- End ----------------')

        # save to the disk
        expr_dir = os.path.join(self.opt.checkpoints_dir, self.opt.name)
        util.mkdirs(expr_dir)
        file_name = os.path.join(expr_dir, 'opt.txt')
        with open(file_name, 'wt') as opt_file:
            opt_file.write('------------ Options -------------\n')
            for k, v in sorted(args.items()):
                opt_file.write('%s: %s\n' % (str(k), str(v)))
            opt_file.write('-------------- End ----------------\n')
        return self.opt
