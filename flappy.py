
from itertools import cycle
import os,glob
import random
import sys
import pygame
from pygame.locals import *
from videocapture import videocapture
from mediap import media
import cv2 as cv
import button
import json
import time
import numpy as np
import datetime
from game_objects import *
from settings import Settings
from assets import * 
from screen_recorder import ScreenRecorder


os.environ['SDL_VIDEO_CENTERED'] = '1'
pygame.init()
pygame.font.init()


FPSCLOCK = pygame.time.Clock()

info = pygame.display.Info()
SCREENWIDTH, SCREENHEIGHT = info.current_w, info.current_h
SCREEN  = pygame.display.set_mode((0,0),pygame.SHOWN)

print(SCREENWIDTH,SCREENHEIGHT)
print(info.current_w,info.current_h)

pygame.display.set_caption('Flappy Bird')



FPS = 60

REF_WIDTH = 1280
REF_HEIGHT = 720
DEFAULT_BG_SIZE = (REF_WIDTH,REF_HEIGHT)
x_scale = SCREENWIDTH / REF_WIDTH
y_scale = SCREENHEIGHT / REF_HEIGHT
size_scale = min(x_scale, y_scale)


NOSOUND = False
PIPEGAPSIZE  = 330 
BASEY = SCREENHEIGHT * 0.79
min_smile = 8
max_smile = 32
_set_max_acc = 0.42
_set_descent_speed = 0.015

mins_l = []
maxs_l = []
landmark_list = []
BIG_STAR = False
START = True
GAME_MODES = {"space":True,"smile":False,"altitude":False}
GAME_DIFFICULTY = {"easy":True,"medium":False,"hard":False,"arcade":False}
GAME_TYPE = {'pipes':True,'stars': False,'balloons':False,'pisa':False,'banners':False,'pisabal':False,'levels':False}
NEW_HIGH_SCORE = False
HEARTS = 3
CRASHED = False
CRASHED_TIME = 0


input_text = 'Player'

LANDMARKS = False
RECORD = False
nameSet = False
FX = False
HOPPED = False
PIPE_OFFSET = 100
PIPE_OFFSET_ = PIPE_OFFSET

file_path = "scores.json"
GOLD_COLOR = (255,215,0)
SILVER_COLOR = (192,192,192)
BRONZ_COLOR = (185,114,45)
BASES_LIST = []


IMAGES = load_images(SCREENWIDTH,SCREENHEIGHT)

#scale images to according to the reference size
for key in IMAGES.keys():
    try:
        for image in IMAGES[key]:
            image = pygame.transform.scale(image, (int(image.get_width() * x_scale ), int(image.get_height() * y_scale)))
    except:
        IMAGES[key] = pygame.transform.scale(IMAGES[key], (int(IMAGES[key].get_width() * x_scale ), int(IMAGES[key].get_height() * y_scale)))

SOUNDS = load_sounds()

# numbers sprites for score display


big_star_w = IMAGES['star_big'].get_width()
big_star_h = IMAGES['star_big'].get_height()
star_w = IMAGES['star'].get_width()
star_h = IMAGES['star'].get_height()



wing = pygame.mixer.Channel(6)
burn_channel = pygame.mixer.Channel(0)
oops_channel = pygame.mixer.Channel(1)

burn_channel.set_volume(10.0) 


messagex = SCREENWIDTH//2- IMAGES['message'].get_width()//2
messagey = int(SCREENHEIGHT * 0.12)
messagex2 = SCREENWIDTH//2 - IMAGES['message2'].get_width()//2
messagey2 = int(SCREENHEIGHT * 0.8 - IMAGES['message2'].get_height()-20) 

calibrate_rect = IMAGES['calibrate_img'].get_rect()
calib_pos = (SCREENWIDTH/2- IMAGES['calibrate_img'].get_width()/2 ,SCREENHEIGHT/2)
calibrate_rect.x = calib_pos[0]
calibrate_rect.y = calib_pos[1]

settings_rect = IMAGES['settings_img'].get_rect()
settings_pos = (SCREENWIDTH/2-IMAGES['settings_img'].get_width()/2,SCREENHEIGHT/2 + IMAGES['calibrate_img'].get_height() + 30)
settings_rect.x = settings_pos[0]
settings_rect.y = settings_pos[1]


heart_y = 10
heart_x1 = SCREENWIDTH-IMAGES['heart'].get_width() - 10 
heart_x2 = heart_x1 - IMAGES['heart'].get_width() - 10 
heart_x3 = heart_x2 - IMAGES['heart'].get_width() - 10


font = pygame.font.Font("assets/game_font.ttf", int(42*size_scale) )
font2 = pygame.font.Font("assets/game_font.ttf", int(26*size_scale) )
avatars = sorted(glob.glob('./assets/avatars/*.jpg')) + sorted(glob.glob('./assets/avatars/*.png'))
current_avatar = 0
next_avatar = font2.render('Next',True,(30,30,30))
prev_avatar = font2.render('Prev',True,(30,30,30))




video_capture = videocapture(0)
video_capture.start()
landmark = media(video_capture).start()
facemask = None#facemasks(video_capture).start()
high_scores = None
settings = Settings(SCREEN)
sc = ScreenRecorder(SCREEN)



def main():
        # select random player sprites
    global BASES_LIST,NEW_HIGH_SCORE,high_scores,file_path,input_text,PIPEGAPSIZE,GAME_TYPE, nameSet,RECORD,recorder,HEARTS,CRASHED
    


    


    BASES_LIST = [{'x':0,'y':SCREENHEIGHT*0.1},
              {'x':IMAGES['base'].get_width(),'y':SCREENHEIGHT  * 0.1}]
    
    LEVELS = False
    while True:
        
        
        #configure langmarks and set the player
        if not landmark.configured:
            configureSmile()
        last_player, last_avatar = get_last_player()
        if last_player: 
            nameSet = True
            input_text = last_player
            current_avatar = avatars.index(last_avatar)
        if not nameSet:
            setName()
        high_scores = read_high_scores(file_path)
        showWelcomeAnimation()

        if GAME_TYPE['balloons'] or GAME_TYPE['banners'] or GAME_TYPE['pisabal']:
            IMAGES['player'] = (
                pygame.image.load('assets/sprites/Ak_upflap.png').convert_alpha(),
                pygame.image.load('assets/sprites/Ak_midflap.png').convert_alpha(),
                pygame.image.load('assets/sprites/Ak_downflap.png').convert_alpha(),
            )
        else:
            IMAGES['player'] = (
                pygame.image.load('assets/sprites/yellowbird-upflap.png').convert_alpha(),
                pygame.image.load('assets/sprites/yellowbird-midflap.png').convert_alpha(),
                pygame.image.load('assets/sprites/yellowbird-downflap.png').convert_alpha(),
            )

        HEARTS = 15
        

        CRASHED = False
        """
        levels mode:
        stars -> balloons -> pisabal modes
        each mode is played for a certain time set in mainGame function
        a text is displayed in each iteration of the modes with next_level function
        """
        if GAME_TYPE['levels']:
            LEVELS = True
            if RECORD:
                #video_capture.start_recording()
                sc.start_recording()
            if  next_level('pipes'):
                update_dict(GAME_MODES,'smile')
                update_dict(GAME_DIFFICULTY,'easy')
                update_dict(GAME_TYPE,'pipes')
                info = mainGame(levels=True)
            else: info = None
            if info is not None:
                if info['levels']:
                    if next_level('stars') :
                        update_dict(GAME_TYPE,'stars')
                        info = mainGame(score = info['score'],levels=True)
                    else: info = None
            if info is not None:
                if info['levels']:
                    if next_level('balloons'):
                        update_dict(GAME_TYPE,'balloons')
                        info = mainGame(score = info['score'],levels=True)
                    else: info = None
            if info is not None:
                if info['levels']:
                    if next_level('pisabal'):
                        update_dict(GAME_TYPE,'pisabal')
                        info = mainGame(score = info['score'],levels=True)
                    else: info = None
            if info is not None:
                if info['levels']:
                    if next_level('finished'):
                        info = None
                    else: info = None
            update_dict(GAME_TYPE,'levels')
            if RECORD:
                #video_capture.stop_recording()
                sc.stop_recording()
        else:
            LEVELS = False
            if RECORD:
                #video_capture.start_recording()
                sc.start_recording()
                

            info = mainGame()
            if RECORD:
                #video_capture.stop_recording()
                sc.stop_recording()
                
        # player can die in these modes so we have a game over screen
        if (GAME_TYPE['pipes'] or GAME_TYPE['pisa'] or GAME_TYPE['pisabal']) and info is not None :
            showGameOverScreen(info, LEVELS)
        
        if (GAME_TYPE['stars'] or GAME_TYPE['balloons'] or GAME_TYPE['banners']) and info is not None:
            session_ending(info)
        

def showWelcomeAnimation():
    global START,PIPEGAPSIZE,GAME_TYPE,GAME_DIFFICULTY,game_mode,game_type,game_difficulty,GAME_MODES,RECORD,LANDMARKS,FX,current_avatar,calibrate_rect,settings_rect
    START = True
    SHOW_SETTINGS = False
    # index of player to blit on screen
    playerIndex = 0
    playerIndexGen = cycle([0, 1, 2, 1])
    # iterator used to change playerIndex after every 5th iteration
    iterloop = 0

    playerx = int(SCREENWIDTH/2 - 120)
    playery = int(SCREENHEIGHT* 0.1)
    
    ossilate_player = 0
    ossilation_up = True
    temp = True
    
    
    while temp:
        
        dt = FPSCLOCK.tick(FPS)
        
        last_player, last_avatar = get_last_player()
        if last_player:
            input_text = last_player
            current_avatar = avatars.index(last_avatar)
        
        #show current player name and avatar on top right corner of the screen
        avatar_image = pygame.image.load(avatars[current_avatar])
        avatar_image = pygame.transform.scale(avatar_image,(64,64))
        text_surface = font2.render(input_text,True,(0,255,0))
        
        # the text is clickable so a new player can be set
        button_rect = text_surface.get_rect()
        button_rect.x = SCREENWIDTH - text_surface.get_width()-avatar_image.get_width()
        button_rect.y = avatar_image.get_height()//2 - text_surface.get_height()//2
        mpos = (0,0)
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                if SHOW_SETTINGS:
                    SHOW_SETTINGS = False
                else:
                    video_capture.stop_video()
                    landmark.stop_media()
                    #facemask.stop_mask()
                    pygame.quit()
                    sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                # make first flap sound and return values for mainGame
                temp = False
                if not NOSOUND: SOUNDS['wing'].play()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    mpos = pygame.mouse.get_pos()
                    # Use event.pos or pg.mouse.get_pos().
                    if button_rect.collidepoint(mpos):
                        setName()
                    elif calibrate_rect.collidepoint(mpos) and not SHOW_SETTINGS:
                        configureSmile()
                    elif settings_rect.collidepoint(mpos):
                        SHOW_SETTINGS = True

        if LANDMARKS:
            setBG(landmark.frame)
        elif FX:
            setBG(facemask.frame)
        else:
            setBG(video_capture.frame)

        if not landmark.configured:
            return

        #ossilate player position y in welcome screen between -8 +8
        if ossilate_player < 8 and ossilation_up: 
            ossilate_player += 0.05 * dt
        elif ossilate_player >= 8: ossilation_up = False

        if ossilate_player >-8 and not ossilation_up:
            ossilate_player -= 0.05 * dt
        elif ossilate_player <= -8:
            ossilation_up = True


        if SHOW_SETTINGS:
            GAME_TYPE, GAME_MODES, GAME_DIFFICULTY, LANDMARKS,RECORD =  settings.draw(mpos)
            for k,v in GAME_TYPE.items():
                if v:
                    game_type = k
            for k,v in GAME_MODES.items():
                if v:
                    game_mode = k
                
            for k,v in GAME_DIFFICULTY.items():
                if v:
                    game_difficulty = k
        else:
            SCREEN.blit(IMAGES['player'][playerIndex],
                    (playerx, playery + ossilate_player))
            SCREEN.blit(IMAGES['message'], (messagex, messagey))
            SCREEN.blit(IMAGES['message2'], (messagex2, messagey2))
        
            SCREEN.blit(IMAGES['calibrate_img'],calib_pos)

            SCREEN.blit(IMAGES['settings_img'],settings_pos)


            SCREEN.blit(text_surface,(SCREENWIDTH - avatar_image.get_width()- text_surface.get_width()-2,avatar_image.get_height()//2-text_surface.get_height()//2))
            SCREEN.blit(avatar_image,(SCREENWIDTH - avatar_image.get_width(),0))


        SCREEN.blit(IMAGES['base'],(0,int(SCREENHEIGHT-IMAGES['base'].get_height())))

        if GAME_DIFFICULTY['easy']:
            PIPEGAPSIZE = 330
        elif GAME_DIFFICULTY['medium']:
            PIPEGAPSIZE = 270
        elif GAME_DIFFICULTY['hard']:
            PIPEGAPSIZE = 210
        elif GAME_DIFFICULTY['arcade']:
            PIPEGAPSIZE = 300

        if iterloop %5 == 0:
            playerIndex = next(playerIndexGen)
        iterloop = (iterloop + 1) % 30
        pygame.display.update()
        

def mainGame(score=0,levels=False):
    global LANDMARKS,GAME_MODES,HOPPED,_set_max_acc,_set_descent_speed,min_smile,max_smile,mins_l,maxs_l,BIG_STAR,high_scores,BASES_LIST,GAME_DIFFICULTY,PIPEGAPSIZE,game_type,game_mode,game_difficulty,star_w,HEARTS,CRASHED,CRASHED_TIME
    #landmark.num_stars = 0

    score = score
    playerIndex = 0
    playerIndexGen = cycle([0, 1, 2, 1])
    iterloop = 0
    
    if not GAME_TYPE['balloons'] and not GAME_TYPE['banners']:
        playerx, playery = int(SCREENWIDTH * 0.2), int(SCREENHEIGHT * 0.5) 
    else:
        playerx, playery = int(SCREENWIDTH * 0.1), int(SCREENHEIGHT * 0.5) 

    proccessed_scores = []

    # get 2 new pipes to add to upperPipes lowerPipes list
    if GAME_TYPE['pipes']:
        if GAME_DIFFICULTY['arcade']:
            newPipe = getRandomPipe('9')
            upperPipes = []
            lowerPipes = []
            upperPipes.append(newPipe[0])
            lowerPipes.append(newPipe[1])
        else:
            newPipe1 = getRandomPipe()
            newPipe2 = getRandomPipe()
            # list of upper pipes
            upperPipes = [
                {'x': int(SCREENWIDTH/2), 'y': newPipe1[0]['y'],"score":False, "crashed":False},
                {'x': int(SCREENWIDTH - IMAGES['pipe'][0].get_width()), 'y': newPipe2[0]['y'],"score":False, "crashed":False},
            ]

            # list of lowerpipe
            lowerPipes = [
                
                {'x': int(SCREENWIDTH/2), 'y': newPipe1[1]['y'],"score":False, "crashed":False},
                {'x': int(SCREENWIDTH - IMAGES['pipe'][0].get_width()), 'y': newPipe2[1]['y'],"score":False, "crashed":False},
                
            ]
    elif GAME_TYPE['stars']:
        stars = [getNewStar(),getNewStar()]
        stars[0]['x'] = int(SCREENWIDTH*0.5)
        stars[1]['x'] = int(SCREENWIDTH*0.8)
    
        """ elif GAME_TYPE['balloons']:
        BALLOONW = 120
        BALLOONH = 120
        WATERBALLW = 30
        WATERBALLH = 20
        WB = False
        words = []
        with open('words.txt','r') as f:
            lines = f.readlines()
            for line in lines:
                line = line.strip()
                color = line[1]
                word = line[3:]
                words.append([color,word])
                print(word,color)
        
        index = random.randint(0,len(words)-1)
        print(index)
        print(words[index][1],words[index][0])
        balloons = [Balloon(words[index][1],words[index][0],SCREENWIDTH,SCREENHEIGHT,BALLOONW,BALLOONH)]
        water_balls = []
        score_streak = 0
        water_balls_count = 1 """
    
    elif GAME_TYPE['balloons']:
        BALLOONW = 120
        BALLOONH = 120
        WATERBALLW = 30
        WATERBALLH = 20
        WB = False
        
        colors = ['red','green','blue','yellow','orange','purple','pink']
        color = random.choice(colors)

        balloons = [Balloon(color,SCREENWIDTH,SCREENHEIGHT,BALLOONW,BALLOONH)]
        water_balls = []
        score_streak = 0
        water_balls_count = 1
    
    elif GAME_TYPE['banners']:
        BANNERW = 430
        BANNERH = 150
        
        WATERBALLW = 30
        WATERBALLH = 20
        
        
        
        WB = False
        b_paths = glob.glob('./assets/banners3/*')

        b = random.choice(b_paths)
        good = False
        if 'good' in b:
            good = True
        
        banners = [Banners(b,SCREENWIDTH,SCREENHEIGHT,BANNERW,BANNERH,good)]
        water_balls = []
        score_streak = 0
        water_balls_count = 1
        
    elif GAME_TYPE['pisa']:
        stars = [getNewStar(),getNewStar()]
        stars[0]['x'] = int(SCREENWIDTH*0.5)
        stars[1]['x'] = int(SCREENWIDTH*0.8)

        if GAME_DIFFICULTY['arcade']:
            newPipe = getRandomPipe('9')
            upperPipes = []
            lowerPipes = []
            upperPipes.append(newPipe[0])
            lowerPipes.append(newPipe[1])
        else:
            newPipe1 = getRandomPipe()
            newPipe2 = getRandomPipe()
            upperPipes = [
                {'x': int(SCREENWIDTH/2), 'y': newPipe1[0]['y'],"score":False, "crashed":False},
                {'x': int(SCREENWIDTH - IMAGES['pipe'][0].get_width()), 'y': newPipe2[0]['y'],"score":False, "crashed":False},
            ]

            # list of lowerpipe
            lowerPipes = [
                
                {'x': int(SCREENWIDTH/2), 'y': newPipe1[1]['y'],"score":False, "crashed":False},
                {'x': int(SCREENWIDTH - IMAGES['pipe'][0].get_width()), 'y': newPipe2[1]['y'],"score":False, "crashed":False},
                
            ]
    
    elif GAME_TYPE['pisabal']:
        
        BALLOONW = 120
        BALLOONH = 120
        WATERBALLW = 30
        WATERBALLH = 20
        
        WB = False
        colors = ['red','green','blue','yellow','orange','purple','pink']
        color = random.choice(colors)
        balloons = [Balloon(color,SCREENWIDTH,SCREENHEIGHT,BALLOONW,BALLOONH)]
        water_balls = []
        score_streak = 0
        water_balls_count = 1
        
        
        stars = [getNewStar(),getNewStar()]
        stars[0]['x'] = int(SCREENWIDTH*0.5)
        stars[1]['x'] = int(SCREENWIDTH*0.8)

        newPipe1 = getRandomPipe()
        newPipe2 = getRandomPipe()
        # list of upper pipes
        upperPipes = [
            {'x': int(SCREENWIDTH/2), 'y': newPipe1[0]['y'],"score":False, "crashed":False},
            {'x': int(SCREENWIDTH - IMAGES['pipe'][0].get_width()), 'y': newPipe2[0]['y'],"score":False, "crashed":False},
        ]

        # list of lowerpipe
        lowerPipes = [
            
            {'x': int(SCREENWIDTH/2), 'y': newPipe1[1]['y'],"score":False, "crashed":False},
            {'x': int(SCREENWIDTH - IMAGES['pipe'][0].get_width()), 'y': newPipe2[1]['y'],"score":False, "crashed":False},
            
        ]
        
    lives_left = HEARTS 
    blink_count = 10
    blink_state = False  
    last_blink_time = 0
    blink_interval = 100 


    #speeds
    pipeVelXBase = -0.20 #128
    starVelXBase = 0.20 #128
    BALLOONS = 0.20 #70
    BANNERS = 0.20 #70 
    WATERBALLS = 0.45 #200 

    sbb_max = 0.8
    banners_max = 0.6

    birdy_speed = 0.35 #150
    baseVelx = -0.20 #128
    
    balloon_spawn_time_max = 3
    balloon_spawn_time_min = 0.5
    balloon_spawn_time = 3


    ballon_spawn_time = 3
    playerVelY = 0 
    playerAccY = _set_max_acc
    playerMinAcc = -0.5
    maxAngle = 40
    minAngle = -15
    descentSpeed = _set_descent_speed
    max_acc = _set_max_acc
    min_acc = 0.25
    
    max_acc_a = 0.5 # for altitude mode
    min_acc_a = 0.01 # for altitude mode
    spaceConst = 1
    smileConst = 1
    altitudeConst = 0.6
    
    temp = True
    start_time = time.time()
    level_start_time = time.time()

    countdown_minutes = 10
    max_minutes = 9
    end_time = pygame.time.get_ticks() + countdown_minutes * 60000
    minutes = '9'
    
    player_width = IMAGES['player'][0].get_width()
    player_height = IMAGES['player'][0].get_height()
    base_width =  IMAGES['base'].get_width()
    base_height = IMAGES['base'].get_height()
    pipe_width = IMAGES['pipe'][0].get_width()

    pipe_diff_value = 0.4

    while temp:

        dt = FPSCLOCK.tick(FPS)
        
        if LANDMARKS:
            setBG(landmark.frame)
        elif FX:
            setBG(facemask.frame)
        else:
            if GAME_TYPE['stars'] or GAME_TYPE['pisa']:
                setBG(landmark.fd)
            else:
                setBG(video_capture.frame)
        
        if not landmark.configured:
            return

        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                temp = False
            if event.type == KEYDOWN:
                if event.key == K_SPACE and (GAME_MODES["space"] or GAME_TYPE["pisabal"]):
                    if GAME_TYPE['balloons'] or GAME_TYPE['banners']:
                        for i in range(water_balls_count):
                            water_balls.append(WaterBall(playerx+ player_width+ 5 + i*WATERBALLW,playery + 15,WATERBALLW,WATERBALLH,WATERBALLS))
                    else:
                        if playery > IMAGES['player'][playerIndex].get_height()/2:
                            playerVelY = playerAccY 
                            if not NOSOUND: SOUNDS['wing'].play()
                elif event.key == K_UP and (GAME_TYPE['balloons'] or GAME_TYPE['banners']):
                    playery -= birdy_speed * dt
                elif event.key == K_DOWN and (GAME_TYPE['balloons'] or GAME_TYPE['banners']):
                    playery += birdy_speed * dt
        
        if GAME_TYPE['balloons'] or GAME_TYPE['banners']:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP]:
                playery -= birdy_speed* dt
            elif keys[pygame.K_DOWN]:
                playery += birdy_speed  * dt
                
        elif landmark.smile_level<=-1*(min_smile*1.2)//1*-1 and HOPPED:
            HOPPED = False
        
        if GAME_MODES["smile"] or GAME_TYPE["pisabal"]:
            
            if GAME_TYPE['balloons'] or GAME_TYPE['banners'] or GAME_TYPE['pisabal']:
                if not WB and  landmark.smile_level > -1 * (min_smile*1.2)//1 * -1:
                    mag = (landmark.smile_level - min_smile) * (max_acc - min_acc) / (max_smile - min_smile)  + min_acc
                    if mag > max_acc or landmark.smile_level>=max_smile*0.85 :
                        for i in range(water_balls_count):
                            water_balls.append(WaterBall(playerx+player_width + 5+ i * WATERBALLW,playery +15,WATERBALLW,WATERBALLH,WATERBALLS))
                        WB = True
                elif landmark.smile_level<=-1*(min_smile*1.2)//1*-1 and WB:
                    WB = False
            elif not GAME_TYPE['pisabal']:
                if not HOPPED:
                    print(landmark.smile_level)
                    if landmark.smile_level > -1 * (min_smile*1.2)//1 * -1:
                        mag = (landmark.smile_level - min_smile) * (max_acc - min_acc) / (max_smile - min_smile)  + min_acc
                        
                        playerVelY = max_acc
                        if not NOSOUND: SOUNDS['wing'].play()
                        HOPPED = True
                elif landmark.smile_level<=-1*(min_smile*1.2)//1*-1 and HOPPED:
                    HOPPED = False
                    
        elif GAME_MODES["altitude"]:
            if landmark.smile_level> -1*(min_smile*1)//1*-1:
                mag = (landmark.smile_level - min_smile) * (max_acc_a - min_acc_a) / (max_smile - min_smile)  + min_acc_a
                playerVelY = mag * altitudeConst
                if not wing.get_busy():
                    if not NOSOUND: wing.play(SOUNDS['wing'])

        if not GAME_TYPE['balloons'] and not GAME_TYPE['banners']:
            
            if playerVelY >= 0:
                if playery > IMAGES['player'][playerIndex].get_height()/2:
                    
                    playery -= playerVelY * dt
                else: playerVelY = 0
            if playerVelY<0:
                
                if playery < SCREENHEIGHT - base_height  - player_height*1.5:
                    playery -= playerVelY * dt

            if playerVelY > playerMinAcc:
                playerVelY -= descentSpeed
            
            rotation = (playerVelY - playerMinAcc) * (maxAngle - minAngle) / (playerAccY -playerMinAcc)  +minAngle
            playerSurface = pygame.transform.rotate(IMAGES['player'][playerIndex], rotation)

        else:
            if playery < 5: playery = 5
            elif playery > SCREENHEIGHT-base_height- player_height*1.5:
                playery = SCREENHEIGHT-base_height- player_height*1.5
            playerSurface = IMAGES['player'][playerIndex]


        
        current_time = pygame.time.get_ticks()

        if blink_count < 10 and (GAME_TYPE['pisa'] or GAME_TYPE['pipes'] or GAME_TYPE['pisabal']):
            if current_time - last_blink_time > blink_interval:
                last_blink_time = current_time
                blink_state = not blink_state
                blink_count += 1

                if blink_count >= 10:
                    blink_state = False
                    CRASHED = False     
        if not blink_state:
            SCREEN.blit(playerSurface, (playerx, playery))

        
        if GAME_TYPE['stars']:
            playerMidPos = (playerx + IMAGES['player'][playerIndex].get_width() / 2,playery +IMAGES['player'][playerIndex].get_height() / 2)
            
            col = checkCollision(stars,playerMidPos)
            
            if col != -100:
                if col <0:
                    #landmark.num_stars += 1
                    stars.pop((-1*(col+1)))
                    score += 8
                else:
                    stars.pop(col)
                    score +=1
                if (score+1) % 15 == 0:
                    if score not in proccessed_scores:
                        proccessed_scores.append(score)
                        BIG_STAR = True
                if not NOSOUND: SOUNDS['stars'].play() 
            
            if GAME_DIFFICULTY['arcade']:
                starVelXBase = 0.20 + ((max_minutes-int(minutes))/max_minutes) * (sbb_max-0.2)
                

            # move star to left
            for star in stars:
                star['x'] -= starVelXBase * dt
                if star['b']:
                    SCREEN.blit(IMAGES['star_big'],(star['x'],star['y']))
                else:
                    SCREEN.blit(IMAGES['star'],(star['x'],star['y']))

            if stars[-1]['x'] <= SCREENWIDTH*0.6 and not BIG_STAR:
                stars.append(getNewStar())

            if BIG_STAR:
                stars.append(getBigStar())
                BIG_STAR = False
            # remove first pipe if its out of the screen
            if len(stars) > 0 and stars[0]['x'] < -star_w:
                stars.pop(0)

        elif GAME_TYPE['pipes']:
            playerMidPos = (playerx,playery)
            if checkCrash(playerMidPos,upperPipes,lowerPipes):
                return {
                    'score':score,
                    'y': playery,
                    'up': upperPipes,
                    'lp': lowerPipes,
                    'minutes':minutes,
                    'seconds':seconds,
                    'levels':False
                }
            else:
                for i in range(len(upperPipes)):
                    
                    if playerMidPos[0] >= upperPipes[i]['x'] + pipe_width//2 and not upperPipes[i]['score'] and not upperPipes[i]['crashed'] and not lowerPipes[i]['crashed']:
                        score += 1
                        upperPipes[i]['score'] = True
                        if not NOSOUND: SOUNDS['pipes'].play()
                    upperPipes[i]['x'] += pipeVelXBase * dt
                    lowerPipes[i]['x'] += pipeVelXBase * dt

                    SCREEN.blit(IMAGES['pipe'][0],(upperPipes[i]['x'],upperPipes[i]['y']))
                    SCREEN.blit(IMAGES['pipe'][1],(lowerPipes[i]['x'],lowerPipes[i]['y']))

                if upperPipes[-1]['x'] <= SCREENWIDTH*pipe_diff_value:
                    
                    if GAME_DIFFICULTY['arcade']:
                        newPipe = getRandomPipe(minutes)
                        pipe_diff_value = 0.4 + ((max_minutes-int(minutes))/max_minutes) * (0.8-0.4)
                    else:
                        newPipe = getRandomPipe()
                    upperPipes.append(newPipe[0])
                    lowerPipes.append(newPipe[1])
                    

                if len(upperPipes)>0 and upperPipes[0]['x'] < - pipe_width:
                    upperPipes.pop(0)
                    lowerPipes.pop(0)
                
                text_lives = str(lives_left) + "/15"
                text_lives_surface = font.render(text_lives,True,(0,0,0))
                text_lives_rect = text_lives_surface.get_rect()
                text_lives_rect.x = heart_x1 - text_lives_rect.width - 10
                text_lives_rect.y = 7
                SCREEN.blit(IMAGES['heart'], (heart_x1, heart_y))
                SCREEN.blit(text_lives_surface,text_lives_rect)

        elif GAME_TYPE['balloons']:
            if balloons:
                if balloons[0].getx() + balloons[0].w < 0:
                    balloons.pop(0)

            if GAME_DIFFICULTY['arcade']:
                BALLOONS = 0.20 + ((max_minutes-int(minutes))/max_minutes) * (sbb_max-0.2)
                balloon_spawn_time = balloon_spawn_time_min + ((int(minutes))/max_minutes) * (balloon_spawn_time_max-balloon_spawn_time_min)

            for b in balloons:
                b.update(dt, BALLOONS)
                b.draw(SCREEN)

            for wb in water_balls:

                wb.update(dt)
                wb.draw(SCREEN)

                if not wb.hit:
                    for b in balloons:
                        if not b.hit and wb.hits(b): 
                            b.hit = True
                            wb.hit = True
                            score += 1
                            if not NOSOUND: SOUNDS['pop'].play()
            if water_balls and water_balls[-1].getx()>SCREENWIDTH:
                water_balls.pop(-1)

            if time.time() - start_time> balloon_spawn_time:
                color = random.choice(colors)
                balloons.append(Balloon(color,SCREENWIDTH,SCREENHEIGHT,BALLOONW,BALLOONH))
                start_time = time.time()
                
        elif GAME_TYPE['banners']:
            
            if banners[0].getx() + banners[0].w < 0:
                banners.pop(0)

            if GAME_DIFFICULTY['arcade']:
                BANNERS = 0.20 + ((max_minutes-int(minutes))/max_minutes) * (banners_max-0.2)
                balloon_spawn_time = 0.8 + ((int(minutes))/max_minutes) * (balloon_spawn_time_max-0.8)

            for b in banners:
                b.update(dt,BANNERS )
                b.draw(SCREEN)

            for wb in water_balls:

                wb.update(dt)
                wb.draw(SCREEN)

                if not wb.hit:
                    for b in banners:
                        if not b.hit and wb.hits(b): 
                            b.hit = True
                            wb.hit = True
                            if b.good:
                                if not NOSOUND: oops_channel.play(SOUNDS['oops'])
                                if score >0:
                                    score -=1
                                    score_streak = 0
                                    water_balls_count = 1
                            else:
                                score += 1
                                if not NOSOUND: burn_channel.play(SOUNDS['burn'])
                                score_streak += 1
                                if score_streak %5 == 0:
                                    water_balls_count += 1
            if water_balls and water_balls[-1].getx()>SCREENWIDTH:
                water_balls.pop(-1)

            if time.time() - start_time> balloon_spawn_time:
                b = random.choice(b_paths)
                good = False
                if 'good' in b.split('/')[-1].split('.')[0]:
                    good = True
                banners.append(Banners(b,SCREENWIDTH,SCREENHEIGHT,BANNERW,BANNERH,good))
                start_time = time.time()
        
        
        
        elif GAME_TYPE['pisa']:
            playerMidPos = (playerx + IMAGES['player'][playerIndex].get_width() / 2,playery +IMAGES['player'][playerIndex].get_height() / 2)
            col = checkCollision(stars,playerMidPos)
            if col != -100:
                if col <0:
                    #landmark.num_stars += 1
                    stars.pop((-1*(col+1)))
                    score += 8
                else:
                    stars.pop(col)
                    score +=1
                if (score+1) % 15 == 0:
                    if score not in proccessed_scores:
                        proccessed_scores.append(score)
                        BIG_STAR = True
                if not NOSOUND: SOUNDS['stars'].play() 
                
            # move star to left
            for star in stars:
                star['x'] -= starVelXBase * dt
                if star['b']:
                    SCREEN.blit(IMAGES['star_big'],(star['x'],star['y']))
                else:
                    SCREEN.blit(IMAGES['star'],(star['x'],star['y']))

            if stars[-1]['x'] <= SCREENWIDTH*0.6 and not BIG_STAR:
                stars.append(getNewStar())

            if BIG_STAR:
                stars.append(getBigStar())
                BIG_STAR = False
            # remove first pipe if its out of the screen
            if len(stars) > 0 and stars[0]['x'] < -IMAGES['star'].get_width():
                stars.pop(0)

            if checkCrash(playerMidPos,upperPipes,lowerPipes):
                return{
                    'score':score,
                    'y': playery,
                    'up': upperPipes,
                    'lp': lowerPipes,
                    'minutes':minutes,
                    'seconds':seconds,
                    'levels':False
                }
            else:
                for i in range(len(upperPipes)):

                    if playerMidPos[0] >= upperPipes[i]['x'] + pipe_width//2 and not upperPipes[i]['score'] and not upperPipes[i]['crashed'] and not lowerPipes[i]['crashed']:
                        upperPipes[i]['score'] = True
                        if not NOSOUND: SOUNDS['pipes'].play()


                    upperPipes[i]['x'] += pipeVelXBase * dt
                    lowerPipes[i]['x'] += pipeVelXBase * dt

                    SCREEN.blit(IMAGES['pipe'][0],(upperPipes[i]['x'],upperPipes[i]['y']))
                    SCREEN.blit(IMAGES['pipe'][1],(lowerPipes[i]['x'],lowerPipes[i]['y']))

                if upperPipes[-1]['x'] <= SCREENWIDTH*pipe_diff_value:
                    
                    if GAME_DIFFICULTY['arcade']:
                        newPipe = getRandomPipe(minutes)
                        pipe_diff_value = 0.4 + ((max_minutes-int(minutes))/max_minutes) * (0.8-0.4)
                    else:
                        newPipe = getRandomPipe()
                    upperPipes.append(newPipe[0])
                    lowerPipes.append(newPipe[1])

                if len(upperPipes)>0 and upperPipes[0]['x'] < - pipe_width:
                    upperPipes.pop(0)
                    lowerPipes.pop(0)
            
                
                text_lives = str(lives_left) + "/15"
                text_lives_surface = font.render(text_lives,True,(0,0,0))
                text_lives_rect = text_lives_surface.get_rect()
                text_lives_rect.x = heart_x1 - text_lives_rect.width - 10
                text_lives_rect.y = 7
                SCREEN.blit(IMAGES['heart'], (heart_x1, heart_y))
                SCREEN.blit(text_lives_surface,text_lives_rect)
                


        elif GAME_TYPE['pisabal']:
            playerMidPos = (playerx + IMAGES['player'][playerIndex].get_width() / 2,playery +IMAGES['player'][playerIndex].get_height() / 2)
            col = checkCollision(stars,playerMidPos)
            if col != -100:
                if col <0:
                    #landmark.num_stars += 1
                    stars.pop((-1*(col+1)))
                    score += 8
                else:
                    stars.pop(col)
                    score +=1
                if (score+1) % 15 == 0:
                    if score not in proccessed_scores:
                        proccessed_scores.append(score)
                        BIG_STAR = True
                if not NOSOUND: SOUNDS['point'].play() 
                
            # move star to left
            for star in stars:
                star['x'] -= starVelXBase * dt
                if star['b']:
                    SCREEN.blit(IMAGES['star_big'],(star['x'],star['y']))
                else:
                    SCREEN.blit(IMAGES['star'],(star['x'],star['y']))

            if stars[-1]['x'] <= SCREENWIDTH*0.6 and not BIG_STAR:
                stars.append(getNewStar())

            if BIG_STAR:
                stars.append(getBigStar())
                BIG_STAR = False
            # remove first pipe if its out of the screen
            if len(stars) > 0 and stars[0]['x'] < -IMAGES['star'].get_width():
                stars.pop(0)

            if checkCrash(playerMidPos,upperPipes,lowerPipes):
                return{
                    'score':score,
                    'y': playery,
                    'up': upperPipes,
                    'lp': lowerPipes,
                    'minutes':minutes,
                    'seconds':seconds,
                    'levels':False
                }
            else:
                for i in range(len(upperPipes)):
                    upperPipes[i]['x'] += pipeVelXBase * dt
                    lowerPipes[i]['x'] += pipeVelXBase * dt

                    SCREEN.blit(IMAGES['pipe'][0],(upperPipes[i]['x'],upperPipes[i]['y']))
                    SCREEN.blit(IMAGES['pipe'][1],(lowerPipes[i]['x'],lowerPipes[i]['y']))

                if upperPipes[-1]['x'] <= SCREENWIDTH*0.6:
                    newPipe = getRandomPipe()
                    upperPipes.append(newPipe[0])
                    lowerPipes.append(newPipe[1])

                if len(upperPipes)>0 and upperPipes[0]['x'] < - pipe_width:
                    upperPipes.pop(0)
                    lowerPipes.pop(0)

            if balloons:
                if balloons[0].getx() + balloons[0].w < 0:
                    balloons.pop(0)

            
            for b in balloons:
                b.update(dt, BALLOONS)
                b.draw(SCREEN)

            for wb in water_balls:

                wb.update(dt)
                wb.draw(SCREEN)

                if not wb.hit:
                    for b in balloons:
                        if not b.hit and wb.hits(b): 
                            b.hit = True
                            wb.hit = True

                            score += 1
                            if not NOSOUND: SOUNDS['point'].play()

                            """ if b.color =='b':
                                if score >0:
                                    score -=1
                                    score_streak = 0
                                    water_balls_count = 1
                            else:
                                score += 1
                                score_streak += 1
                                if score_streak %5 == 0:
                                    water_balls_count += 1 """
            if water_balls and water_balls[-1].getx()>SCREENWIDTH:
                water_balls.pop(-1)

            if time.time() - start_time> ballon_spawn_time:
                #index = random.randint(0,len(words)-1)
                #balloons.append(Balloon(words[index][1],words[index][0],SCREENWIDTH,SCREENHEIGHT,BALLOONW,BALLOONH))
                color = random.choice(colors)
                balloons.append(Balloon(color,SCREENWIDTH,SCREENHEIGHT,BALLOONW,BALLOONH))
                start_time = time.time()

            text_lives = str(lives_left) + "/15"
            text_lives_surface = font.render(text_lives,True,(0,0,0))
            text_lives_rect = text_lives_surface.get_rect()
            text_lives_rect.x = heart_x1 - text_lives_rect.width - 10
            text_lives_rect.y = 7
            SCREEN.blit(IMAGES['heart'], (heart_x1, heart_y))
            SCREEN.blit(text_lives_surface,text_lives_rect)
        
        showScore(score)

        now = pygame.time.get_ticks()
        if now < end_time:
            total_seconds = (end_time - now) // 1000 
            minutes = int(total_seconds // 60)
            seconds = int(total_seconds % 60)
        else:
            minutes, seconds = 0, 0
            if GAME_TYPE['stars'] or GAME_TYPE['banners'] or GAME_TYPE['balloons']:
                return score
            else:
                return {
                    'score':score,
                    'y': playery,
                    'up': upperPipes,
                    'lp': lowerPipes,
                    'minutes':minutes,
                    'seconds':seconds,
                    'levels':False
                }

        
        minutes = str(minutes).rjust(2,'0')
        seconds = str(seconds).rjust(2,'0')
        
        showTime(minutes,seconds)   
        
        if iterloop %5 == 0:
            playerIndex = next(playerIndexGen)
            
        iterloop = (iterloop + 1) % 30      
        
        if BASES_LIST[0]['x'] + base_width<=0:
            BASES_LIST.pop(0)

        if len(BASES_LIST)<3:
            BASES_LIST.append({'x':BASES_LIST[-1]['x']+base_width,'y':SCREENHEIGHT*0.1})


        for base in BASES_LIST:
            base['x'] += baseVelx * dt
            SCREEN.blit(IMAGES['base'],(base['x'],int(SCREENHEIGHT-IMAGES['base'].get_height())))
        

        #levels mode level time 
        if levels and time.time() - level_start_time> 120:
            print('here')
            return {'levels':levels,
                    'y':playery,
                    'score':score}
        
        """ if GAME_TYPE['stars'] or GAME_TYPE['banners'] or GAME_TYPE['balloons']:
            if time.time() - level_start_time>600:
                return score """

        if HEARTS < lives_left:
            lives_left = HEARTS
            blink_count = 0

        pygame.display.update()
    
def showGameOverScreen(crashInfo,levels = False):
    global file_path,GAME_MODES,BASES_LIST,high_scores,game_mode,game_type,game_difficulty,NEW_HIGH_SCORE,LANDMARKS,FX,input_text
    score = crashInfo['score']
    playerx = SCREENWIDTH * 0.2
    playery = crashInfo['y']
    minutes = crashInfo['minutes']
    seconds = crashInfo['seconds']
    try:
        upperPipes = crashInfo['up']
        lowerPipes = crashInfo['lp']
    except:
        upperPipes = []
        lowerPipes = []
    # play hit and die sounds
    if not NOSOUND:
        SOUNDS['hit'].play()
        SOUNDS['die'].play()


    if LANDMARKS:
        frame = landmark.frame
    elif FX:
        frame = facemask.frame    
    else:
        if GAME_TYPE['stars']:
            frame = landmark.fd
        else:
            frame = video_capture.frame
    processedScore = False
    while True:
        dt = FPSCLOCK.tick(FPS)
        events = pygame.event.get()
        for event in events:
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE) or (event.type == KEYDOWN and event.key == K_SPACE):
                
                return

        if not landmark.configured:
            return
        # player y shift
        if playery < SCREENHEIGHT - IMAGES['base'].get_height() - IMAGES['player'][0].get_height() * 1.2:
            playery += 0.1 * dt

        playerRot  = -75
        setBG(frame)

        if upperPipes:
            for uPipe, lPipe in zip(upperPipes, lowerPipes):
                SCREEN.blit(IMAGES['pipe'][0], (uPipe['x'], uPipe['y']))
                SCREEN.blit(IMAGES['pipe'][1], (lPipe['x'], lPipe['y']))

        playerSurface = pygame.transform.rotate(IMAGES['player'][1], playerRot)
        SCREEN.blit(playerSurface, (playerx,playery))
        #SCREEN.blit(IMAGES['gameover'], ((SCREENWIDTH -IMAGES['gameover'].get_width())/2 , (SCREENHEIGHT-IMAGES['gameover'].get_height())/2))

        for base in BASES_LIST:
            SCREEN.blit(IMAGES['base'],(base['x'],int(SCREENHEIGHT-IMAGES['base'].get_height())))
        
        #processedScore =  showLeaderBoard(score,processedScore,levels)

        minutes = str(minutes).rjust(2,'0')
        seconds = str(seconds).rjust(2,'0')
        
        showTime(minutes,seconds)
        showScore(score)
        write_high_scores()
        pygame.display.update()

def getNewStar():
       
      return {'x':random.randrange(int(SCREENWIDTH*0.7),SCREENWIDTH),
            'y':random.randrange(int(SCREENHEIGHT*0.2),int((SCREENHEIGHT-IMAGES['base'].get_height())*0.8)),
    'score': False,'b':False}

def getBigStar():
    return {'x':random.randrange(int(SCREENWIDTH*0.7),SCREENWIDTH),
            'y':random.randrange(int(SCREENHEIGHT*0.3),int((SCREENHEIGHT-IMAGES['base'].get_height())*0.6)),
            'score': False,'b':True}

def getRandomPipe(minutes=None):

    if minutes:
        minutes = int(minutes)
        min_upper_y = -IMAGES['pipe'][0].get_height() + IMAGES['player'][0].get_height() + 10
        max_upper_y = SCREENHEIGHT - IMAGES['base'].get_height() - IMAGES['player'][0].get_height()*2 - PIPEGAPSIZE - IMAGES['pipe'][0].get_height() - IMAGES['player'][0].get_height() * (5 +(10-minutes)/10*(20-5))

        #upper_y = random.randrange(min_upper_y, max_upper_y)
        upper_y = max_upper_y
        lower_y = upper_y + IMAGES['pipe'][0].get_height() + PIPEGAPSIZE
        pipeX = SCREENWIDTH 
        
        return [
            {'x': pipeX + (10-minutes)*30, 'y': upper_y, "score": False, "crashed":False},  # upper pipe
            {'x': pipeX + 30, 'y': lower_y, "score": False, "crashed":False},  # lower pipe
        ]
    else:

        min_upper_y = -IMAGES['pipe'][0].get_height() + IMAGES['player'][0].get_height() + 10
        max_upper_y = SCREENHEIGHT - IMAGES['base'].get_height() - IMAGES['player'][0].get_height()*2 - PIPEGAPSIZE - IMAGES['pipe'][0].get_height() - 10

        upper_y = random.randrange(min_upper_y, max_upper_y)
        lower_y = upper_y + IMAGES['pipe'][0].get_height() + PIPEGAPSIZE
        pipeX = SCREENWIDTH + 30
        
        return [
            {'x': pipeX, 'y': upper_y, "score": False, "crashed":False},  # upper pipe
            {'x': pipeX, 'y': lower_y, "score": False, "crashed":False},  # lower pipe
        ]

def setBG(frame, f = False):
    if frame is not None:
        bg = cv.resize(frame,(SCREENWIDTH,SCREENHEIGHT))
        #bg = cv.flip(bg,1)
        bg = cv.cvtColor(bg,cv.COLOR_BGR2RGB)
        
        #bg = pygame.image.frombuffer(bg.tostring(), bg.shape[1::-1], "BGR")
        bg = pygame.surfarray.make_surface(bg)
        bg = pygame.transform.rotate(bg, -90)
        SCREEN.blit(bg,(0,0))

def showScore(score,gameOver = False):
    global high_scores,game_type,game_mode,game_difficulty,font,NEW_HIGH_SCORE
    scoreDigits = [int(x) for x in list(str(score))]
    totalWidth = 0 # total width of all numbers to be printed

    if not gameOver:
        for digit in scoreDigits:
            totalWidth += IMAGES['numbers'][digit].get_width()
        Xoffset = (SCREENWIDTH - totalWidth) / 2
        for digit in scoreDigits:
            SCREEN.blit(IMAGES['numbers'][digit], (Xoffset, SCREENHEIGHT * 0.1))
            Xoffset += IMAGES['numbers'][digit].get_width()

def showTime(mins,secs):
    global font

    height = SCREENHEIGHT * 0.1 - IMAGES['numbersg'][0].get_height() - 5

    minDigits = [int(x) for x in list(str(mins))]
    totalWidth = 0 
    for digit in minDigits:
        totalWidth += IMAGES['numbersg'][digit].get_width()
    Xoffset = SCREENWIDTH / 2 - totalWidth - IMAGES['colon'].get_width()
    for digit in minDigits:
        SCREEN.blit(IMAGES['numbersg'][digit], (Xoffset, height))
        Xoffset += IMAGES['numbersg'][digit].get_width()
    
    Xoffset += 2
    SCREEN.blit(IMAGES['colon'], (Xoffset, height+5))
    Xoffset += IMAGES['colon'].get_width()  + 2

    secDigits = [int(x) for x in list(str(secs))]
    totalWidth = 0
    for digit in secDigits:
        SCREEN.blit(IMAGES['numbersg'][digit], (Xoffset, height))
        Xoffset += IMAGES['numbersg'][digit].get_width()



def showLeaderBoard(score,processedScore,levels = False):
    
    global font,high_scores,input_text,GOLD_COLOR,BRONZ_COLOR,SILVER_COLOR

    text_offset = 30
    text_start_height = 0.1
    game_mode = get_game_mode()
    game_type = get_game_type()
    game_difficulty = get_game_difficulty()
    if  game_type == 'stars' or game_type == 'balloons' or game_type == 'banners' or game_type == 'levels':

        first_n = high_scores[game_type][game_mode]['1st']["name"]
        second_n =  high_scores[game_type][game_mode]['2nd']["name"]
        third_n =  high_scores[game_type][game_mode]['3rd']["name"]
        
        first_s = high_scores[game_type][game_mode]['1st']["s"]
        second_s =  high_scores[game_type][game_mode]['2nd']["s"]
        third_s =  high_scores[game_type][game_mode]['3rd']["s"]
        
        try: 
            first_a = high_scores[game_type][game_mode]['1st']["avatar"]
        except: first_a = None
        try:
            second_a =  high_scores[game_type][game_mode]['2nd']["avatar"]
        except: second_a = None
        try:
            third_a =  high_scores[game_type][game_mode]['3rd']["avatar"]
        except: third_a = None
        
        if not processedScore:
            if score > first_s: 
                
                high_scores[game_type][game_mode]['3rd']["name"] = second_n
                high_scores[game_type][game_mode]['3rd']["s"] = second_s
                high_scores[game_type][game_mode]['3rd']["avatar"] = second_a
                third_n = second_n
                third_s = second_s
                third_a = second_a

                high_scores[game_type][game_mode]['2nd']["name"] = first_n
                high_scores[game_type][game_mode]['2nd']["s"] = first_s
                high_scores[game_type][game_mode]['2nd']["avatar"] = first_a
                second_n = first_n
                second_s = first_s
                second_a = first_a

                high_scores[game_type][game_mode]['1st']["name"] = input_text
                high_scores[game_type][game_mode]['1st']["s"] = score
                high_scores[game_type][game_mode]['1st']["avatar"] = avatars[current_avatar]
                first_n = input_text
                first_s = score
                first_a = avatars[current_avatar]
            elif first_n == "":
                first_n = input_text
                first_s = score
                first_a = avatars[current_avatar]
            elif score > second_s: 
                high_scores[game_type][game_mode]['2nd']["name"] = input_text
                high_scores[game_type][game_mode]['2nd']["s"] = score
                high_scores[game_type][game_mode]['2nd']["avatar"] = avatars[current_avatar]
                second_n = input_text
                second_s = score
                second_a = avatars[current_avatar]
            elif score > third_s: 
                high_scores[game_type][game_mode]['3rd']["name"] = input_text
                high_scores[game_type][game_mode]['3rd']["s"] = score
                high_scores[game_type][game_mode]['3rd']["avatar"] = avatars[current_avatar]
                third_n = input_text
                third_s = score
                third_a = avatars[current_avatar]
            processedScore = True
    
    elif game_type == 'pipes' or game_type == 'pisa' or game_type=='pisabal':

        first_n = high_scores[game_type][game_mode][game_difficulty]['1st']["name"]
        second_n =  high_scores[game_type][game_mode][game_difficulty]['2nd']["name"]
        third_n =  high_scores[game_type][game_mode][game_difficulty]['3rd']["name"]
        first_s = high_scores[game_type][game_mode][game_difficulty]['1st']["s"]
        second_s =  high_scores[game_type][game_mode][game_difficulty]['2nd']["s"]
        third_s =  high_scores[game_type][game_mode][game_difficulty]['3rd']["s"]
        try: 
            first_a = high_scores[game_type][game_mode][game_difficulty]['1st']["avatar"]
        except: first_a = None
        try:
            second_a =  high_scores[game_type][game_mode][game_difficulty]['2nd']["avatar"]
        except: second_a = None
        try:
            third_a =  high_scores[game_type][game_mode][game_difficulty]['3rd']["avatar"]
        except: third_a = None

        if not processedScore:
            if score > first_s: 


                high_scores[game_type][game_mode][game_difficulty]['3rd']["name"] = second_n
                high_scores[game_type][game_mode][game_difficulty]['3rd']["s"] = second_s
                high_scores[game_type][game_mode][game_difficulty]['3rd']["avatar"] = second_a
                third_n = second_n
                third_s = second_s
                third_a = second_a

                high_scores[game_type][game_mode][game_difficulty]['2nd']["name"] = first_n
                high_scores[game_type][game_mode][game_difficulty]['2nd']["s"] = first_s
                high_scores[game_type][game_mode][game_difficulty]['2nd']["avatar"] = first_a
                second_n = first_n
                second_s = first_s
                second_a = first_a


                high_scores[game_type][game_mode][game_difficulty]['1st']["name"] = input_text
                high_scores[game_type][game_mode][game_difficulty]['1st']["s"] = score
                high_scores[game_type][game_mode][game_difficulty]['1st']["avatar"] = avatars[current_avatar]
                first_n = input_text
                first_s = score
                first_a = avatars[current_avatar]

            elif first_n == "":
                first_n = input_text
                first_s = score
                first_a = avatars[current_avatar]
            elif score > second_s: 

                high_scores[game_type][game_mode][game_difficulty]['3rd']["name"] = second_n
                high_scores[game_type][game_mode][game_difficulty]['3rd']["s"] = second_s
                high_scores[game_type][game_mode][game_difficulty]['3rd']["avatar"] = second_a
                third_n = second_n
                third_s = second_s
                third_a = second_a

                high_scores[game_type][game_mode][game_difficulty]['2nd']["name"] = input_text
                high_scores[game_type][game_mode][game_difficulty]['2nd']["s"] = score
                high_scores[game_type][game_mode][game_difficulty]['2nd']["avatar"] = avatars[current_avatar]
                second_n = input_text
                second_s = score
                second_a = avatars[current_avatar]
            elif score > third_s: 
                high_scores[game_type][game_mode][game_difficulty]['3rd']["name"] = input_text
                high_scores[game_type][game_mode][game_difficulty]['3rd']["s"] = score
                high_scores[game_type][game_mode][game_difficulty]['3rd']["avatar"] = avatars[current_avatar]
                third_n = input_text
                third_s = score
                third_a = avatars[current_avatar]
            processedScore = True
    
    fn = font.render(first_n,True,GOLD_COLOR)
    fs = font.render(str(first_s),True,GOLD_COLOR)
    sn = font.render(second_n,True,SILVER_COLOR)
    ss = font.render(str(second_s),True,SILVER_COLOR)
    tn = font.render(third_n,True,BRONZ_COLOR)
    ts = font.render(str(third_s),True,BRONZ_COLOR)
    if first_a:
        fa = pygame.image.load(first_a)
        fa = pygame.transform.scale(fa,(64,64))
    if second_a:
        sa = pygame.image.load(second_a)
        sa = pygame.transform.scale(sa,(64,64))
    if third_a:
        ta = pygame.image.load(third_a)
        ta = pygame.transform.scale(ta,(64,64))
    p_text = font.render('Player', True, (30,30,30))
    s_text = font.render('Score',True,(30,30,30))

    

    SCREEN.blit(p_text,(SCREENWIDTH//2-p_text.get_width()-text_offset,SCREENHEIGHT * text_start_height))

    SCREEN.blit(s_text,(SCREENWIDTH//2+text_offset,SCREENHEIGHT * text_start_height))
    
    SCREEN.blit(fn,(SCREENWIDTH//2-fn.get_width()-text_offset,SCREENHEIGHT * text_start_height + p_text.get_height() + 10))
    SCREEN.blit(fs,(SCREENWIDTH//2+text_offset + s_text.get_width()//2 - fs.get_width()//2,SCREENHEIGHT *  text_start_height+ s_text.get_height()+10))
    if first_a:
        SCREEN.blit(fa, (SCREENWIDTH//2-fn.get_width()-text_offset - fa.get_width() - 10,SCREENHEIGHT * text_start_height + p_text.get_height()))
    if second_a:
        SCREEN.blit(sn,(SCREENWIDTH//2-sn.get_width()-text_offset,SCREENHEIGHT * text_start_height + p_text.get_height() + fn.get_height() + 40))
        SCREEN.blit(ss,(SCREENWIDTH//2+text_offset+ s_text.get_width()//2 - ss.get_width()//2,SCREENHEIGHT * text_start_height + s_text.get_height() + fs.get_height()+40))
        SCREEN.blit(sa,(SCREENWIDTH//2-sn.get_width()-text_offset - sa.get_width() - 10,SCREENHEIGHT * text_start_height + p_text.get_height() + 40 + fn.get_height() ))
    if third_a: 
        SCREEN.blit(tn,(SCREENWIDTH//2-tn.get_width()-text_offset,SCREENHEIGHT * text_start_height+ p_text.get_height() + sn.get_height() + fn.get_height()+60))
        SCREEN.blit(ts,(SCREENWIDTH//2+text_offset+ s_text.get_width()//2 - ts.get_width()//2,SCREENHEIGHT * text_start_height + s_text.get_height()+ ss.get_height()+fs.get_height()+60))
        SCREEN.blit(ta,(SCREENWIDTH//2-tn.get_width()-text_offset - ta.get_width() -10,SCREENHEIGHT * text_start_height+ p_text.get_height() + sn.get_height()+60 + fn.get_height()))
    
    your_score = font.render("Your Score: {}".format(score),True,(0,255,0))
    SCREEN.blit(your_score,(SCREENWIDTH//2-your_score.get_width()//2,SCREENHEIGHT * text_start_height +  s_text.get_height() + ss.get_height()+fs.get_height() + ts.get_height() + 80))

    return processedScore

def newHighScore(score,events):
    global NEW_HIGH_SCORE,font,high_scores,input_text

    game_mode = get_game_mode()
    game_type = get_game_type()
    game_difficulty = get_game_difficulty()

    if game_type == 'stars':
        prev_name = font.render(high_scores[game_type][game_mode]["name"], True, (0, 0, 0))
        prev_score = high_scores[game_type][game_mode]["s"]
    elif game_type == 'pipes':
        prev_name = font.render(high_scores[game_type][game_mode][game_difficulty]["name"], True, (0, 0, 0))
        prev_score = high_scores[game_type][game_mode][game_difficulty]["s"]

    scoreDigits = [int(x) for x in list(str(prev_score))]
    totalWidth = 0  # total width of all numbers to be printed
    for digit in scoreDigits:
        totalWidth += IMAGES['numbers'][digit].get_width()

    scoreDigitsNew = [int(x) for x in list(str(score))]
    totalWidthNew = 0  # total width of all numbers to be printed
    for digit in scoreDigitsNew:
        totalWidthNew += IMAGES['numbers'][digit].get_width()

    

    for event in events:
        if event.type == KEYDOWN:
            if event.key == K_BACKSPACE:
                if len(input_text>0):
                    input_text = input_text[:-1]
            else:
                input_text += event.unicode

    SCREEN.blit(IMAGES['new_hs'], (int(SCREENWIDTH // 2) - IMAGES['new_hs'].get_width() // 2, SCREENHEIGHT * 0.2))

    Xoffset = (SCREENWIDTH - totalWidthNew) / 2
    for digit in scoreDigitsNew:
        SCREEN.blit(IMAGES['numbers'][digit], (Xoffset, SCREENHEIGHT * 0.2 + IMAGES['new_hs'].get_height() + 10))
        Xoffset += IMAGES['numbers'][digit].get_width()

    SCREEN.blit(IMAGES['prev'], (int(SCREENWIDTH // 2) - IMAGES['prev'].get_width() // 2,
                                    SCREENHEIGHT * 0.2 + IMAGES['new_hs'].get_height() + 10 + IMAGES['numbersg'][0].get_height() + 10))

    Xoffset = (SCREENWIDTH - totalWidth) / 2
    for digit in scoreDigits:
        SCREEN.blit(IMAGES['numbers'][digit], (Xoffset, SCREENHEIGHT * 0.2 + IMAGES['new_hs'].get_height() + 10 + IMAGES['numbersg'][0].get_height() + 10 + IMAGES['prev'].get_height() + 10))
        Xoffset += IMAGES['numbers'][digit].get_width()

    prev_n_x = int(SCREENWIDTH // 2) - prev_name.get_width() // 2
    prev_n_y = SCREENHEIGHT * 0.2 + IMAGES['new_hs'].get_height() + 10 + IMAGES['numbersg'][0].get_height() + 10 + IMAGES['prev'].get_height() + 10 + IMAGES['numbersg'][0].get_height() + 15
    SCREEN.blit(prev_name, (prev_n_x, prev_n_y))

    
    input_text_surface = font.render(input_text, True, (0, 0, 0))
    prev_n_x = int(SCREENWIDTH // 2) - input_text_surface.get_width() // 2
    prev_n_y = SCREENHEIGHT * 0.2 + IMAGES['new_hs'].get_height() + 10 + IMAGES['numbersg'][0].get_height() + 10 + IMAGES['prev'].get_height() + 10 + IMAGES['numbersg'][0].get_height() + 15+ prev_name.get_height() + 10
    SCREEN.blit(input_text_surface, (prev_n_x,prev_n_y  ))

def checkCollision(stars,playerMidPos):
   global big_star_w,big_star_h,star_w,star_h
   
   for j,i in enumerate(stars):
      
      if i['b']:
         
         x0 = i['x']
         x1 = i['x'] + big_star_w
         y0 = i['y']
         y1 = i['y'] + big_star_h
         
         if playerMidPos[0]<x1 and playerMidPos[0]>x0 and playerMidPos[1]<y1 and playerMidPos[1]>y0:
            return -j-1
      else:
         x0 = i['x']
         x1 = i['x'] + star_w
         y0 = i['y']
         y1 = i['y'] + star_h
         
         if playerMidPos[0]<x1 and playerMidPos[0]>x0 and playerMidPos[1]<y1 and playerMidPos[1]>y0:
            return j
   return -100

def checkCrash(playerMidPos, upperPipes, lowerPipes):

    global HEARTS,CRASHED,CRASHED_TIME
    #print('HEARTS',HEARTS)
    if CRASHED: return False
    """ 
        # if player crashes into ground
        if playerMidPos[1] + IMAGES['player'][0].get_height() >= SCREENHEIGHT - IMAGES['base'].get_height() - IMAGES['player'][0].get_height():
        if HEARTS:
            HEARTS -= 1
            CRASHED = True
            CRASHED_TIME = time.time()
            print('crash base')
            return False
            
        return True """
    
    for i in range(len(upperPipes)):
        x0 = upperPipes[i]['x'] - 2
        x1 = upperPipes[i]['x'] + IMAGES['pipe'][0].get_width() + 2
        y0 = upperPipes[i]['y'] - 2 
        y1 = upperPipes[i]['y'] + IMAGES['pipe'][0].get_height() +2
        
        #crash by right
        if (playerMidPos[0]+IMAGES['player'][0].get_width()<x1 and playerMidPos[0]+IMAGES['player'][0].get_width() >x0 and 
            playerMidPos[1] +IMAGES['player'][0].get_height()<y1 and playerMidPos[1] >y0):
            if HEARTS>0:
                HEARTS -= 1
                CRASHED = True
                CRASHED_TIME = time.time()
                upperPipes[i]['crashed'] = True

                print('crash pipe')
                return False
            return True
        #crash by top
        elif (playerMidPos[0]+IMAGES['player'][0].get_width()/2<x1 and playerMidPos[0]+IMAGES['player'][0].get_width()/2 >x0 and 
            playerMidPos[1]<y1 and playerMidPos[1] >y0):
            if HEARTS>0:
                HEARTS -= 1
                CRASHED = True
                CRASHED_TIME = time.time()
                upperPipes[i]['crashed'] = True
                print('crash pipe')
                return False
            return True
        #crash by bottom
        elif (playerMidPos[0]+IMAGES['player'][0].get_width()/2<x1 and playerMidPos[0]+IMAGES['player'][0].get_width()/2 >x0 and 
            playerMidPos[1]+IMAGES['player'][0].get_height()<y1 and playerMidPos[1]+IMAGES['player'][0].get_height() >y0):
            if HEARTS>0:
                HEARTS -= 1
                CRASHED = True
                CRASHED_TIME = time.time()
                upperPipes[i]['crashed'] = True
                print('crash pipe')
                return False
            return True
        
        x0 = lowerPipes[i]['x'] -2 
        x1 = lowerPipes[i]['x'] + IMAGES['pipe'][0].get_width() + 2
        y0 = lowerPipes[i]['y'] - 2
        y1 = lowerPipes[i]['y'] + IMAGES['pipe'][0].get_height() + 2
        
        #crash by right
        if (playerMidPos[0]+IMAGES['player'][0].get_width()<x1 and playerMidPos[0]+IMAGES['player'][0].get_width() >x0 and 
            playerMidPos[1] +IMAGES['player'][0].get_height()<y1 and playerMidPos[1] >y0):
            if HEARTS>0:
                HEARTS -= 1
                CRASHED = True
                CRASHED_TIME = time.time()
                lowerPipes[i]['crashed'] = True
                print('crash pipe')
                return False
            return True
        #crash by top
        elif (playerMidPos[0]+IMAGES['player'][0].get_width()/2<x1 and playerMidPos[0]+IMAGES['player'][0].get_width()/2 >x0 and 
            playerMidPos[1]<y1 and playerMidPos[1] >y0):
            if HEARTS>0:
                HEARTS -= 1
                CRASHED = True
                print('crash pipe')
                lowerPipes[i]['crashed'] = True
                return False
            return True
        #crash by bottom
        elif (playerMidPos[0]+IMAGES['player'][0].get_width()/2<x1 and playerMidPos[0]+IMAGES['player'][0].get_width()/2 >x0 and 
            playerMidPos[1]+IMAGES['player'][0].get_height()<y1 and playerMidPos[1]+IMAGES['player'][0].get_height() >y0):
            if HEARTS>0:
                HEARTS -= 1
                CRASHED = True
                CRASHED_TIME = time.time()
                lowerPipes[i]['crashed'] = True
                print('crash pipe')
                return False
            return True
    return False 

def pixelCollision(rect1, rect2, hitmask1, hitmask2):
    """Checks if two objects collide and not just their rects"""
    rect = rect1.clip(rect2)

    if rect.width == 0 or rect.height == 0:
        return False

    x1, y1 = rect.x - rect1.x, rect.y - rect1.y
    x2, y2 = rect.x - rect2.x, rect.y - rect2.y

    for x in range(rect.width):
        for y in range(rect.height):
            if hitmask1[x1+x][y1+y] and hitmask2[x2+x][y2+y]:
                return True
    return False

def getHitmask(image):
    """returns a hitmask using an image's alpha."""
    mask = []
    for x in range(image.get_width()):
        mask.append([])
        for y in range(image.get_height()):
            mask[x].append(bool(image.get_at((x,y))[3]))
    return mask

def read_high_scores(file_path):
    with open(file_path, 'r') as file:
        high_scores = json.load(file)
    return high_scores

def update_high_score(input_text, score):
    game_mode = get_game_mode()
    game_type = get_game_type()
    game_difficulty = get_game_difficulty()
    if game_type == "stars":
        high_scores[game_type][game_mode]["s"] = score
        high_scores[game_type][game_mode]["name"] = input_text
    elif game_type == "pipes":
        high_scores[game_type][game_mode][game_difficulty]["s"] = score
        high_scores[game_type][game_mode][game_difficulty]["name"] = input_text

    write_high_scores()

def write_high_scores():
    global file_path,high_scores
    with open(file_path, 'w') as file:
        json.dump(high_scores, file)

def removeOutliers(data):
    if data:
        sorted_data = sorted(data)
        q1, q3 = np.percentile(sorted_data, [25, 75])
        iqr = q3 - q1
        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr
        return [x for x in sorted_data if lower_bound <= x <= upper_bound]
    return data

def configureSmile():
    global landmark,video_capture,landmark_list, HOPPED,min_smile,max_smile,FPS

    dt = FPSCLOCK.tick(FPS)
    playerIndex = 0
    playery = int(SCREENHEIGHT*0.5)
    playerIndexGen = cycle([0, 1, 2, 1])
    iterloop = 0
    
    baseVelx = -0.20 #128
    
    
    playerVelY = 0 
    playerAccY = 0.5
    playerMinAcc = -0.5
    maxAngle = 40
    minAngle = -15
    descentSpeed = _set_descent_speed
    max_acc = _set_max_acc
    min_acc = 0.25

    smileConst = 1

    
    landmark_list = []
    smileConst = 1

    
    temp = True
    while temp:
        
        dt = FPSCLOCK.tick(FPS)

        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                temp = False
    
        setBG(video_capture.frame)

        
         
        if not HOPPED:
            if landmark.smile_level > -1 * (min_smile*1.2)//1 * -1:
                """ mag = (landmark.smile_level - min_smile) * (max_acc - min_acc) / (max_smile - min_smile)  + min_acc
                if mag > max_acc or landmark.smile_level>=max_smile*0.85 : mag = max_acc
                if mag < min_acc: mag = min_acc
                playerVelY = mag * smileConst """

                playerVelY = max_acc
                if not NOSOUND: SOUNDS['wing'].play()
                HOPPED = True
        elif landmark.smile_level<=-1*(min_smile*1.2)//1*-1 and HOPPED:
            HOPPED = False


        if playerVelY >= 0:
            if playery > IMAGES['player'][playerIndex].get_height()/2:
                playery -= playerVelY * dt
            else: playerVelY = 0
        if playerVelY<0:
            if playery < SCREENHEIGHT - IMAGES['base'].get_height() - IMAGES['player'][playerIndex].get_height() *2 :
                playery -= playerVelY * dt
        if playerVelY > playerMinAcc:
            playerVelY -= descentSpeed
        
        rotation = (playerVelY - playerMinAcc) * (maxAngle - minAngle) / (playerAccY -playerMinAcc)  +minAngle
        

        if landmark.smile_level != -1:
            landmark_list.append(landmark.smile_level)
        

        text_surface = font.render(str(landmark.smile_level), True, (255, 0, 0))
        SCREEN.blit(text_surface,(SCREENWIDTH//2-text_surface.get_width()//2, SCREENHEIGHT * 0.2 ))
        SCREEN.blit(IMAGES['configure'],(SCREENWIDTH//2-IMAGES['configure'].get_width()//2, SCREENHEIGHT * 0.2 + text_surface.get_height() + 10 ))
        playerSurface = pygame.transform.rotate(IMAGES['player'][playerIndex], rotation)
        SCREEN.blit(playerSurface, (int(SCREENWIDTH*0.2), playery))
        
        if iterloop %5 == 0:
            playerIndex = next(playerIndexGen)
            
        iterloop = (iterloop + 1) % 30      
        
        if BASES_LIST[0]['x'] + IMAGES['base'].get_width()<=0:
            BASES_LIST.pop(0)

        if len(BASES_LIST)<3:
            BASES_LIST.append({'x':BASES_LIST[-1]['x']+IMAGES['base'].get_width(),'y':SCREENHEIGHT*0.1})
        for base in BASES_LIST:
            base['x'] += baseVelx
            SCREEN.blit(IMAGES['base'],(base['x'],int(SCREENHEIGHT-IMAGES['base'].get_height())))


        sub_list = removeOutliers(landmark_list)

        t = sub_list[:int(len(sub_list)*0.1)]

        try:
            min_smile = np.sum(t) / len(t)
        except:
            try: 
                min_smile = sub_list[0]
            except:
                min_smile = 6
        
        t = sub_list[int(len(sub_list)*0.9):]
        try:
            max_smile = np.sum(t) / len(t)
        except:
            try: 
                max_smile = sub_list[-1]
            except:
                max_smile = 25
        
            
        
        
        pygame.display.update()
    
    landmark.configured = True
    print(min_smile,max_smile)

def setName():
    global base,input_text, nameSet,current_avatar,avatars
    avatar_image = pygame.image.load(avatars[current_avatar])
    avatar_image = pygame.transform.scale(avatar_image,(256,256))
    iw, ih = avatar_image.get_rect().size
    next_rect = next_avatar.get_rect()
    next_rect.x = SCREENWIDTH//2+iw//2 - next_avatar.get_width()
    next_rect.y = SCREENHEIGHT * 0.2  + ih + 5
    prev_rect = prev_avatar.get_rect()
    prev_rect.x = SCREENWIDTH//2-iw//2
    prev_rect.y = SCREENHEIGHT * 0.2  + ih + 5
    temp = True
    cameraOn = False
    while temp:

        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and (event.key == K_ESCAPE or event.key==K_RETURN)):
                temp = False
                if cameraOn:
                    d = datetime.datetime.now()
                    cv.imwrite(f"./assets/avatars/{d.hour}{d.minute}{d.second}.jpg",video_capture.frame)
                    avatars = sorted(glob.glob("./assets/avatars/*.jpg"))
                    save_last_player(input_text,f"./assets/avatars/{d.hour}{d.minute}{d.second}.jpg")
                else:
                    save_last_player(input_text,avatars[current_avatar])
            elif event.type == KEYDOWN:
                if event.key == K_BACKSPACE:
                    if len(input_text)>0:
                        input_text = input_text[:-1]
                else:
                    input_text += event.unicode
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    mpos = pygame.mouse.get_pos()
                    # Use event.pos or pg.mouse.get_pos().
                    if next_rect.collidepoint(mpos):
                        if current_avatar < len(avatars)-2: 
                            current_avatar += 1
                            cameraOn = False
                        elif current_avatar == len(avatars)-2 and not cameraOn:
                            current_avatar += 1
                            cameraOn = True
                        else: 
                            cameraOn = False
                            current_avatar =0 
                    elif prev_rect.collidepoint(mpos):
                        if current_avatar>0:current_avatar-=1
                        else: current_avatar = len(avatars)-1
        setBG(video_capture.frame)

        if cameraOn:
            bg = cv.resize(video_capture.frame,(256,256))
            bg = cv.cvtColor(bg,cv.COLOR_BGR2RGB)
            #bg = pygame.image.frombuffer(bg.tostring(), bg.shape[1::-1], "BGR")
            bg = pygame.surfarray.make_surface(bg)
            bg = pygame.transform.rotate(bg, -90)
            SCREEN.blit(bg,(SCREENWIDTH//2- avatar_image.get_width()//2,SCREENHEIGHT * 0.2))
        else:
            avatar_image = pygame.image.load(avatars[current_avatar])
            avatar_image = pygame.transform.scale(avatar_image,(256,256))
            iw, ih = avatar_image.get_rect().size
            SCREEN.blit(avatar_image,(SCREENWIDTH//2- avatar_image.get_width()//2,SCREENHEIGHT * 0.2))
        SCREEN.blit(prev_avatar,(SCREENWIDTH//2-iw//2, SCREENHEIGHT * 0.2  + ih + 5 ))
        SCREEN.blit(next_avatar,(SCREENWIDTH//2+iw//2 - next_avatar.get_width(),SCREENHEIGHT * 0.2  + ih + 5 ))


        text_surface0 = font.render('Enter Name:',True,(0,255,0))
        SCREEN.blit(text_surface0,(SCREENWIDTH//2-text_surface0.get_width()- 20 ,SCREENHEIGHT * 0.2  + avatar_image.get_height() + 60))
        text_surface = font.render(input_text, True, (30, 30,30))
        SCREEN.blit(text_surface,(SCREENWIDTH//2, SCREENHEIGHT * 0.2 + avatar_image.get_height() + 60 ))
        SCREEN.blit(IMAGES['base'],(0,int(SCREENHEIGHT-IMAGES['base'].get_height())))
        FPSCLOCK.tick(FPS)
        pygame.display.update()

    
    nameSet = True

def save_last_player(player_name, avatar_file):
    with open('last_player.txt', 'w') as f:
        # write the player's name and avatar file to the text file
        f.write(f'{player_name}\n')
        f.write(f'{avatar_file}\n')

def get_last_player():
    with open('last_player.txt', 'r') as f:
        player = f.readline().strip()
        avatar = f.readline().strip()

    return player,avatar        

def update_dict(dict,key):
        for k in dict.keys():
            if k == key:
                dict[k] = True
            else:
                dict[k] = False
                
def get_game_type():
    global GAME_TYPE
    return next((key for key, value in GAME_TYPE.items() if value), None)

def get_game_mode():
    global GAME_MODES
    return next((key for key, value in GAME_MODES.items() if value), None)

def get_game_difficulty():
    global GAME_DIFFICULTY
    return next((key for key, value in GAME_DIFFICULTY.items() if value), None)

def next_level(level):
    global video_capture,font,font2
    temp = True
    cameraOn = False
    
    while temp:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and (event.key == K_ESCAPE)):
                return False
            elif event.type == KEYDOWN and event.key == K_RETURN:
                return True

        setBG(video_capture.frame)


        if level == 'pipes':
            text1 = "Welcome!"
            text2 = "This is the first level of the game."
            text3 = "Try to avoid the pipes by smiling!"
        elif level == 'stars':
            text1 = "Cool!"
            text2 = "You have reached the stars stage."
            text3 = "Now try to collect stars by smiling!"
        elif level == 'balloons':
            print('here')
            text1 = "Awesome!"
            text2= "You have reached the balloons stage."
            text3 = "Shoot the red balloons by similing. Move the birdy up and down with arrow keys!"
        elif level == 'pisa':
            text1 = 'Great!'
            text2 = "You have reached the Pipes and Stars stage."
            text3 = "Try to avoid pipes and collect stars by smiling!"
        elif level == 'pisabal':
            text1 = 'G-R-E-A-T!!!!'
            text2 = "You have reached the final level!"
            text3 = "Avoid pipes and collect stars with SPACE key and shoot the red balloons by smiling!"
        elif level =='finished':
            text1 = 'Congratulations!'
            text2 = "You have finished the game!"
            text3 = "Dont forget to come and play again!"
            
        text_surface1 = font2.render(text1,True,(0,255,0))
        text_surface2 = font2.render(text2,True,(0,255,0))
        text_surface3 = font2.render(text3,True,(0,255,0))
        SCREEN.blit(text_surface1,(SCREENWIDTH//2-text_surface1.get_width()//2,SCREENHEIGHT * 0.2 ))
        SCREEN.blit(text_surface2,(SCREENWIDTH//2-text_surface2.get_width()//2,SCREENHEIGHT * 0.2 + text_surface1.get_height() + 10 ))
        SCREEN.blit(text_surface3,(SCREENWIDTH//2-text_surface3.get_width()//2,SCREENHEIGHT * 0.2 + text_surface1.get_height() + text_surface2.get_height() + 20 ))
        
        enter_text = font2.render('Press Enter to continue', True, (0, 255, 0))
        SCREEN.blit(enter_text,(SCREENWIDTH//2-enter_text.get_width()//2,SCREENHEIGHT * 0.2 + text_surface1.get_height() + text_surface2.get_height() + text_surface3.get_height() + 60 ))
        
        SCREEN.blit(IMAGES['base'],(0,int(SCREENHEIGHT-IMAGES['base'].get_height())))
        FPSCLOCK.tick(FPS)
        pygame.display.update()


def session_ending(score):
    global video_capture,font,font2
    temp = True
    
    while temp:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and (event.key == K_ESCAPE)):
                return False
            elif event.type == KEYDOWN and event.key == K_RETURN:
                return True

        setBG(video_capture.frame)

        if score > 20:
            text0 = str(score)
            text1 = "Congratulations!"
            text2 = "You did GREAT!"
            text3 = "Dont forget to come and play again!"
            
            text_surface0 = font.render(text0,True,(0,255,0)) 
            text_surface1 = font2.render(text1,True,(0,255,0))
            text_surface2 = font2.render(text2,True,(0,255,0))
            text_surface3 = font2.render(text3,True,(0,255,0))
            
            SCREEN.blit(text_surface0,(SCREENWIDTH//2-text_surface0.get_width()//2,SCREENHEIGHT * 0.2 ))
            SCREEN.blit(text_surface1,(SCREENWIDTH//2-text_surface1.get_width()//2,SCREENHEIGHT * 0.2 + text_surface0.get_height() + 10 ))
            SCREEN.blit(text_surface2,(SCREENWIDTH//2-text_surface2.get_width()//2,SCREENHEIGHT * 0.2 + text_surface0.get_height() + text_surface1.get_height() + 20 ))
            SCREEN.blit(text_surface3,(SCREENWIDTH//2-text_surface3.get_width()//2,SCREENHEIGHT * 0.2 + text_surface0.get_height() + text_surface1.get_height() + text_surface2.get_height() + 30 ))

            enter_text = font2.render('Press Enter to continue', True, (0, 255, 0))
            SCREEN.blit(enter_text,(SCREENWIDTH//2-enter_text.get_width()//2,SCREENHEIGHT * 0.2 + text_surface0.get_height()+ text_surface1.get_height() + text_surface2.get_height() + text_surface3.get_height() + 60 ))
        


        elif score>10:
            text0 = str(score)
            text1 = "Well done!"
            text2 = "You have potential!"
            text3 = "Dont forget to come and play again."
            
            text_surface0 = font.render(text0,True,(0,255,0)) 
            text_surface1 = font2.render(text1,True,(0,255,0))
            text_surface2 = font2.render(text2,True,(0,255,0))
            text_surface3 = font2.render(text3,True,(0,255,0))
            
            SCREEN.blit(text_surface0,(SCREENWIDTH//2-text_surface0.get_width()//2,SCREENHEIGHT * 0.2 ))
            SCREEN.blit(text_surface1,(SCREENWIDTH//2-text_surface1.get_width()//2,SCREENHEIGHT * 0.2 + text_surface0.get_height() + 10 ))
            SCREEN.blit(text_surface2,(SCREENWIDTH//2-text_surface2.get_width()//2,SCREENHEIGHT * 0.2 + text_surface0.get_height() + text_surface1.get_height() + 20 ))
            SCREEN.blit(text_surface3,(SCREENWIDTH//2-text_surface3.get_width()//2,SCREENHEIGHT * 0.2 + text_surface0.get_height() + text_surface1.get_height() + text_surface2.get_height() + 30 ))

            enter_text = font2.render('Press Enter to continue', True, (0, 255, 0))
            SCREEN.blit(enter_text,(SCREENWIDTH//2-enter_text.get_width()//2,SCREENHEIGHT * 0.2 + text_surface0.get_height()+ text_surface1.get_height() + text_surface2.get_height() + text_surface3.get_height() + 60 ))
        

        else:
            #text0 = str(score)
            text1 = "Great Start!"
            text2 = "Practice makes perfect."
            text3 = "Dont forget to come and play again."
            
            #text_surface0 = font.render(text0,True,(0,255,0)) 
            text_surface1 = font2.render(text1,True,(0,255,0))
            text_surface2 = font2.render(text2,True,(0,255,0))
            text_surface3 = font2.render(text3,True,(0,255,0))
            
            #SCREEN.blit(text_surface0,(SCREENWIDTH//2-text_surface0.get_width()//2,SCREENHEIGHT * 0.2 ))
            SCREEN.blit(text_surface1,(SCREENWIDTH//2-text_surface1.get_width()//2,SCREENHEIGHT * 0.2  ))
            SCREEN.blit(text_surface2,(SCREENWIDTH//2-text_surface2.get_width()//2,SCREENHEIGHT * 0.2 +  text_surface1.get_height() + 10 ))
            SCREEN.blit(text_surface3,(SCREENWIDTH//2-text_surface3.get_width()//2,SCREENHEIGHT * 0.2 +  text_surface1.get_height() + text_surface2.get_height() + 20 ))

            enter_text = font2.render('Press Enter to continue', True, (0, 255, 0))
            SCREEN.blit(enter_text,(SCREENWIDTH//2-enter_text.get_width()//2,SCREENHEIGHT * 0.2  + text_surface1.get_height() + text_surface2.get_height() + text_surface3.get_height() + 60 ))
        

        
        SCREEN.blit(IMAGES['base'],(0,int(SCREENHEIGHT-IMAGES['base'].get_height())))
        FPSCLOCK.tick(FPS)
        pygame.display.update()
if __name__ == '__main__':
    main()
