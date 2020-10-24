import numpy as np
from PIL import Image
import os
from loadDarknet import load_net,load_meta,detect

class Net():
    
    def __init__(self, cfg_path, weight_path, data_path):
        self.net = load_net(cfg_path.encode(), weight_path.encode(), 0)
        self.meta = load_meta(data_path.encode())
        
    def detectSwoon(self, frame, duration):

        tmp = Image.fromarray(frame[:,:,::-1], 'RGB')
        tmp_file_path = os.getenv("HOME")+'/.saveJohn_tmp/tmp.jpg'

        tmp.save(tmp_file_path)
        
        detection_result = detect(self.net, self.meta, tmp_file_path.encode())
        
            # detection_result[0] = class
            # detection_result[1] = probability
            # detection_reuslt[2] = (b.x, b.y, b.w, b.h)
        
        os.remove(tmp_file_path)
        
        if len(detection_result)==0 or detection_result[0][1]< 0.8 :
            duration = 0
            return None, duration
        else :
            duration = duration+1
            return list(detection_result)[0], duration