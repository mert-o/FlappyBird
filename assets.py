import os,glob,sys
import pygame 



def load_images(SCREENWIDTH,SCREENHEIGHT):
    IMAGES = {}

    IMAGES['player'] = (
        pygame.image.load('assets/sprites/yellowbird-upflap.png').convert_alpha(),
        pygame.image.load('assets/sprites/yellowbird-midflap.png').convert_alpha(),
        pygame.image.load('assets/sprites/yellowbird-downflap.png').convert_alpha(),
    )

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

    IMAGES['colon'] = pygame.image.load('assets/sprites/colon.png').convert_alpha()
    IMAGES['colon'] = pygame.transform.scale(IMAGES['colon'],(IMAGES['colon'].get_width()//2,IMAGES['colon'].get_height()//2))

    scaled_images = [pygame.transform.scale(img, (int(img.get_width() * 0.85), int(img.get_height() * 0.85))) for img in IMAGES['numbersg']]
    IMAGES['numbersg'] = tuple(scaled_images)

    # game over sprite
    IMAGES['gameover'] = pygame.image.load('assets/sprites/gameover.png').convert_alpha()

    # message sprite for welcome screen
    IMAGES['message'] = pygame.image.load('assets/sprites/welcome_v1.png').convert_alpha()
    IMAGES['message'] = pygame.transform.scale(IMAGES['message'],(IMAGES['message'].get_width() * 0.7 , IMAGES['message'].get_height()*0.7))
    IMAGES['message2'] = pygame.image.load('assets/sprites/press_space.png').convert_alpha()
    IMAGES['message2'] = pygame.transform.scale(IMAGES['message2'],(IMAGES['message2'].get_width() * 1.2 , IMAGES['message2'].get_height()*1.2))

    IMAGES['configure'] = pygame.image.load('assets/sprites/configure.png').convert_alpha()
    IMAGES['configure'] = pygame.transform.scale(IMAGES['configure'],(IMAGES['configure'].get_width() * 0.8 , IMAGES['configure'].get_height()*0.8))

    IMAGES['prev'] = pygame.image.load('assets/sprites/previous.png').convert_alpha()

    IMAGES['prev'] = pygame.transform.scale(IMAGES['prev'],(IMAGES['prev'].get_width() * 0.8 , IMAGES['prev'].get_height()*0.8))

    # base (ground) sprite
    IMAGES['base'] = pygame.image.load('assets/sprites/base.png').convert_alpha()
    IMAGES['base'] = pygame.transform.scale(IMAGES['base'],(SCREENWIDTH,SCREENHEIGHT*0.1))


    _star_big = pygame.image.load('assets/sprites/star.png').convert_alpha()
    
    _star = pygame.transform.scale(_star_big,(_star_big.get_width()//1.6,_star_big.get_height()//1.6))
    IMAGES['star'] = _star
    IMAGES['star_big'] = _star_big

    IMAGES['calibrate_img'] = pygame.image.load('assets/sprites/calibrate_white.png')
    IMAGES['calibrate_img'] = pygame.transform.scale(IMAGES['calibrate_img'],(IMAGES['calibrate_img'].get_width()*0.7,IMAGES['calibrate_img'].get_height()*0.7))

    IMAGES['settings_img'] = pygame.image.load('assets/sprites/settings.png')
    IMAGES['settings_img'] = pygame.transform.scale(IMAGES['settings_img'],(IMAGES['settings_img'].get_width()*0.7,IMAGES['settings_img'].get_height()*0.7))

    _pipe = pygame.image.load('assets/sprites/pipe-green.png').convert_alpha()
    _pipe = pygame.transform.scale(_pipe,(_pipe.get_width(),(SCREENHEIGHT-50)))
    IMAGES['pipe'] = [
        pygame.transform.flip(_pipe, False, True),
        _pipe,
    ]

    IMAGES['heart'] = pygame.image.load('assets/sprites/heart.png').convert_alpha()
    IMAGES['heart'] = pygame.transform.scale(IMAGES['heart'],(IMAGES['heart'].get_width() * 0.15 , IMAGES['heart'].get_height()*0.15))

    return IMAGES

    
def load_sounds():
    SOUNDS = {}
    if 'win' in sys.platform:
        soundExt = '.wav'
    else:
        soundExt = '.ogg'


    SOUNDS['die']    = pygame.mixer.Sound('assets/audio/die' + soundExt)
    SOUNDS['hit']    = pygame.mixer.Sound('assets/audio/hit' + soundExt)
    SOUNDS['point']  = pygame.mixer.Sound('assets/audio/point' + soundExt)
    SOUNDS['swoosh'] = pygame.mixer.Sound('assets/audio/swoosh' + soundExt)
    SOUNDS['wing']   = pygame.mixer.Sound('assets/audio/wing' + soundExt)
    SOUNDS['pop'] = pygame.mixer.Sound('assets/audio/pop.wav')
    SOUNDS['burn'] = pygame.mixer.Sound('assets/audio/burn.wav')
    SOUNDS['oops'] = pygame.mixer.Sound('assets/audio/oops.wav')
    SOUNDS['pipes'] = pygame.mixer.Sound('assets/audio/pipes.wav')
    SOUNDS['stars'] = pygame.mixer.Sound('assets/audio/stars.wav')

    return SOUNDS


