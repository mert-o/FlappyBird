import pygame
import glob
import random
import math
import time
import os

""" class Balloon:
    def __init__(self, word, color,sw,sh,w,h):
        self.word = word
        self.w = w
        self.h = h
        self.sw = sw
        self.sh = sh
        
        self.b_index = 0

        if color == 'b':
            self.balloons = [pygame.transform.scale(pygame.image.load(i),(w,h)) for i in sorted(glob.glob('./assets/balloons/blue*.png'))]
        elif color == 'r':
            self.balloons = [pygame.transform.scale(pygame.image.load(i),(w,h)) for i in sorted(glob.glob('./assets/balloons/red*.png'))]
        
        self.color = color

        font_size = 1
        font = pygame.font.Font('./assets/game_font.ttf', font_size)
        
        self.text = font.render(self.word, True, (0, 0, 0)) 

        while self.text.get_width()<w/2 - 2:
            font_size +=1
            font = pygame.font.Font('./assets/game_font.ttf', font_size) 
            self.text = font.render(self.word, True, (0, 0, 0))  



        self.rect = self.balloons[0].get_rect()
        self.rect.x = self.sw + w

        self.basey = random.randint(0, int(self.sh * 0.6))
        self.rect.y = self.basey
        self.freq = 0.005
        self.angle = 0
        self.hit = False
        self.anim_time = 0
    def update(self, delta, x_speed):
        self.angle += self.freq * delta
        
        self.rect.y += self.h * 0.04 * math.sin( self.angle)

        if self.rect.y > self.sh:
            self.rect.y = 0
            
        self.rect.x -= delta * x_speed

    def draw(self, screen):
        if not self.hit:
            screen.blit(self.balloons[0], (self.rect.x, self.rect.y))
            # Calculate the center of the balloon to position the text
            text_rect = self.text.get_rect(center=self.rect.center)
            screen.blit(self.text, text_rect)
        else:
            if not self.anim_time: 
                self.anim_time = time.time()
                self.b_index = 1
            
            
            if time.time()-self.anim_time>0.00001:
                self.anim_time = time.time()
                if self.b_index<len(self.balloons)-1 and self.b_index != -1:
                    self.b_index+=1
                else:
                    self.b_index = -1
            
            if self.b_index != -1:
                screen.blit(self.balloons[self.b_index],(self.rect.x, self.rect.y))

    def getx(self):
        return self.rect.x """

class Balloon:
    def __init__(self,color,sw,sh,w,h):
        
        self.w = w
        self.h = h
        self.sw = sw
        self.sh = sh
        
        self.b_index = 0
        
        
        self.color = color

        self.balloons = [pygame.transform.scale(pygame.image.load(i),(w,h)) for i in sorted(glob.glob(f'./assets/balloons2/{color}/*.png'))]
        
 
        self.rect = self.balloons[0].get_rect()
        self.rect.x = self.sw + w

        self.basey = random.randint(0, int(self.sh * 0.6))
        self.rect.y = self.basey
        self.freq = 0.005
        self.angle = 0
        self.hit = False
        self.anim_time = 0

    def update(self, delta, x_speed):
        if not self.hit:
            self.angle += self.freq * delta
            
            self.rect.y += self.h * 0.04 * math.sin( self.angle)

            if self.rect.y > self.sh:
                self.rect.y = 0
                
            self.rect.x -= delta * x_speed

    def draw(self, screen):
        if not self.hit:
            screen.blit(self.balloons[0], (self.rect.x, self.rect.y))
        else:
            if not self.anim_time: 
                self.anim_time = time.time()
                self.b_index = 1
            if time.time()-self.anim_time>0.00001:
                self.anim_time = time.time()
                if self.b_index<len(self.balloons)-1 and self.b_index != -1:
                    self.b_index+=1
                else:
                    self.b_index = -1
            
            if self.b_index != -1:
                screen.blit(self.balloons[self.b_index],(self.rect.x, self.rect.y))

    def getx(self):
        return self.rect.x


class WaterBall:
    def __init__(self, x, y, w,h, speed):
        self.image = pygame.image.load('./assets/sprites/bullet.png').convert_alpha()
        self.image = pygame.transform.scale(self.image,(w,h))
        #self.image = pygame.transform.flip(self.image,True,False)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = speed
        self.hit = False
        
    def update(self,dt):
        # Move the water ball upwards
        self.rect.x += self.speed * dt

    def draw(self, screen):
        if not self.hit:
            screen.blit(self.image, self.rect)

    def hits(self, balloon):
        return self.rect.colliderect(balloon.rect)
        
    def getx(self):
        return self.rect.x
    
    
    
    
class Banners:
    def __init__(self,path,sw,sh,w,h,good=False):
        self.w = w
        self.h = h
        self.sw = sw
        self.sh = sh

        
        self.banners = [pygame.transform.scale(pygame.image.load(i),(w,h)) for i in sorted(glob.glob(os.path.join(path,'*.png')))]

        if good:
            self.ops = [pygame.image.load(i) for i in sorted(glob.glob('./assets/ops/*.png'),key=self.sort_nums)]
            
        self.good = good
        self.path, self.name = os.path.split(path)

        self.banner = self.banners[0]
        

        self.rect = self.banner.get_rect()
        self.rect.x = self.sw + w

        self.basey = random.randint(0, int(self.sh * 0.6))
        self.rect.y = self.basey
        self.freq = 0.001
        self.angle = 0
        self.hit = False
        self.anim_time = 0
        self.grow = True
        self.finish = False
        self.center_x = self.rect.x + self.w / 2
        self.center_y = self.rect.y + self.h / 2

    def update(self, delta, x_speed):
        if not self.hit:
            self.angle += self.freq * delta
            self.rect.y += self.h * 0.02 * math.sin( self.angle)
            if self.rect.y > self.sh:
                self.rect.y = 0
            self.rect.x -= delta * x_speed
            self.center_x = self.rect.x + self.w / 2
            self.center_y = self.rect.y + self.h / 2


    def draw(self, screen):
        if not self.hit:
            screen.blit(self.banner, (self.rect.x, self.rect.y))
        else:
            if self.good:
                if not self.anim_time: 
                    self.anim_time = time.time()
                    self.b_index = 0
                if time.time()-self.anim_time>0.00001:
                    self.anim_time = time.time()
                    if self.b_index<len(self.ops)-1:
                        self.b_index+=1
                    
                current_width, current_height = self.ops[self.b_index].get_size()
                new_x = self.center_x - current_width / 2
                new_y = self.center_y - current_height / 2
                if self.b_index<len(self.ops)-1:
                    screen.blit(self.ops[self.b_index],(new_x, new_y))
                    
            else:
                if not self.anim_time: 
                    self.anim_time = time.time()
                    self.b_index = 1
                
                if time.time()-self.anim_time>0.00005:
                    self.anim_time = time.time()
                    if self.b_index<len(self.banners)-1 and self.b_index != -1:
                        self.b_index+=1
                    else:
                        self.b_index = -1
                if self.b_index != -1:
                    screen.blit(self.banners[self.b_index],(self.rect.x, self.rect.y))

    def sort_nums(self,x):
        name = os.path.basename(x)
        return int(name.split('.')[0])



    def getx(self):
        return self.rect.x