from threading import Thread
import cv2
import time
from datetime import datetime

class videocapture:

    def __init__(self, src=0):
        self.video = cv2.VideoCapture(src)
        self.video.set(cv2.CAP_PROP_BUFFERSIZE, 2)
        self.ret, self.frame = self.video.read()
        self.stop = False
        self.frame_rate = 1./24
        self.start_time = time.time()
        self.prev_frame_time = 0
        self.new_frame_time = 0
        self.showFps = False
        self.record = False
        self.fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        self.out = None

    def start(self):
        Thread(target=self.get, args=()).start()
        return self

    def get(self):
        while not self.stop:
            if not self.ret:
                self.stop_video()
            else:
                self.ret, self.frame = self.video.read()
                self.new_frame_time = time.time()
                fps = 1/(self.new_frame_time - self.prev_frame_time)
                self.prev_frame_time = self.new_frame_time
                fps = int(fps)
                fps = str(fps)
                if self.record:
                    self.out.write(cv2.flip(self.frame, 1))
                if self.showFps:
                    cv2.putText(self.frame, fps, (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                elapsed_time = time.time() - self.new_frame_time 
                delay = max(self.frame_rate - elapsed_time, 0)
                time.sleep(delay)

    def generate_filename(self):
        return './videos/' + datetime.now().strftime("%m%d%H%M%S") + '.mp4'

    def start_recording(self):
        self.out = cv2.VideoWriter(self.generate_filename(), self.fourcc, 24.0, (640, 480))
        self.record = True
    
    def stop_recording(self):
        self.record = False
        if self.out is not None:
            self.out.release()
            self.out = None

    def stop_video(self):
        self.stop = True
        if self.out is not None:
            self.out.release()
        if self.video is not None:
            self.video.release()
