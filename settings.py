import pygame



class Settings:

    def __init__(self,screen) -> None:
        self.screen = screen
        self.sw = self.screen.get_width()
        self.sh = self.screen.get_height()

        self.GAME_MODES = {"space":True,"smile":False,"altitude":False}
        self.GAME_DIFFICULTY = {"easy":True,"medium":False,"hard":False,"arcade":False}
        self.GAME_TYPE = {'pipes':True,'stars': False,'balloons':False,'pisa':False, 'banners':False, 'pisabal':False,'levels':False}
        
        self.fonth = pygame.font.Font('assets/font/Ubuntu-BoldItalic.ttf',46)
        self.font = pygame.font.Font('assets/font/Ubuntu-Medium.ttf',36)
        
        self.color = (30,30,30)
        self.colorg = (10,240,10)
        self.colorr = (240,10,10)
        
        self.landmark = False
        self.record = False
        self.start_w = self.sw * 0.2
        self.start_h = self.sh * 0.2
        
        self.option_w = self.sw * 0.15
        self.mode_w = self.sw * 0.2
        
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
        
        self.banners_text = self.font.render('Banners',True,self.color)
        self.banners_rect = self.banners_text.get_rect()
        
        self.pisa_text = self.font.render('Pipes and Stars',True,self.color)
        self.pisa_rect = self.pisa_text.get_rect()
        
        self.pisabal_text = self.font.render('PiSaBal',True,self.color)
        self.pisabal_rect = self.pisabal_text.get_rect()
        
        self.levels_text = self.font.render('Levels',True,self.color)
        self.levels_rect = self.levels_text.get_rect()
        
        
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
        
        self.record_text = self.fonth.render('Record On/Off', True,self.colorr)
        self.record_rect = self.record_text.get_rect()


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
            if not self.GAME_TYPE['levels']:
                self.update_dict(self.GAME_MODES,'space')
                self.set_mode()

        opt_pos[0] += self.option_w
        self.screen.blit(self.smile_text,opt_pos)
        self.smile_rect.x = opt_pos[0]
        self.smile_rect.y = opt_pos[1]
        if self.smile_rect.collidepoint(pos):
            if not self.GAME_TYPE['levels'] and not self.GAME_TYPE['pisabal']:
                self.update_dict(self.GAME_MODES,'smile')
                self.set_mode()

        opt_pos[0] -= self.option_w
        opt_pos[1] += self.smile_text.get_height() + 10
        self.screen.blit(self.alt_text,opt_pos)
        self.alt_rect.x = opt_pos[0]
        self.alt_rect.y = opt_pos[1]
        if self.alt_rect.collidepoint(pos):
            if not self.GAME_TYPE['balloons'] and not self.GAME_TYPE['banners'] and not self.GAME_TYPE['levels'] and not self.GAME_TYPE['pisabal']:
                self.update_dict(self.GAME_MODES,'altitude')
                self.set_mode()
        
        opt_pos[0] += self.mode_w + self.smile_text.get_width() + 20
        opt_pos[1] = self.start_h
        self.screen.blit(self.mode_text,opt_pos)
        
        opt_pos[0] += 20
        opt_pos[1] += self.mode_text.get_height() + 10
        self.screen.blit(self.pipes_text,opt_pos)
        self.pipes_rect.x = opt_pos[0]
        self.pipes_rect.y = opt_pos[1]
        if self.pipes_rect.collidepoint(pos):
            self.update_dict(self.GAME_DIFFICULTY,'easy')
            self.set_difficulty()
        
            self.update_dict(self.GAME_TYPE,'pipes')
            self.set_type()

            self.update_dict(self.GAME_MODES,'space')
            self.set_mode()



        opt_pos[0] += self.option_w
        self.screen.blit(self.stars_text,opt_pos)
        self.stars_rect.x = opt_pos[0]
        self.stars_rect.y = opt_pos[1]
        
        if self.stars_rect.collidepoint(pos):
            self.update_dict(self.GAME_TYPE,'stars')
            self.set_type()

            self.update_dict(self.GAME_DIFFICULTY,'easy')
            self.set_difficulty(['medium','hard'])

            self.update_dict(self.GAME_MODES,'space')
            self.set_mode()
            

        opt_pos[0] -= self.option_w
        opt_pos[1] += self.stars_text.get_height() + 10
        self.screen.blit(self.balloons_text,opt_pos)
        self.balloons_rect.x = opt_pos[0]
        self.balloons_rect.y = opt_pos[1]
        if self.balloons_rect.collidepoint(pos):
            self.update_dict(self.GAME_TYPE,'balloons')
            self.set_type()
            
            self.update_dict(self.GAME_MODES,'space')
            self.set_mode(['altitude'])
            
            self.update_dict(self.GAME_DIFFICULTY,'easy')
            self.set_difficulty(['medium','hard'])

        opt_pos[0] += self.option_w
        self.screen.blit(self.pisa_text,opt_pos)
        self.pisa_rect.x = opt_pos[0]
        self.pisa_rect.y = opt_pos[1]
        if self.pisa_rect.collidepoint(pos):
            self.update_dict(self.GAME_TYPE,'pisa')
            self.set_type()
            
            self.update_dict(self.GAME_MODES,'space')
            self.set_mode()
            
            self.update_dict(self.GAME_DIFFICULTY,'easy')
            self.set_difficulty()
        
        opt_pos[0] -= self.option_w
        
        opt_pos[1] += self.balloons_text.get_height() + 10
        
        self.screen.blit(self.banners_text,opt_pos)
        self.banners_rect.x = opt_pos[0]
        self.banners_rect.y = opt_pos[1]
        if self.banners_rect.collidepoint(pos):            
            self.update_dict(self.GAME_TYPE,'banners')
            self.set_type()

            self.update_dict(self.GAME_MODES,'space')
            self.set_mode(['altitude'])


            self.update_dict(self.GAME_DIFFICULTY,'easy')
            self.set_difficulty(['medium','hard'])

        opt_pos[0] += self.option_w
        self.screen.blit(self.pisabal_text,opt_pos)
        self.pisabal_rect.x = opt_pos[0]
        self.pisabal_rect.y = opt_pos[1]
        if self.pisabal_rect.collidepoint(pos):
            self.update_dict(self.GAME_DIFFICULTY,'easy')
            self.set_difficulty()

            self.update_dict(self.GAME_TYPE,'pisabal')
            self.set_type()

            self.update_dict(self.GAME_MODES,'space')
            self.set_mode(['altitude','smile'])


        opt_pos[0] -= self.option_w
        opt_pos[1] += self.banners_text.get_height() + 10
        self.screen.blit(self.levels_text,opt_pos)
        self.levels_rect.x = opt_pos[0]
        self.levels_rect.y = opt_pos[1]
        if self.levels_rect.collidepoint(pos):
            
            self.update_dict(self.GAME_TYPE,'levels')
            self.set_type()


            self.update_dict(self.GAME_MODES,'space')
            self.set_mode(['space','smile','altitude'])

            self.update_dict(self.GAME_DIFFICULTY,'easy')
            self.set_difficulty(['easy','medium','hard','arcade'])




        opt_pos[0] = self.start_w
        opt_pos[1] = self.alt_rect.y + self.alt_text.get_height() + 20
        self.screen.blit(self.diff_text,opt_pos)

        opt_pos[0] += 20
        opt_pos[1] += self.diff_text.get_height() + 10
        self.screen.blit(self.easy_text,opt_pos)
        self.easy_rect.x = opt_pos[0]
        self.easy_rect.y = opt_pos[1]
        if self.easy_rect.collidepoint(pos):
            if not self.GAME_TYPE['levels']:
                self.update_dict(self.GAME_DIFFICULTY,'easy')

                if not self.GAME_TYPE['stars'] and not self.GAME_TYPE['balloons'] and not self.GAME_TYPE['banners']:
                    self.set_difficulty()
                else:
                    self.set_difficulty(['medium','hard'])

        opt_pos[0] += self.option_w
        self.screen.blit(self.med_text,opt_pos)
        self.med_rect.x = opt_pos[0]
        self.med_rect.y = opt_pos[1]
        if self.med_rect.collidepoint(pos):
            if not self.GAME_TYPE['stars'] and not self.GAME_TYPE['balloons'] and not self.GAME_TYPE['banners'] and not self.GAME_TYPE['levels']:
                self.update_dict(self.GAME_DIFFICULTY,'medium')
                self.set_difficulty()

        opt_pos[0] -= self.option_w
        opt_pos[1] += self.easy_text.get_height() + 10
        self.screen.blit(self.hard_text,opt_pos)
        self.hard_rect.x = opt_pos[0]
        self.hard_rect.y = opt_pos[1]
        if self.hard_rect.collidepoint(pos):
            if not self.GAME_TYPE['stars'] and not self.GAME_TYPE['balloons'] and not self.GAME_TYPE['banners'] and not self.GAME_TYPE['levels']:
                self.update_dict(self.GAME_DIFFICULTY,'hard')
                self.set_difficulty()

        opt_pos[0] += self.option_w
        self.screen.blit(self.arc_text,opt_pos)
        self.arc_rect.x = opt_pos[0]
        self.arc_rect.y = opt_pos[1]
        if self.arc_rect.collidepoint(pos):
            if not self.GAME_TYPE['levels']:
                self.update_dict(self.GAME_DIFFICULTY,'arcade')
                if not self.GAME_TYPE['stars'] and not self.GAME_TYPE['balloons'] and not self.GAME_TYPE['banners']:
                    self.set_difficulty()
                else:
                    self.set_difficulty(['medium','hard'])
                    
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


        opt_pos[0] = self.start_w
        opt_pos[1] = self.landmark_rect.y + self.landmarks_text.get_height() + 20
        self.screen.blit(self.record_text,opt_pos)
        self.record_rect.x = opt_pos[0]
        self.record_rect.y = opt_pos[1]
        if self.record_rect.collidepoint(pos):
            if self.record:
                self.record_text = self.fonth.render('Record On/Off',True,self.colorr)
                self.record = False
            else:
                self.record_text = self.fonth.render('Record On/Off',True,self.colorg)
                self.record = True

        return self.GAME_TYPE,self.GAME_MODES,self.GAME_DIFFICULTY,self.landmark,self.record
    
    def update_dict(self,dict,key):
        for k in dict.keys():
            if k == key:
                dict[k] = True
            else:
                dict[k] = False

    def set_difficulty(self,reds=[]):
        if self.GAME_DIFFICULTY['easy']:
            self.easy_text = self.font.render('Easy',True,self.colorg)
        else:
            self.easy_text = self.font.render('Easy',True,self.color)

        if self.GAME_DIFFICULTY['medium']:
            self.med_text = self.font.render('Medium',True,self.colorg)
        else:
            self.med_text = self.font.render('Medium',True,self.color)
        if self.GAME_DIFFICULTY['hard']:
            self.hard_text = self.font.render('Hard',True,self.colorg)
        else:
            self.hard_text = self.font.render('Hard',True,self.color)
        if self.GAME_DIFFICULTY['arcade']:
            self.arc_text = self.font.render('Arcade',True,self.colorg)
        else:
            self.arc_text = self.font.render('Arcade',True,self.color)
        
        for red in reds:
            if red == 'easy':
                self.easy_text = self.font.render('Easy',True,self.colorr)
            if red == 'medium':
                self.med_text = self.font.render('Medium',True,self.colorr)
            if red == 'hard':
                self.hard_text = self.font.render('Hard',True,self.colorr)
            if red == 'arcade':
                self.arc_text = self.font.render('Arcade',True,self.colorr)
        

    def set_mode(self,reds=[]):
        if self.GAME_MODES['space']:
            self.space_text = self.font.render('Space',True,self.colorg)
        else:
            self.space_text = self.font.render('Space',True,self.color)
        if self.GAME_MODES['smile']:
            self.smile_text = self.font.render('Smile',True,self.colorg)
        else:
            self.smile_text = self.font.render('Smile',True,self.color)
        if self.GAME_MODES['altitude']:
            self.alt_text = self.font.render('Altitude',True,self.colorg)
        else:
            self.alt_text = self.font.render('Altitude',True,self.color)
        
        for red in reds:
            if red == 'space':
                self.space_text = self.font.render('Space',True,self.colorr)
            if red == 'smile':
                self.smile_text = self.font.render('Smile',True,self.colorr)
            if red == 'altitude':
                self.alt_text = self.font.render('Altitude',True,self.colorr)

    def set_type(self,reds=[]):
        if self.GAME_TYPE['pipes']:
            self.pipes_text = self.font.render('Pipes',True,self.colorg)
        else:
            self.pipes_text = self.font.render('Pipes',True,self.color)
        if self.GAME_TYPE['stars']:
            self.stars_text = self.font.render('Stars',True,self.colorg)
        else:
            self.stars_text = self.font.render('Stars',True,self.color)
        if self.GAME_TYPE['balloons']:
            self.balloons_text = self.font.render('Balloons',True,self.colorg)
        else:
            self.balloons_text = self.font.render('Balloons',True,self.color)
        if self.GAME_TYPE['pisa']:
            self.pisa_text = self.font.render('Pipes and Stars',True,self.colorg)
        else:
            self.pisa_text = self.font.render('Pipes and Stars',True,self.color)
        if self.GAME_TYPE['banners']:
            self.banners_text = self.font.render('Banners',True,self.colorg)
        else:
            self.banners_text = self.font.render('Banners',True,self.color)
        if self.GAME_TYPE['pisabal']:
            self.pisabal_text = self.font.render('PiSaBal',True,self.colorg)
        else:
            self.pisabal_text = self.font.render('PiSaBal',True,self.color)
        if self.GAME_TYPE['levels']:
            self.levels_text = self.font.render('Levels',True,self.colorg)
        else:
            self.levels_text = self.font.render('Levels',True,self.color)
        


