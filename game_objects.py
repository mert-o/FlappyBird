import pygame
import glob
import random
import math
import time
class Balloon:
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
        self.freq = 2.5
        self.angle = 0
        self.hit = False
        self.anim_time = 0
    def update(self, delta, x_speed):
        self.angle += self.freq * delta
        self.rect.y += self.h * 0.05 * math.sin( self.angle)

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