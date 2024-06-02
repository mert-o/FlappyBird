import os
import time

from threading import Thread
from datetime import datetime
import pygame
import cv2
import numpy as np


class ScreenRecorder:
    
    def __init__(self,screen):

        self.screen = screen
        self.stop = False
        self.new_frame_time = 0
        self.frame_rate = 1./24
        self.writer = None
        self.fourcc = cv2.VideoWriter_fourcc(*'mp4v')

    def start_recording(self):
        self.stop = False
        self.writer = cv2.VideoWriter(self.generate_filename(), self.fourcc, 24.0, (640, 480))
        Thread(target=self.get, args=()).start()
        return self

    def get(self):
        
        while not self.stop:
            buffer_str = pygame.image.tostring(self.screen, 'RGB')
            self.new_frame_time = time.time()
            img = np.fromstring(buffer_str, dtype=np.uint8)
            img = img.reshape((self.screen.get_height(), self.screen.get_width(), 3))
            img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
            resized_img = cv2.resize(img, (640, 480))
            self.writer.write(resized_img)
            elapsed_time = time.time() - self.new_frame_time 
            delay = max(self.frame_rate - elapsed_time, 0)
            time.sleep(delay)
        


    def stop_recording(self):
        if self.writer is not None:
            self.writer.release()
            self.writer = None
        self.stop = True
        
    def generate_filename(self):
        return './videos/'+ datetime.now().strftime("%m%d%H%M%S")+'_gameplay.mp4'
        





