import cv2
import numpy as np
from PIL import Image
import os
import time
from darknet import load_net,load_meta,detect

def logging_time(original_fn):
    def wrapper_fn(*args, **kwargs):
        start_time = time.time()
        result = original_fn(*args, **kwargs)
        end_time = time.time()
        print("WorkingTime[{}]: {} sec".format(original_fn.__name__, end_time-start_time))
        return result
    return wrapper_fn

class Net():
    
    @logging_time
    def __init__(self, cfg_path, weight_path, data_path):
        self.net = load_net(cfg_path.encode(), weight_path.encode(), 0)
        self.meta = load_meta(data_path.encode())
        
#     @logging_time
    def detectSwoon(self, frame):

        global duration

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
            return None
        else :
            duration = duration+1
            return list(detection_result)[0]

    
# @logging_time
def drawBoudingBox(points, frame):
    
    start_point = (int(points[0]), int(points[1]))
    end_point = (int(points[0] + points[2]), int(points[1] + points[3]))
    
    return cv2.rectangle(frame, start_point, end_point, (0,0,255), 3)
    

if __name__=='__main__':
    
    duration = 0

    cfg_path = "/root/cfg/obj.cfg"
    weight_path = "/root/4th/obj_120000.weights"
    data_path = "/root/cfg/obj.data"    

    net = Net(cfg_path, weight_path, data_path)
    
    title = '''\033[36m
      ____                        _       _           
     / ___|  __ ___   _____      | | ___ | |__  _ __  
     \___ \ / _` \ \ / / _ \  _  | |/ _ \| '_ \| '_ \ 
      ___) | (_| |\ V /  __/ | |_| | (_) | | | | | | |
     |____/ \__,_| \_/ \___|  \___/ \___/|_| |_|_| |_|\033[0m

                 Duksung Women's University
        College of Engineering - IT Media Engineering
        
                 \033[1m8th Graduation Exhibition\033[0m
                  2020.10.26 - 2020.10.28
                 
           \033[1mYeeun Lee\033[0m   ye97527@gmail.com
           \033[1mInseo Song\033[0m  songinseo0910@gmail.com
    '''
    os.system('clear')
    print(title)
    
    video = '/root/test.mp4'

    cap = cv2.VideoCapture(video)
    
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_number = 0
    step = 1
    
    while(cap.isOpened()):
        
        if duration > 5/step: #5 sec
            
            print(f'[{time.ctime()}] \033[31mClass [Swoon] has detected.\033[0m')
            duration = 0
        
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
        ret, frame = cap.read()
    
        if ret:
            frame_number = frame_number + (int(fps)*step)
            
            img = cv2.resize(frame, (960,540))
            result = net.detectSwoon(img)
            
            if result != None:
                img = drawBoudingBox(result[2], img)
            
            cv2.imshow('video', img)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        else:
            frame_number = 0
            break

    cap.release()
    cv2.destroyAllWindows()