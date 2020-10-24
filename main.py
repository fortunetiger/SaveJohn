import cv2
import os
import time
from detectSwoon import Net
import argparse

def logging_time(original_fn):
    def wrapper_fn(*args, **kwargs):
        start_time = time.time()
        result = original_fn(*args, **kwargs)
        end_time = time.time()
        print("WorkingTime[{}]: {} sec".format(original_fn.__name__, end_time-start_time))
        return result
    return wrapper_fn

def drawBoudingBox(points, frame):
    
    start_point = (int(points[0]), int(points[1]))
    end_point = (int(points[0] + points[2]), int(points[1] + points[3]))
    
    return cv2.rectangle(frame, start_point, end_point, (0,0,255), 3)
    

if __name__=='__main__':
    
    parser = argparse.ArgumentParser(description='Save John')
    
    parser.add_argument('--cfg', type=str, default='cfg/obj.cfg', help='path to cfg file')
    parser.add_argument('--data', type=str, default='cfg/obj.data', help='path to data file')
    parser.add_argument('--weight', type=str, default='weight/obj_final.weights', help='path to data file')
    parser.add_argument('--input', type=str, default='input/', help='path to input files(.mp4)')
    
    args = parser.parse_args()
    
    duration = 0

<<<<<<< HEAD
<<<<<<< HEAD
    net = Net(args.cfg, args.weight, args.data)
=======
=======
>>>>>>> 6b37b5732d48b9c5b7eeee19ec638906eb8015c0
    cfg_path = "cfg/obj.cfg"
    weight_path = "weight/obj_final.weights"
    data_path = "cfg/obj.data"    

    net = Net(cfg_path, weight_path, data_path)
>>>>>>> 6b37b5732d48b9c5b7eeee19ec638906eb8015c0
    
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
    
    for video in [f for f in os.listdir(args.input) if f.endswith('.mp4')] :
        print(f'[ file name ] {video}')
        
        cap = cv2.VideoCapture(args.input+video)

        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_number = 0
        step = 1

        while(cap.isOpened()):

            if duration > 5/step: #5 sec

                print(f'[ {time.ctime()} ] \033[31mClass [Swoon] has detected.\033[0m')
                duration = 0

            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
            ret, frame = cap.read()

            if ret:
                frame_number = frame_number + (int(fps)*step)

                img = cv2.resize(frame, (960,540))
                result, duration = net.detectSwoon(img, duration)

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