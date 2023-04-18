
from itertools import cycle
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

FPS = 30
SCREENWIDTH  = 1280
SCREENHEIGHT = 720

PIPEGAPSIZE  = 330 

BASEY = SCREENHEIGHT * 0.79



REF_WIDTH = 1280
REF_HEIGHT = 720
DEFAULT_BG_SIZE = (REF_WIDTH,REF_HEIGHT)


x_scale = SCREENWIDTH / REF_WIDTH
y_scale = SCREENHEIGHT / REF_HEIGHT
size_scale = min(x_scale, y_scale)

min_smile = 8
max_smile = 32
mins_l = []
maxs_l = []
landmark_list = []
BIG_STAR = False

START = True
GAME_MODES = {"space":True,"smile":False,"altitude":False}
GAME_DIFFICULTY = {"easy":True,"medium":False,"hard":False,"arcade":False}
GAME_TYPE = {'pipes':True,'stars': False}
NEW_HIGH_SCORE = False
gm = "space"
gt = "pipes"
gd = "easy"
input_text = 'Enter Your Name'
LANDMARKS = False
FX = False
HOPPED = False
PIPE_OFFSET = 100
PIPE_OFFSET_ = PIPE_OFFSET
IMAGES, SOUNDS, HITMASKS = {}, {}, {}
file_path = "scores.json"
BASES_LIST = []
PLAYERS_LIST = (
    # red bird
    (
        'assets/sprites/redbird-upflap.png',
        'assets/sprites/redbird-midflap.png',
        'assets/sprites/redbird-downflap.png',
    ),
    # blue bird
    (
        'assets/sprites/bluebird-upflap.png',
        'assets/sprites/bluebird-midflap.png',
        'assets/sprites/bluebird-downflap.png',
    ),
    # yellow bird
    (
        'assets/sprites/yellowbird-upflap.png',
        'assets/sprites/yellowbird-midflap.png',
        'assets/sprites/yellowbird-downflap.png',
    ),
)

# list of backgrounds
BACKGROUNDS_LIST = (
    'assets/sprites/background-day.png',
    'assets/sprites/background-night.png',
)

# list of pipes
PIPES_LIST = (
    'assets/sprites/pipe-green.png',
    'assets/sprites/pipe-red.png',
)

pygame.init()
pygame.font.init()
font = pygame.font.Font("assets/Minecraft.ttf", 48)
font = pygame.font.Font(pygame.font.get_default_font(), 42)

FPSCLOCK = pygame.time.Clock()
SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
pygame.display.set_caption('Flappy Bird')

# numbers sprites for score display
IMAGES['numbers'] = (
    pygame.image.load('assets/sprites/0.png').convert_alpha(),
    pygame.image.load('assets/sprites/1.png').convert_alpha(),
    pygame.image.load('assets/sprites/2.png').convert_alpha(),
    pygame.image.load('assets/sprites/3.png').convert_alpha(),
    pygame.image.load('assets/sprites/4.png').convert_alpha(),
    pygame.image.load('assets/sprites/5.png').convert_alpha(),
    pygame.image.load('assets/sprites/6.png').convert_alpha(),
    pygame.image.load('assets/sprites/7.png').convert_alpha(),
    pygame.image.load('assets/sprites/8.png').convert_alpha(),
    pygame.image.load('assets/sprites/9.png').convert_alpha()
)

IMAGES['numbersg'] = (
    pygame.image.load('assets/sprites/0g.png').convert_alpha(),
    pygame.image.load('assets/sprites/1g.png').convert_alpha(),
    pygame.image.load('assets/sprites/2g.png').convert_alpha(),
    pygame.image.load('assets/sprites/3g.png').convert_alpha(),
    pygame.image.load('assets/sprites/4g.png').convert_alpha(),
    pygame.image.load('assets/sprites/5g.png').convert_alpha(),
    pygame.image.load('assets/sprites/6g.png').convert_alpha(),
    pygame.image.load('assets/sprites/7g.png').convert_alpha(),
    pygame.image.load('assets/sprites/8g.png').convert_alpha(),
    pygame.image.load('assets/sprites/9g.png').convert_alpha()
)

scaled_images = [pygame.transform.scale(img, (int(img.get_width() * 0.85), int(img.get_height() * 0.85))) for img in IMAGES['numbersg']]
IMAGES['numbersg'] = tuple(scaled_images)

# game over sprite
IMAGES['gameover'] = pygame.image.load('assets/sprites/gameover.png').convert_alpha()

# message sprite for welcome screen
IMAGES['message'] = pygame.image.load('assets/sprites/welcome_v1.png').convert_alpha()
IMAGES['message'] = pygame.transform.scale(IMAGES['message'],(IMAGES['message'].get_width() * 0.7 , IMAGES['message'].get_height()*0.7))

IMAGES['message2'] = pygame.image.load('assets/sprites/press_space.png').convert_alpha()
IMAGES['message2'] = pygame.transform.scale(IMAGES['message2'],(IMAGES['message2'].get_width() * 1.2 , IMAGES['message2'].get_height()*1.2))


IMAGES['input'] = pygame.image.load('assets/sprites/input.png').convert_alpha()
IMAGES['input'] = pygame.transform.scale(IMAGES['input'],(IMAGES['input'].get_width() * 0.35 , IMAGES['input'].get_height()*0.35))

IMAGES['mode'] = pygame.image.load('assets/sprites/mode.png').convert_alpha()
IMAGES['mode'] = pygame.transform.scale(IMAGES['mode'],(IMAGES['mode'].get_width() * 0.35 , IMAGES['mode'].get_height()*0.35))

IMAGES['difficulty'] = pygame.image.load('assets/sprites/difficulty.png').convert_alpha()
IMAGES['difficulty'] = pygame.transform.scale(IMAGES['difficulty'],(IMAGES['difficulty'].get_width() * 0.35 , IMAGES['difficulty'].get_height()*0.35))

IMAGES['smile'] = pygame.image.load('assets/sprites/smile.png').convert_alpha()
IMAGES['smile'] = pygame.transform.scale(IMAGES['smile'],(IMAGES['smile'].get_width()*0.8,IMAGES['smile'].get_height()*0.8))
IMAGES['altitude'] = pygame.image.load('assets/sprites/altitude.png').convert_alpha()
IMAGES['altitude'] = pygame.transform.scale(IMAGES['altitude'],(IMAGES['altitude'].get_width()*0.8,IMAGES['altitude'].get_height()*0.8))
IMAGES['space'] = pygame.image.load('assets/sprites/space.png').convert_alpha()
IMAGES['space'] = pygame.transform.scale(IMAGES['space'],(IMAGES['space'].get_width()*0.8,IMAGES['space'].get_height()*0.8))
IMAGES['pipes_mode'] =  pygame.image.load('assets/sprites/mode_pipe.png').convert_alpha()
IMAGES['stars_mode'] =  pygame.image.load('assets/sprites/mode_stars.png').convert_alpha()
IMAGES['easy'] =  pygame.image.load('assets/sprites/easy.png').convert_alpha()
IMAGES['medium'] =  pygame.image.load('assets/sprites/medium.png').convert_alpha()
IMAGES['hard'] =  pygame.image.load('assets/sprites/hard.png').convert_alpha()
IMAGES['arcade'] =  pygame.image.load('assets/sprites/arcade.png').convert_alpha()

IMAGES['calibrate'] = pygame.image.load('assets/sprites/calibrate.png').convert_alpha()
IMAGES['calibrate'] = pygame.transform.scale(IMAGES['calibrate'],(IMAGES['calibrate'].get_width() * 0.3 , IMAGES['calibrate'].get_height()*0.3))

IMAGES['landmarks_on'] = pygame.image.load('assets/sprites/landmarks_on.png').convert_alpha()
IMAGES['landmarks_on'] = pygame.transform.scale(IMAGES['landmarks_on'],(IMAGES['landmarks_on'].get_width() * 0.3 , IMAGES['landmarks_on'].get_height()*0.3))
IMAGES['landmarks_off'] = pygame.image.load('assets/sprites/landmarks_off.png').convert_alpha()
IMAGES['landmarks_off'] = pygame.transform.scale(IMAGES['landmarks_off'],(IMAGES['landmarks_off'].get_width() * 0.3 , IMAGES['landmarks_off'].get_height()*0.3))
IMAGES['fx_on'] = pygame.image.load('assets/sprites/fx_on.png').convert_alpha()
IMAGES['fx_on'] = pygame.transform.scale(IMAGES['fx_on'],(IMAGES['fx_on'].get_width() * 0.3 , IMAGES['fx_on'].get_height()*0.3))
IMAGES['fx_off'] = pygame.image.load('assets/sprites/fx_off.png').convert_alpha()
IMAGES['fx_off'] = pygame.transform.scale(IMAGES['fx_off'],(IMAGES['fx_off'].get_width() * 0.3 , IMAGES['fx_off'].get_height()*0.3))

IMAGES['new_hs'] = pygame.image.load('assets/sprites/new_high_score.png').convert_alpha()

IMAGES['prev'] = pygame.image.load('assets/sprites/previous.png').convert_alpha()
IMAGES['prev'] = pygame.transform.scale(IMAGES['prev'],(IMAGES['prev'].get_width() * 0.8 , IMAGES['prev'].get_height()*0.8))

IMAGES['hs'] = pygame.image.load('assets/sprites/high_score.png').convert_alpha()

IMAGES['y_hs'] = pygame.image.load('assets/sprites/your_score.png').convert_alpha()

IMAGES['configure'] = pygame.image.load('assets/sprites/configure.png').convert_alpha()
IMAGES['configure'] = pygame.transform.scale(IMAGES['configure'],(IMAGES['configure'].get_width() * 0.8 , IMAGES['configure'].get_height()*0.8))

# base (ground) sprite
IMAGES['base'] = pygame.image.load('assets/sprites/base.png').convert_alpha()
IMAGES['base'] = pygame.transform.scale(IMAGES['base'],(SCREENWIDTH,SCREENHEIGHT*0.1))

_star_big = pygame.image.load('assets/sprites/star.png').convert_alpha()
_star = pygame.transform.scale(_star_big,(_star_big.get_width()/2,_star_big.get_height()/2))
IMAGES['star'] = _star
IMAGES['star_big'] = _star_big

HITMASKS['star'] = _star.get_rect()
HITMASKS['star_big'] = _star_big.get_rect()

# sounds
if 'win' in sys.platform:
    soundExt = '.wav'
else:
    soundExt = '.ogg'

SOUNDS['die']    = pygame.mixer.Sound('assets/audio/die' + soundExt)
SOUNDS['hit']    = pygame.mixer.Sound('assets/audio/hit' + soundExt)
SOUNDS['point']  = pygame.mixer.Sound('assets/audio/point' + soundExt)
SOUNDS['swoosh'] = pygame.mixer.Sound('assets/audio/swoosh' + soundExt)
SOUNDS['wing']   = pygame.mixer.Sound('assets/audio/wing' + soundExt)

wing = pygame.mixer.Channel(6)

messagex = int((SCREENWIDTH - IMAGES['message'].get_width()) / 2)
messagey = int(SCREENHEIGHT * 0.12)

input_options_pos = (int(SCREENWIDTH * 0.05)  - IMAGES['input'].get_width()//2, int(SCREENHEIGHT * 0.15))
check_img1 = pygame.image.load("assets/sprites/check1.png").convert_alpha()
check_img1 = pygame.transform.scale(check_img1,(check_img1.get_width() * 0.2 , check_img1.get_height()*0.2))
check_img0 = pygame.image.load("assets/sprites/check0.png").convert_alpha()
check_img0 = pygame.transform.scale(check_img0,(check_img0.get_width() * 0.2 , check_img0.get_height()*0.2))

space_option = button.Button(input_options_pos[0],    input_options_pos[1]+ IMAGES['input'].get_height() + 10 + (check_img0.get_height() + 5 ) * 0    , check_img0, 1)
space_text_pos = (input_options_pos[0] + check_img0.get_width() + 5 ,input_options_pos[1]+ IMAGES['input'].get_height() + 10 +(check_img0.get_height() + 5 ) * 0+2)
smile_option = button.Button(input_options_pos[0], input_options_pos[1]+ IMAGES['input'].get_height() + 10 +(check_img0.get_height() + 5 ) * 1, check_img1, 1)
smile_text_pos = (input_options_pos[0] + check_img0.get_width() + 5,input_options_pos[1]+ IMAGES['input'].get_height() + 10 +(check_img0.get_height() + 5 ) * 1 +2)
altitude_option = button.Button(input_options_pos[0], input_options_pos[1]+ IMAGES['input'].get_height() + 10 +(check_img0.get_height() + 5 ) * 2, check_img1, 1)
altitude_text_pos = (input_options_pos[0] + check_img0.get_width() + 5,input_options_pos[1]+ IMAGES['input'].get_height() + 10 +(check_img0.get_height() + 5 ) * 2 + 3 )


mode_options_pos =(input_options_pos[0] + IMAGES['input'].get_width() + 45, input_options_pos[1])

check_img1_p = pygame.image.load("assets/sprites/check1_purp.png").convert_alpha()
check_img1_p = pygame.transform.scale(check_img1_p,(check_img1_p.get_width() * 0.2 , check_img1_p.get_height()*0.2))
check_img0_p = pygame.image.load("assets/sprites/check0_purp.png").convert_alpha()
check_img0_p = pygame.transform.scale(check_img0_p,(check_img0_p.get_width() * 0.2 , check_img0_p.get_height()*0.2))
pipes_option = button.Button(mode_options_pos[0],    mode_options_pos[1] + IMAGES['input'].get_height() + 10 + (check_img0_p.get_height() + 5 ) * 0, check_img0_p, 1)
pipes_text_pos = (mode_options_pos[0] + check_img0_p.get_width() + 5 ,mode_options_pos[1] + IMAGES['input'].get_height() + 10 +(check_img0_p.get_height() + 5 ) * 0+2)
stars_option = button.Button(mode_options_pos[0], mode_options_pos[1] + IMAGES['input'].get_height() + 10 +(check_img0_p.get_height() + 5 ) * 1, check_img1_p, 1)
stars_text_pos = (mode_options_pos[0] + check_img0_p.get_width() + 5,mode_options_pos[1] + IMAGES['input'].get_height() + 10 +(check_img0_p.get_height() + 5 ) * 1 +2)





check_img1_r = pygame.image.load("assets/sprites/check1_red.png").convert_alpha()
check_img1_r = pygame.transform.scale(check_img1_r,(check_img1_r.get_width() * 0.2 , check_img1_r.get_height()*0.2))
check_img0_r = pygame.image.load("assets/sprites/check0_red.png").convert_alpha()
check_img0_r = pygame.transform.scale(check_img0_r,(check_img0_r.get_width() * 0.2 , check_img0_r.get_height()*0.2))

easy_option_pos = (input_options_pos[0], altitude_text_pos[1] + IMAGES['difficulty'].get_height() *2 + 10  )

easy_option = button.Button(easy_option_pos[0],    easy_option_pos[1] + (check_img0_r.get_height() + 5 ) * 0, check_img0_r, 1)
easy_text_pos = (easy_option_pos[0] + check_img0_r.get_width() + 5 ,easy_option_pos[1] +(check_img0_r.get_height() + 5 ) * 0+2)
medium_option = button.Button(easy_option_pos[0], easy_option_pos[1] +(check_img0_r.get_height() + 5 ) * 1, check_img1_r, 1)
medium_text_pos = (easy_option_pos[0] + check_img0_r.get_width() + 5,easy_option_pos[1] +(check_img0_r.get_height() + 5 ) * 1 +2)

hard_option = button.Button(easy_option_pos[0] + check_img0.get_width() + IMAGES['medium'].get_width() + 40,
                             easy_option_pos[1] +(check_img0_r.get_height() + 5 ) * 0, check_img1_r, 1)
hard_text_pos = (easy_option_pos[0] + check_img0_r.get_width() + 5  + check_img0.get_width() + IMAGES['medium'].get_width() + 40,
                 easy_option_pos[1] +(check_img0_r.get_height() + 5 ) * 0 +2)
arcade_option = button.Button(easy_option_pos[0] + check_img0.get_width() + IMAGES['medium'].get_width() + 40,
                               easy_option_pos[1] +(check_img0_r.get_height() + 5 ) * 1, check_img1_r, 1)
arcade_text_pos = (easy_option_pos[0] + check_img0_r.get_width() + 5 + check_img0.get_width() + IMAGES['medium'].get_width() + 40,
                   easy_option_pos[1] +(check_img0_r.get_height() + 5 ) * 1 +2)

difficulty_options_pos =((easy_option.rect.topleft[0] + hard_option.rect.topleft[0] + check_img0.get_width())//2 - IMAGES['difficulty'].get_width()//2,
                          altitude_text_pos[1] + 45)





landmarks_option = button.Button(input_options_pos[0], arcade_text_pos[1] + IMAGES['arcade'].get_height() + 45  , IMAGES["landmarks_off"], 1)
fx_option = button.Button(input_options_pos[0] + IMAGES['landmarks_off'].get_width()//2 - IMAGES['fx_off'].get_width()//2 - 3,
                           arcade_text_pos[1] + IMAGES['arcade'].get_height() + 45 + IMAGES['landmarks_off'].get_height() + 10, IMAGES["fx_off"], 1)
calibrate_option = button.Button(landmarks_option.rect.topleft[0] + IMAGES['landmarks_off'].get_width() + 20,
                                 (landmarks_option.rect.topleft[1]+
                                   fx_option.rect.topleft[1] + IMAGES['fx_off'].get_height())//2 - IMAGES['calibrate'].get_height() //2
                                 , IMAGES["calibrate"], 1)


messagex2 = int((SCREENWIDTH - IMAGES['message2'].get_width()) / 2)
messagey2 = int(SCREENHEIGHT * 0.7)


video_capture = videocapture(0)
video_capture.start()
landmark = media(video_capture).start()
facemask = None#facemasks(video_capture).start()
high_scores = None

def main():
        # select random player sprites
    global BASES_LIST,NEW_HIGH_SCORE,high_scores,file_path,input_text,PIPEGAPSIZE
    randPlayer = random.randint(0, len(PLAYERS_LIST) - 1)
    IMAGES['player'] = (
        pygame.image.load(PLAYERS_LIST[randPlayer][0]).convert_alpha(),
        pygame.image.load(PLAYERS_LIST[randPlayer][1]).convert_alpha(),
        pygame.image.load(PLAYERS_LIST[randPlayer][2]).convert_alpha(),
    )
    # select random pipe sprites
    pipeindex = random.randint(0, len(PIPES_LIST) - 1)
    _pipe = pygame.image.load(PIPES_LIST[pipeindex]).convert_alpha()
    _pipe = pygame.transform.scale(_pipe,(_pipe.get_width(),(SCREENHEIGHT-50)))
    IMAGES['pipe'] = [
        pygame.transform.flip(_pipe, False, True),
        _pipe,
    ]
    # hitmask for pipes
    HITMASKS['pipe'] = (
        getHitmask(IMAGES['pipe'][0]),
        getHitmask(IMAGES['pipe'][1]),
    )

    # hitmask for player
    HITMASKS['player'] = (
        getHitmask(IMAGES['player'][0]),
        getHitmask(IMAGES['player'][1]),
        getHitmask(IMAGES['player'][2]),
    )
    for key in IMAGES.keys():
        try:
            for image in IMAGES[key]:
                image = pygame.transform.scale(image, (int(image.get_width() * x_scale ), int(image.get_height() * y_scale)))
        except:
            IMAGES[key] = pygame.transform.scale(IMAGES[key], (int(IMAGES[key].get_width() * x_scale ), int(IMAGES[key].get_height() * y_scale)))


    BASES_LIST = [{'x':0,'y':SCREENHEIGHT*0.1},
              {'x':IMAGES['base'].get_width(),'y':SCREENHEIGHT  * 0.1}]
    
    
    while True:

        if not landmark.configured:
            configureSmile()
        NEW_HIGH_SCORE = False
        input_text = 'Enter Your Name'
        high_scores = read_high_scores(file_path)
        showWelcomeAnimation()
        info = mainGame()
        if GAME_TYPE['pipes'] and info is not None:
            showGameOverScreen(info)


def showWelcomeAnimation():
    global START,PIPEGAPSIZE,GAME_DIFFICULTY,gm,gt,gd,GAME_MODES,LANDMARKS,FX
    START = True
    # index of player to blit on screen
    playerIndex = 0
    playerIndexGen = cycle([0, 1, 2, 1])
    # iterator used to change playerIndex after every 5th iteration
    iterloop = 0

    playerx = int(SCREENWIDTH/2 - 75)
    playery = int(SCREENHEIGHT* 0.1)
    
    ossilate_player = 0
    ossilation_up = True
    temp = True
    
    while temp: 
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                video_capture.stop_video()
                landmark.stop_media()
                facemask.stop_mask()
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                # make first flap sound and return values for mainGame
                temp = False
                SOUNDS['wing'].play()
        

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
            ossilate_player +=1
        elif ossilate_player >= 8: ossilation_up = False

        if ossilate_player >-8 and not ossilation_up:
            ossilate_player -=1
        elif ossilate_player <= -8:
            ossilation_up = True

        # draw sprites
        SCREEN.blit(IMAGES['player'][playerIndex],
                  (playerx, playery + ossilate_player))
        SCREEN.blit(IMAGES['message'], (messagex, messagey))
        SCREEN.blit(IMAGES['message2'], (messagex2, messagey2))
        SCREEN.blit(IMAGES["input"],input_options_pos)
        SCREEN.blit(IMAGES['space'],space_text_pos)
        SCREEN.blit(IMAGES['smile'],smile_text_pos)
        SCREEN.blit(IMAGES['altitude'],altitude_text_pos)
        SCREEN.blit(IMAGES["mode"],mode_options_pos)
        SCREEN.blit(IMAGES['pipes_mode'],pipes_text_pos)
        SCREEN.blit(IMAGES['stars_mode'],stars_text_pos)
        SCREEN.blit(IMAGES["difficulty"],difficulty_options_pos)
        SCREEN.blit(IMAGES['easy'],easy_text_pos)
        SCREEN.blit(IMAGES['medium'],medium_text_pos)
        SCREEN.blit(IMAGES['hard'],hard_text_pos)
        SCREEN.blit(IMAGES['arcade'],arcade_text_pos)
        SCREEN.blit(IMAGES['base'],(0,int(SCREENHEIGHT-IMAGES['base'].get_height())))

        if space_option.draw(SCREEN):
            if space_option.image == check_img1:
                smile_option.image = check_img1
                altitude_option.image = check_img1
            space_option.image = check_img0
            GAME_MODES = {"space":True,"smile":False,"altitude":False}
            gm = "space"
        elif smile_option.draw(SCREEN):
            if smile_option.image == check_img1:
                smile_option.image = check_img0
                altitude_option.image = check_img1
                space_option.image = check_img1
            GAME_MODES = {"space":False,"smile":True,"altitude":False}
            gm = "smile"
        elif altitude_option.draw(SCREEN):
            if altitude_option.image == check_img1:
                smile_option.image = check_img1
                altitude_option.image = check_img0
                space_option.image = check_img1
            GAME_MODES = {"space":False,"smile":False,"altitude":True}
            gm = "altitude"
        
        if pipes_option.draw(SCREEN):
            pipes_option.image = check_img0_p
            stars_option.image = check_img1_p
            GAME_TYPE['pipes'] = True
            GAME_TYPE['stars'] = False
            gt = "pipes"
        elif stars_option.draw(SCREEN):
            pipes_option.image = check_img1_p
            stars_option.image = check_img0_p
            GAME_TYPE['pipes'] = False
            GAME_TYPE['stars'] = True
            gt = "stars"

        if easy_option.draw(SCREEN):
            easy_option.image = check_img0_r
            medium_option.image = check_img1_r
            hard_option.image = check_img1_r
            arcade_option.image = check_img1_r
            GAME_DIFFICULTY = {"easy":True,"medium":False,"hard":False,"arcade":False}
            gd = "easy"
        elif medium_option.draw(SCREEN):
            easy_option.image = check_img1_r
            medium_option.image = check_img0_r
            hard_option.image = check_img1_r
            arcade_option.image = check_img1_r
            GAME_DIFFICULTY = {"easy":False,"medium":True,"hard":False,"arcade":False}
            gd = "medium"
        elif hard_option.draw(SCREEN):
            easy_option.image = check_img1_r
            medium_option.image = check_img1_r
            hard_option.image = check_img0_r
            arcade_option.image = check_img1_r
            GAME_DIFFICULTY = {"easy":False,"medium":False,"hard":True,"arcade":False}
            gd = "hard"
        elif arcade_option.draw(SCREEN):
            easy_option.image = check_img1_r
            medium_option.image = check_img1_r
            hard_option.image = check_img1_r
            arcade_option.image = check_img0_r
            GAME_DIFFICULTY = {"easy":False,"medium":False,"hard":False,"arcade":True}
            gd = "arcade"
        
        if landmarks_option.draw(SCREEN):
            if LANDMARKS:
                landmarks_option.image = IMAGES["landmarks_off"]
                LANDMARKS = False
            else:
                LANDMARKS = True
                FX = False
                landmarks_option.image = IMAGES["landmarks_on"]
                fx_option.image = IMAGES["fx_off"]
        elif fx_option.draw(SCREEN):
            pass
            """ if FX:
                fx_option.image = IMAGES["fx_off"]
                FX = False
            else:
                FX = True
                LANDMARKS = False
                landmarks_option.image = IMAGES["landmarks_off"]
                fx_option.image = IMAGES["fx_on"] """
        
        if calibrate_option.draw(SCREEN):
            landmark.configured = False

        if GAME_DIFFICULTY["easy"] or GAME_DIFFICULTY["arcade"]: PIPEGAPSIZE = IMAGES['player'][0].get_height() * 18
        elif GAME_DIFFICULTY["medium"]: PIPEGAPSIZE = IMAGES['player'][0].get_height() * 12
        elif GAME_DIFFICULTY["hard"]: PIPEGAPSIZE = IMAGES['player'][0].get_height() * 6
        
        if iterloop %5 == 0:
         playerIndex = next(playerIndexGen)
        iterloop = (iterloop + 1) % 30
        pygame.display.update()
        FPSCLOCK.tick(FPS)


def mainGame():
    global LANDMARKS,GAME_MODES,HOPPED,min_smile,max_smile,mins_l,maxs_l,BIG_STAR,high_scores,BASES_LIST,GAME_DIFFICULTY,PIPEGAPSIZE,gt,gm,gd
    landmark.num_stars = 0

    score = 0
    playerIndex = 0
    playerIndexGen = cycle([0, 1, 2, 1])
    iterloop = 0
    playerx, playery = int(SCREENWIDTH * 0.2), int(SCREENHEIGHT * 0.5) 
    stars = [getNewStar(),getNewStar()]
    stars[0]['x'] = int(SCREENWIDTH*0.5)
    stars[1]['x'] = int(SCREENWIDTH*0.8)
    proccessed_scores = []

    # get 2 new pipes to add to upperPipes lowerPipes list

    newPipe1 = getRandomPipe()
    newPipe2 = getRandomPipe()
    newPipe3 = getRandomPipe()
    newPipe4 = getRandomPipe()

    # list of upper pipes
    upperPipes = [
        {'x': int(SCREENWIDTH/2), 'y': newPipe1[0]['y'],"score":False},
        {'x': int(SCREENWIDTH - IMAGES['pipe'][0].get_width()), 'y': newPipe2[0]['y'],"score":False},
    ]

    # list of lowerpipe
    lowerPipes = [
        
        {'x': int(SCREENWIDTH/2), 'y': newPipe1[1]['y'],"score":False},
        {'x': int(SCREENWIDTH - IMAGES['pipe'][0].get_width()), 'y': newPipe2[1]['y'],"score":False},
        
    ]

    dt = FPSCLOCK.tick(FPS)/1000
    pipeVelXBase = -128
    pipeVelX = -128 * dt
    starVelX = -128 * dt
    baseVelx = -128 * dt
    # player velocity, max velocity, downward acceleration, acceleration on flap
    playerVelY    =  0   # player's velocity along Y, default same as playerFlapped
    playerAccY = 12
    playerMinAcc = -9
    maxAngle = 40
    minAngle = -15
    descentSpeed = 0.85
    max_acc = 16
    min_acc = 9
    max_acc_a = 12
    min_acc_a = 1
    spaceConst = 1
    smileConst = 1
    altitudeConst = 1
    temp = True
    start_time = time.time()

    while temp:

            
        if LANDMARKS:
            setBG(landmark.frame)
        elif FX:
            setBG(facemask.frame)
        else:
            if GAME_TYPE['stars']:
                setBG(landmark.fd)
            else:
                setBG(video_capture.frame)
        
        if not landmark.configured:
            return

        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                temp = False
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP) and GAME_MODES["space"] :
                if playery > 3 * IMAGES['player'][0].get_height():
                    playerVelY = playerAccY * spaceConst
                    SOUNDS['wing'].play()
        
        if GAME_MODES["smile"]:
         descentSpeed = 0.65
         if not HOPPED:
            if landmark.smile_level > -1 * (min_smile*1)//1 * -1:
               mag = (landmark.smile_level - min_smile) * (max_acc - min_acc) / (max_smile - min_smile)  + min_acc
               if mag > max_acc or landmark.smile_level>=max_smile*0.75 : mag = max_acc
               if mag < min_acc: mag = min_acc
               playerVelY = mag * smileConst
               SOUNDS['wing'].play()
               HOPPED = True
         elif landmark.smile_level<=-1*(min_smile*1)//1*-1 and HOPPED:
               HOPPED = False

        if GAME_MODES["altitude"]:
            if landmark.smile_level> -1*(min_smile*1)//1*-1:
                mag = (landmark.smile_level - min_smile) * (max_acc_a - min_acc_a) / (max_smile - min_smile)  + min_acc_a
                playerVelY = mag * altitudeConst
                if not wing.get_busy():
                    wing.play(SOUNDS['wing'])

        # player's movement
        if playerVelY >= 0:
            if playery > IMAGES['player'][playerIndex].get_height()/2:
                playery -= playerVelY
            else: playerVelY = 0
        if playerVelY<0:
            if playery < SCREENHEIGHT - IMAGES['base'].get_height() - IMAGES['player'][playerIndex].get_height():
                playery -= playerVelY
        if playerVelY > -9:
            playerVelY -= descentSpeed
        
        rotation = (playerVelY - playerMinAcc) * (maxAngle - minAngle) / (playerAccY -playerMinAcc)  +minAngle
        
        
        if GAME_TYPE['stars']:
            playerMidPos = (playerx + IMAGES['player'][playerIndex].get_width() / 2,playery +IMAGES['player'][playerIndex].get_height() / 2)
            col = checkCollision(stars,playerMidPos)
            if col != -100:
                if col <0:
                    landmark.num_stars += 1
                    stars.pop((-1*(col+1)))
                    score += 8
                else:
                    stars.pop(col)
                    score +=1
                if score % 2 == 0:
                    if score not in proccessed_scores:
                        proccessed_scores.append(score)
                        BIG_STAR = True
                SOUNDS['point'].play() 
                
            # move star to left
            for star in stars:
                star['x'] += starVelX
                if star['b']:
                    SCREEN.blit(IMAGES['star_big'],(star['x'],star['y']))
                else:
                    SCREEN.blit(IMAGES['star'],(star['x'],star['y']))

            # add new pipe when first pipe is about to touch left of screen
            if stars[-1]['x'] <= SCREENWIDTH*0.6 and not BIG_STAR:
                stars.append(getNewStar())

            if BIG_STAR:
                stars.append(getBigStar())
                BIG_STAR = False
            # remove first pipe if its out of the screen
            if len(stars) > 0 and stars[0]['x'] < -IMAGES['star'].get_width():
                stars.pop(0)

                

        elif GAME_TYPE['pipes']:
            playerMidPos = (playerx,playery)
            if checkCrash(playerMidPos,upperPipes,lowerPipes):
                return {
                    'score': score,
                    'y' : playery,
                    'up':upperPipes,
                    'lp': lowerPipes,
                    'bases':BASES_LIST
                }
            else:
                for i in range(len(upperPipes)):
                    if playerMidPos[0] >= upperPipes[i]['x'] + IMAGES['pipe'][0].get_width()//2 and not upperPipes[i]['score']:
                        score += 1
                        upperPipes[i]['score'] = True
                        SOUNDS['point'].play()
                    upperPipes[i]['x'] += pipeVelX
                    lowerPipes[i]['x'] += pipeVelX

                    SCREEN.blit(IMAGES['pipe'][0],(upperPipes[i]['x'],upperPipes[i]['y']))
                    SCREEN.blit(IMAGES['pipe'][1],(lowerPipes[i]['x'],lowerPipes[i]['y']))

                if upperPipes[-1]['x'] <= SCREENWIDTH*0.6:
                    newPipe = getRandomPipe()
                    upperPipes.append(newPipe[0])
                    lowerPipes.append(newPipe[1])
                    

                if len(upperPipes)>0 and upperPipes[0]['x'] < - IMAGES['pipe'][0].get_width():
                    upperPipes.pop(0)
                    lowerPipes.pop(0)

                
                    

                
        if landmark.smile_level <15 and len(mins_l)<100:
            mins_l.append(landmark.smile_level)
        elif landmark.smile_level > 25 and len(maxs_l)<100:
            maxs_l.append(landmark.smile_level)
        try:
            min_smile = sum(mins_l)/len(mins_l)
            max_smile = sum(maxs_l)/len(maxs_l)
        except: pass
        
        showScore(score)
        
        playerSurface = pygame.transform.rotate(IMAGES['player'][playerIndex], rotation)
        SCREEN.blit(playerSurface, (playerx, playery))
        #SCREEN.blit(IMAGES['base'],(0,int(SCREENHEIGHT-IMAGES['base'].get_height())))

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
        
        if GAME_TYPE['pipes'] and GAME_DIFFICULTY["arcade"] and time.time() - start_time > 3:
            
            pipeVelXBase  -= 5
            pipeVelX = pipeVelXBase * dt
            if PIPEGAPSIZE > IMAGES['player'][0].get_height() * 2.5:
                PIPEGAPSIZE -= 4
            descentSpeed += 0.06
            #if spaceConst 
            spaceConst += 0.01
            smileConst += 0.01
            altitudeConst += 0.01
            start_time = time.time()
        
        FPSCLOCK.tick(FPS)
        pygame.display.update()
    
    if GAME_TYPE['stars']:
        if high_scores[gt][gm]["s"]<score:
            update_high_score("",score)


def showGameOverScreen(crashInfo):
    global file_path,GAME_MODES,BASES_LIST,high_scores,gm,gt,gd,NEW_HIGH_SCORE,LANDMARKS,FX
    score = crashInfo['score']
    playerx = SCREENWIDTH * 0.2
    playery = crashInfo['y']
    upperPipes = crashInfo['up']
    lowerPipes = crashInfo['lp']

    # play hit and die sounds
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
        events = pygame.event.get()
        for event in events:
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                if NEW_HIGH_SCORE:
                    update_high_score("?", score)
                return
            if not NEW_HIGH_SCORE:
                if (event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP)):
                    return
            else:
                if event.type == KEYDOWN and (event.key == K_RETURN or event.key == K_UP):
                    update_high_score(input_text, score)
                    return

        if not landmark.configured:
            return
        if processedScore:
            return
        # player y shift
        if playery < SCREENHEIGHT - IMAGES['base'].get_height() - IMAGES['player'][0].get_height():
            playery += 7

        playerRot  = -75
        setBG(frame)


        for uPipe, lPipe in zip(upperPipes, lowerPipes):
            SCREEN.blit(IMAGES['pipe'][0], (uPipe['x'], uPipe['y']))
            SCREEN.blit(IMAGES['pipe'][1], (lPipe['x'], lPipe['y']))

        playerSurface = pygame.transform.rotate(IMAGES['player'][1], playerRot)
        SCREEN.blit(playerSurface, (playerx,playery))
        #SCREEN.blit(IMAGES['gameover'], ((SCREENWIDTH -IMAGES['gameover'].get_width())/2 , (SCREENHEIGHT-IMAGES['gameover'].get_height())/2))

        for base in BASES_LIST:
            SCREEN.blit(IMAGES['base'],(base['x'],int(SCREENHEIGHT-IMAGES['base'].get_height())))
        
        if NEW_HIGH_SCORE:
            newHighScore(score,events)
        elif not NEW_HIGH_SCORE:
            showScore(score,True)
        
        FPSCLOCK.tick(FPS)
        pygame.display.update()

def getNewStar():
       
      return {'x':random.randrange(int(SCREENWIDTH*0.7),SCREENWIDTH),
            'y':random.randrange(int(SCREENHEIGHT*0.2),int((SCREENHEIGHT-IMAGES['base'].get_height())*0.8)),
    'score': False,'b':False}

def getBigStar():
    return {'x':random.randrange(int(SCREENWIDTH*0.7),SCREENWIDTH),
            'y':random.randrange(int(SCREENHEIGHT*0.3),int((SCREENHEIGHT-IMAGES['base'].get_height())*0.6)),
            'score': False,'b':True}

""" def getRandomPipe():
    upper_y = random.randrange(-IMAGES['pipe'][0].get_height() + IMAGES['player'][0].get_height() , 0)
    lower_y = upper_y + IMAGES['pipe'][0].get_height() + PIPEGAPSIZE
    pipeX = SCREENWIDTH + 30
    
    return [
        {'x': pipeX, 'y':upper_y,"score":False},  # upper pipe
        {'x': pipeX, 'y': lower_y,"score":False}, # lower pipe
    ] """

def getRandomPipe():
    min_upper_y = -IMAGES['pipe'][0].get_height() + IMAGES['player'][0].get_height() + 10
    max_upper_y = SCREENHEIGHT - IMAGES['base'].get_height() - IMAGES['player'][0].get_height()*2 - PIPEGAPSIZE - IMAGES['pipe'][0].get_height() - 10

    upper_y = random.randrange(min_upper_y, max_upper_y)
    lower_y = upper_y + IMAGES['pipe'][0].get_height() + PIPEGAPSIZE
    pipeX = SCREENWIDTH + 30
    
    return [
        {'x': pipeX, 'y': upper_y, "score": False},  # upper pipe
        {'x': pipeX, 'y': lower_y, "score": False},  # lower pipe
    ]

def setBG(frame, f = False):
    if frame is not None:
        bg = cv.resize(frame,(SCREENWIDTH,SCREENHEIGHT))
        bg = cv.flip(bg,1)
        bg = cv.cvtColor(bg,cv.COLOR_BGR2RGB)
        
        #bg = pygame.image.frombuffer(bg.tostring(), bg.shape[1::-1], "BGR")
        bg = pygame.surfarray.make_surface(bg)
        bg = pygame.transform.rotate(bg, -90)
        SCREEN.blit(bg,(0,0))

def showScore(score,gameOver = False):
    global high_scores,gt,gm,gd,font,NEW_HIGH_SCORE
    scoreDigits = [int(x) for x in list(str(score))]
    totalWidth = 0 # total width of all numbers to be printed
    
    if gt == "stars":
        if high_scores[gt][gm]["s"]<score:
            NEW_HIGH_SCORE = True
    elif gt == "pipes":
        if high_scores[gt][gm][gd]["s"]<score:
            NEW_HIGH_SCORE = True

    if not gameOver:
        for digit in scoreDigits:
            totalWidth += IMAGES['numbers'][digit].get_width()
        Xoffset = (SCREENWIDTH - totalWidth) / 2
        for digit in scoreDigits:
            SCREEN.blit(IMAGES['numbers'][digit], (Xoffset, SCREENHEIGHT * 0.1))
            Xoffset += IMAGES['numbers'][digit].get_width()

        if gt == "stars":
            scoreDigits = [int(x) for x in list(str(high_scores[gt][gm]["s"]))]
            totalWidth = 0 # total width of all numbers to be printed
            for digit in scoreDigits:
                totalWidth += IMAGES['numbersg'][digit].get_width()
            Xoffset = (SCREENWIDTH - totalWidth) / 2
            for digit in scoreDigits:
                SCREEN.blit(IMAGES['numbersg'][digit], (Xoffset, SCREENHEIGHT * 0.1 - IMAGES['numbersg'][digit].get_height() - 2))
                Xoffset += IMAGES['numbersg'][digit].get_width()
        if gt == "pipes":
            scoreDigits = [int(x) for x in list(str(high_scores[gt][gm][gd]["s"]))]
            totalWidth = 0 # total width of all numbers to be printed
            for digit in scoreDigits:
                totalWidth += IMAGES['numbersg'][digit].get_width()
            Xoffset = (SCREENWIDTH - totalWidth) / 2
            for digit in scoreDigits:
                SCREEN.blit(IMAGES['numbersg'][digit], (Xoffset, SCREENHEIGHT * 0.1 - IMAGES['numbersg'][digit].get_height() - 2))
                Xoffset += IMAGES['numbersg'][digit].get_width()
    else:
        h = SCREENHEIGHT*0.3
        SCREEN.blit(IMAGES['y_hs'],(SCREENWIDTH//2-IMAGES['y_hs'].get_width()//2,h))

        for digit in scoreDigits:
            totalWidth += IMAGES['numbers'][digit].get_width()
        Xoffset = (SCREENWIDTH - totalWidth) / 2
        for digit in scoreDigits:
            SCREEN.blit(IMAGES['numbers'][digit], (Xoffset, h + IMAGES['y_hs'].get_height() + 10))
            Xoffset += IMAGES['numbers'][digit].get_width()

        SCREEN.blit(IMAGES['hs'],(SCREENWIDTH//2-IMAGES['hs'].get_width()//2,h+ IMAGES['y_hs'].get_height() + 10 + IMAGES['numbers'][0].get_height() + 10))

        if gt == "stars":
            scoreDigits = [int(x) for x in list(str(high_scores[gt][gm]["s"]))]
            totalWidth = 0 # total width of all numbers to be printed
            for digit in scoreDigits:
                totalWidth += IMAGES['numbers'][digit].get_width()
            Xoffset = (SCREENWIDTH - totalWidth) / 2
            for digit in scoreDigits:
                SCREEN.blit(IMAGES['numbers'][digit], (Xoffset, h+ IMAGES['y_hs'].get_height() + 10 + IMAGES['numbers'][0].get_height() + 10 + IMAGES['hs'].get_height() + 10))
                Xoffset += IMAGES['numbers'][digit].get_width()

            hs_name = font.render(high_scores[gt][gm]["name"], True, (0, 0, 0))
            SCREEN.blit(hs_name, (SCREENWIDTH//2 - hs_name.get_width()//2,h+ IMAGES['y_hs'].get_height() + 10 + IMAGES['numbers'][0].get_height() + 10 + IMAGES['hs'].get_height() + 10 + IMAGES['numbers'][0].get_height() + 10))
        if gt == "pipes":
            scoreDigits = [int(x) for x in list(str(high_scores[gt][gm][gd]["s"]))]
            totalWidth = 0 # total width of all numbers to be printed
            for digit in scoreDigits:
                totalWidth += IMAGES['numbers'][digit].get_width()
            Xoffset = (SCREENWIDTH - totalWidth) / 2
            for digit in scoreDigits:
                SCREEN.blit(IMAGES['numbers'][digit], (Xoffset, h+ IMAGES['y_hs'].get_height() + 10 + IMAGES['numbers'][0].get_height() + 10 + IMAGES['hs'].get_height() + 10))
                Xoffset += IMAGES['numbers'][digit].get_width()

            hs_name = font.render(high_scores[gt][gm][gd]["name"], True, (0, 0, 0))
            SCREEN.blit(hs_name, (SCREENWIDTH//2 - hs_name.get_width()//2,h+ IMAGES['y_hs'].get_height() + 10 + IMAGES['numbers'][0].get_height() + 10 + IMAGES['hs'].get_height() + 10 + IMAGES['numbers'][0].get_height() + 10))

def newHighScore(score,events):
    global NEW_HIGH_SCORE,gt,gd,gm,font,high_scores,input_text

    if gt == 'stars':
        prev_name = font.render(high_scores[gt][gm]["name"], True, (0, 0, 0))
        prev_score = high_scores[gt][gm]["s"]
    elif gt == 'pipes':
        prev_name = font.render(high_scores[gt][gm][gd]["name"], True, (0, 0, 0))
        prev_score = high_scores[gt][gm][gd]["s"]

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
   for j,i in enumerate(stars):
      
      if i['b']:
         
         x0 = i['x']
         x1 = i['x'] + IMAGES['star_big'].get_width()
         y0 = i['y']
         y1 = i['y'] + IMAGES['star_big'].get_height()
         
         if playerMidPos[0]<x1 and playerMidPos[0]>x0 and playerMidPos[1]<y1 and playerMidPos[1]>y0:
            return -j-1
      else:
         x0 = i['x']
         x1 = i['x'] + IMAGES['star'].get_width()
         y0 = i['y']
         y1 = i['y'] + IMAGES['star'].get_height()
         
         if playerMidPos[0]<x1 and playerMidPos[0]>x0 and playerMidPos[1]<y1 and playerMidPos[1]>y0:
            return j
   return -100

def checkCrash(playerMidPos, upperPipes, lowerPipes):
    if playerMidPos[1] + IMAGES['player'][0].get_height()//3 >= SCREENHEIGHT - IMAGES['base'].get_height() - IMAGES['player'][0].get_height():
        return True
    
    for i in range(len(upperPipes)):
        x0 = upperPipes[i]['x'] - 2
        x1 = upperPipes[i]['x'] + IMAGES['pipe'][0].get_width() + 2
        y0 = upperPipes[i]['y'] - 2 
        y1 = upperPipes[i]['y'] + IMAGES['pipe'][0].get_height() +2
        
        #crash by right
        if (playerMidPos[0]+IMAGES['player'][0].get_width()<x1 and playerMidPos[0]+IMAGES['player'][0].get_width() >x0 and 
            playerMidPos[1] +IMAGES['player'][0].get_height()<y1 and playerMidPos[1] >y0):
            return True
        #crash by top
        elif (playerMidPos[0]+IMAGES['player'][0].get_width()/2<x1 and playerMidPos[0]+IMAGES['player'][0].get_width()/2 >x0 and 
            playerMidPos[1]<y1 and playerMidPos[1] >y0):
            return True
        #crash by bottom
        elif (playerMidPos[0]+IMAGES['player'][0].get_width()/2<x1 and playerMidPos[0]+IMAGES['player'][0].get_width()/2 >x0 and 
            playerMidPos[1]+IMAGES['player'][0].get_height()<y1 and playerMidPos[1]+IMAGES['player'][0].get_height() >y0):
            return True
        
        x0 = lowerPipes[i]['x'] -2 
        x1 = lowerPipes[i]['x'] + IMAGES['pipe'][0].get_width() + 2
        y0 = lowerPipes[i]['y'] - 2
        y1 = lowerPipes[i]['y'] + IMAGES['pipe'][0].get_height() + 2
        
        #crash by right
        if (playerMidPos[0]+IMAGES['player'][0].get_width()<x1 and playerMidPos[0]+IMAGES['player'][0].get_width() >x0 and 
            playerMidPos[1] +IMAGES['player'][0].get_height()<y1 and playerMidPos[1] >y0):
            return True
        #crash by top
        elif (playerMidPos[0]+IMAGES['player'][0].get_width()/2<x1 and playerMidPos[0]+IMAGES['player'][0].get_width()/2 >x0 and 
            playerMidPos[1]<y1 and playerMidPos[1] >y0):
            return True
        #crash by bottom
        elif (playerMidPos[0]+IMAGES['player'][0].get_width()/2<x1 and playerMidPos[0]+IMAGES['player'][0].get_width()/2 >x0 and 
            playerMidPos[1]+IMAGES['player'][0].get_height()<y1 and playerMidPos[1]+IMAGES['player'][0].get_height() >y0):
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
    global gt,gm,gd
    if gt == "stars":
        high_scores[gt][gm]["s"] = score
        high_scores[gt][gm]["name"] = input_text
    elif gt == "pipes":
        high_scores[gt][gm][gd]["s"] = score
        high_scores[gt][gm][gd]["name"] = input_text

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

    dt = FPSCLOCK.tick(FPS)/1000
    playerIndex = 0
    playery = int(SCREENHEIGHT*0.5)
    playerIndexGen = cycle([0, 1, 2, 1])
    iterloop = 0
    baseVelx = -16 * dt
    playerVelY    =  0  
    playerAccY = 12
    playerMinAcc = -9
    maxAngle = 60
    minAngle = 0
    descentSpeed = 0.65
    max_acc = 15
    min_acc = 10
    landmark_list = []
    smileConst = 1

    
    temp = True
    while temp:

        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                temp = False
    
        setBG(video_capture.frame)

        
         
        if not HOPPED:
            if landmark.smile_level > -1 * (min_smile*1.2)//1 * -1:
                mag = (landmark.smile_level - min_smile) * (max_acc - min_acc) / (max_smile - min_smile)  + min_acc
                if mag > max_acc or landmark.smile_level>=max_smile*0.75 : mag = max_acc
                if mag < min_acc: mag = min_acc
                playerVelY = mag * smileConst
                SOUNDS['wing'].play()
                HOPPED = True
        elif landmark.smile_level<=-1*(min_smile*1.2)//1*-1 and HOPPED:
            HOPPED = False


        if playerVelY >= 0:
            if playery > IMAGES['player'][playerIndex].get_height()/2:
                playery -= playerVelY
            else: playerVelY = 0
        if playerVelY<0:
            if playery < SCREENHEIGHT - IMAGES['base'].get_height() - IMAGES['player'][playerIndex].get_height():
                playery -= playerVelY
        if playerVelY > -9:
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
        
        t = sub_list[:int(len(sub_list)*0.2)]
        try:
            min_smile = np.sum(t) / len(t)
        except:
            try: 
                min_smile = sub_list[0]
            except:
                min_smile = 12
        
        t = sub_list[int(len(sub_list)*0.8):]
        try:
            max_smile = np.sum(t) / len(t)
        except:
            try: 
                max_smile = sub_list[-1]
            except:
                max_smile = 45
        
            
        
        FPSCLOCK.tick(FPS)
        pygame.display.update()
    
    landmark.configured = True
    print(min_smile,max_smile)



if __name__ == '__main__':
    main()
