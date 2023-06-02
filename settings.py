import pygame



class Settings:

    def __init__(self,screen) -> None:
        self.screen = screen
        self.sw = self.screen.get_width()
        self.sh = self.screen.get_height()

        self.GAME_MODES = {"space":True,"smile":False,"altitude":False}
        self.GAME_DIFFICULTY = {"easy":True,"medium":False,"hard":False,"arcade":False}
        self.GAME_TYPE = {'pipes':True,'stars': False,'balloons':False,'pisa':False}
        self.fonth = pygame.font.Font('assets/font/Ubuntu-BoldItalic.ttf',46)
        self.font = pygame.font.Font('assets/font/Ubuntu-Medium.ttf',36)
        self.color = (30,30,30)
        self.colorg = (10,240,10)
        self.colorr = (240,10,10)
        self.landmark = False
        self.start_w = self.sw * 0.2
        self.start_h = self.sh * 0.2
        self.option_w = 180
        self.mode_w = 200
        self.input_text = self.fonth.render('Input:',True,(15,15,15))
        self.space_text = self.font.render('Space',True,self.colorg)
        self.space_rect = self.space_text.get_rect()
        self.smile_text = self.font.render('Smile',True,self.color)
        self.smile_rect = self.smile_text.get_rect()
        self.alt_text = self.font.render('Altitude',True,self.color)
        self.alt_rect = self.alt_text.get_rect()

        self.mode_text = self.fonth.render('Mode:',True,(15,15,15))
        self.pipes_text = self.font.render('Pipes',True,self.colorg)
        self.pipes_rect = self.pipes_text.get_rect()
        self.stars_text = self.font.render('Stars',True,self.color)
        self.stars_rect = self.stars_text.get_rect()
        self.balloons_text = self.font.render('Balloons',True,self.color)
        self.balloons_rect = self.balloons_text.get_rect()
        self.pisa_text = self.font.render('Pipes and Stars',True,self.color)
        self.pisa_rect = self.pisa_text.get_rect()

        self.diff_text = self.fonth.render('Difficulty:',True,(15,15,15))
        self.easy_text = self.font.render('Easy',True,self.colorg)
        self.easy_rect = self.easy_text.get_rect()
        self.med_text = self.font.render('Medium',True,self.color)
        self.med_rect = self.med_text.get_rect()
        self.hard_text = self.font.render('Hard',True,self.color)
        self.hard_rect = self.hard_text.get_rect()
        self.arc_text = self.font.render('Arcade',True,self.color)
        self.arc_rect = self.arc_text.get_rect()
        
        self.landmarks_text = self.fonth.render('Landmarks On/Off', True,self.colorr)
        self.landmark_rect = self.landmarks_text.get_rect()
        
        self.rect_list = [(self.space_text,self.space_rect),(self.smile_text,self.smile_rect),
                     (self.alt_text,self.alt_rect),
                     (self.pipes_text,self.pipes_rect),(self.stars_text,self.stars_rect),
                    (self.balloons_text,self.balloons_rect), (self.pisa_text,self.pisa_rect),
                    (self.easy_text,self.easy_rect),(self.med_text,self.med_rect),
                    (self.hard_text,self.hard_rect),(self.arc_text,self.arc_rect),
                    (self.landmarks_text,self.landmark_rect)]
    def draw(self,pos):
        
        self.screen.blit(self.input_text,(self.start_w,self.start_h))
        opt_pos = [self.start_w + 20, self.start_h + 10 +self.input_text.get_height()]

        self.screen.blit(self.space_text,opt_pos)
        self.space_rect.x = opt_pos[0]
        self.space_rect.y = opt_pos[1]

        if self.space_rect.collidepoint(pos):
            self.space_text = self.font.render('Space',True,self.colorg)
            self.smile_text = self.font.render('Smile',True,self.color)
            self.alt_text = self.font.render('Altitude',True,self.color)
            self.update_dict(self.GAME_MODES,'space')

        opt_pos[0] += self.option_w
        self.screen.blit(self.smile_text,opt_pos)
        self.smile_rect.x = opt_pos[0]
        self.smile_rect.y = opt_pos[1]
        if self.smile_rect.collidepoint(pos):
            self.space_text = self.font.render('Space',True,self.color)
            self.smile_text = self.font.render('Smile',True,self.colorg)
            self.alt_text = self.font.render('Altitude',True,self.color)
            self.update_dict(self.GAME_MODES,'smile')

        opt_pos[0] -= self.option_w
        opt_pos[1] += self.smile_text.get_height() + 10
        self.screen.blit(self.alt_text,opt_pos)
        self.alt_rect.x = opt_pos[0]
        self.alt_rect.y = opt_pos[1]
        if self.alt_rect.collidepoint(pos):
            if not self.GAME_TYPE['balloons']:
                self.space_text = self.font.render('Space',True,self.color)
                self.smile_text = self.font.render('Smile',True,self.color)
                self.alt_text = self.font.render('Altitude',True,self.colorg)
                self.update_dict(self.GAME_MODES,'altitude')
        
        opt_pos[0] += self.mode_w + self.smile_text.get_width() + 20
        opt_pos[1] = self.start_h
        self.screen.blit(self.mode_text,opt_pos)

        opt_pos[0] += 20
        opt_pos[1] += self.mode_text.get_height() + 10
        self.screen.blit(self.pipes_text,opt_pos)
        self.pipes_rect.x = opt_pos[0]
        self.pipes_rect.y = opt_pos[1]
        if self.pipes_rect.collidepoint(pos):
            if self.GAME_TYPE['stars'] or self.GAME_TYPE['balloons']:
                self.easy_text = self.font.render('Easy',True,self.colorg)
                self.med_text = self.font.render('Medium',True,self.color)
                self.hard_text = self.font.render('Hard',True,self.color)
                self.arc_text = self.font.render('Arcade',True,self.color)
                self.update_dict(self.GAME_DIFFICULTY,'easy')

            self.pipes_text = self.font.render('Pipes',True,self.colorg)
            self.stars_text = self.font.render('Stars',True,self.color)
            self.balloons_text = self.font.render('Balloons',True,self.color)
            self.pisa_text = self.font.render('Pipes and Stars',True,self.color)
            self.update_dict(self.GAME_TYPE,'pipes')

        opt_pos[0] += self.option_w
        self.screen.blit(self.stars_text,opt_pos)
        self.stars_rect.x = opt_pos[0]
        self.stars_rect.y = opt_pos[1]
        if self.stars_rect.collidepoint(pos):
            self.pipes_text = self.font.render('Pipes',True,self.color)
            self.stars_text = self.font.render('Stars',True,self.colorg)
            self.balloons_text = self.font.render('Balloons',True,self.color)
            self.pisa_text = self.font.render('Pipes and Stars',True,self.color)
            self.update_dict(self.GAME_TYPE,'stars')

            self.easy_text = self.font.render('Easy',True,self.colorr)
            self.med_text = self.font.render('Medium',True,self.colorr)
            self.hard_text = self.font.render('Hard',True,self.colorr)
            self.arc_text = self.font.render('Arcade',True,self.colorr)
            



        opt_pos[0] -= self.option_w
        opt_pos[1] += self.stars_text.get_height() + 10
        self.screen.blit(self.balloons_text,opt_pos)
        self.balloons_rect.x = opt_pos[0]
        self.balloons_rect.y = opt_pos[1]
        if self.balloons_rect.collidepoint(pos):
            self.pipes_text = self.font.render('Pipes',True,self.color)
            self.stars_text = self.font.render('Stars',True,self.color)
            self.balloons_text = self.font.render('Balloons',True,self.colorg)
            self.pisa_text = self.font.render('Pipes and Stars',True,self.color)
            self.update_dict(self.GAME_TYPE,'balloons')

            self.space_text = self.font.render('Space',True,self.colorg)
            self.smile_text = self.font.render('Smile',True,self.color)
            self.alt_text = self.font.render('Altitude',True,self.colorr)
            self.update_dict(self.GAME_MODES,'space')

            self.easy_text = self.font.render('Easy',True,self.colorr)
            self.med_text = self.font.render('Medium',True,self.colorr)
            self.hard_text = self.font.render('Hard',True,self.colorr)
            self.arc_text = self.font.render('Arcade',True,self.colorr)
            

        opt_pos[0] += self.option_w
        self.screen.blit(self.pisa_text,opt_pos)
        self.pisa_rect.x = opt_pos[0]
        self.pisa_rect.y = opt_pos[1]
        if self.pisa_rect.collidepoint(pos):
            if self.GAME_TYPE['stars'] or self.GAME_TYPE['balloons']:
                self.easy_text = self.font.render('Easy',True,self.colorg)
                self.med_text = self.font.render('Medium',True,self.color)
                self.hard_text = self.font.render('Hard',True,self.color)
                self.arc_text = self.font.render('Arcade',True,self.color)
                self.update_dict(self.GAME_DIFFICULTY,'easy')

            self.pipes_text = self.font.render('Pipes',True,self.color)
            self.stars_text = self.font.render('Stars',True,self.color)
            self.balloons_text = self.font.render('Balloons',True,self.color)
            self.pisa_text = self.font.render('Pipes and Stars',True,self.colorg)
            self.update_dict(self.GAME_TYPE,'pisa')

        opt_pos[0] = self.start_w
        opt_pos[1] = self.alt_rect.y + self.alt_text.get_height() + 20
        self.screen.blit(self.diff_text,opt_pos)

        opt_pos[0] += 20
        opt_pos[1] += self.diff_text.get_height() + 10
        self.screen.blit(self.easy_text,opt_pos)
        self.easy_rect.x = opt_pos[0]
        self.easy_rect.y = opt_pos[1]
        if self.easy_rect.collidepoint(pos):
            if not self.GAME_TYPE['stars'] and not self.GAME_TYPE['balloons']:
                self.easy_text = self.font.render('Easy',True,self.colorg)
                self.med_text = self.font.render('Medium',True,self.color)
                self.hard_text = self.font.render('Hard',True,self.color)
                self.arc_text = self.font.render('Arcade',True,self.color)
                self.update_dict(self.GAME_DIFFICULTY,'easy')

        opt_pos[0] += self.option_w
        self.screen.blit(self.med_text,opt_pos)
        self.med_rect.x = opt_pos[0]
        self.med_rect.y = opt_pos[1]
        if self.med_rect.collidepoint(pos):
            if not self.GAME_TYPE['stars'] and not self.GAME_TYPE['balloons']:
                self.easy_text = self.font.render('Easy',True,self.color)
                self.med_text = self.font.render('Medium',True,self.colorg)
                self.hard_text = self.font.render('Hard',True,self.color)
                self.arc_text = self.font.render('Arcade',True,self.color)
                self.update_dict(self.GAME_DIFFICULTY,'medium')

        opt_pos[0] -= self.option_w
        opt_pos[1] += self.easy_text.get_height() + 10
        self.screen.blit(self.hard_text,opt_pos)
        self.hard_rect.x = opt_pos[0]
        self.hard_rect.y = opt_pos[1]
        if self.hard_rect.collidepoint(pos):
            if not self.GAME_TYPE['stars'] and not self.GAME_TYPE['balloons']:
                self.easy_text = self.font.render('Easy',True,self.color)
                self.med_text = self.font.render('Medium',True,self.color)
                self.hard_text = self.font.render('Hard',True,self.colorg)
                self.arc_text = self.font.render('Arcade',True,self.color)
                self.update_dict(self.GAME_DIFFICULTY,'hard')

        opt_pos[0] += self.option_w
        self.screen.blit(self.arc_text,opt_pos)
        self.arc_rect.x = opt_pos[0]
        self.arc_rect.y = opt_pos[1]
        if self.arc_rect.collidepoint(pos):
            if not self.GAME_TYPE['stars'] and not self.GAME_TYPE['balloons']:
                self.easy_text = self.font.render('Easy',True,self.color)
                self.med_text = self.font.render('Medium',True,self.color)
                self.hard_text = self.font.render('Hard',True,self.color)
                self.arc_text = self.font.render('Arcade',True,self.colorg)
                self.update_dict(self.GAME_DIFFICULTY,'arcade')
        
        opt_pos[0] = self.start_w
        opt_pos[1] = self.arc_rect.y + self.arc_text.get_height() + 20
        self.screen.blit(self.landmarks_text,opt_pos)
        self.landmark_rect.x = opt_pos[0]
        self.landmark_rect.y = opt_pos[1]
        if self.landmark_rect.collidepoint(pos):
            if self.landmark:
                self.landmarks_text = self.fonth.render('Landmark On/Off',True,self.colorr)
                self.landmark = False
            else:
                self.landmarks_text = self.fonth.render('Landmark On/Off',True,self.colorg)
                self.landmark = True

        return self.GAME_TYPE,self.GAME_MODES,self.GAME_DIFFICULTY,self.landmark
    
    def update_dict(self,dict,key):
        for k in dict.keys():
            if k == key:
                dict[k] = True
            else:
                dict[k] = False








