from threading import Thread
import cv2
import time

class videocapture:

    def __init__(self,src=0):


        self.video = cv2.VideoCapture(src)
        self.video.set(cv2.CAP_PROP_BUFFERSIZE, 2)
        self.ret = True
        self.frame = None
        self.stop = False
        
        self.frame_rate = 1./30
        self.start_time = time.time()

        self.prev_frame_time = 0
        self.new_frame_time = 0
        self.showFps = True

    def start(self):
        Thread(target=self.get,args=()).start()
        return self

    def get(self):

        while not self.stop:
            if not self.ret:
                self.stop_video()

            else:                    
                self.ret,self.frame = self.video.read()
                
                self.new_frame_time =time.time()
                fps = 1/(self.new_frame_time-self.prev_frame_time)
                self.prev_frame_time = self.new_frame_time
                fps = int(fps)
                fps = str(fps)
                if self.showFps:
                    self.frame = cv2.putText(self.frame, fps, (10, 25),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                time.sleep(self.frame_rate)
                

    def stop_video(self):
        self.stop = True
    
    def get_stop(self):
        return self.stop