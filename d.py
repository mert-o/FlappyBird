def mainGame():
    global LANDMARKS,GAME_MODES,HOPPED,min_smile,max_smile,mins_l,maxs_l,BIG_STAR,high_scores,BASES_LIST,GAME_DIFFICULTY,PIPEGAPSIZE,gt,gm,gd
    landmark.num_stars = 0

    score = 0
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
        newPipe1 = getRandomPipe()
        newPipe2 = getRandomPipe()
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
    elif GAME_TYPE['stars']:
        stars = [getNewStar(),getNewStar()]
        stars[0]['x'] = int(SCREENWIDTH*0.5)
        stars[1]['x'] = int(SCREENWIDTH*0.8)
    elif GAME_TYPE['balloons']:
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
        water_balls_count = 1
    
    elif GAME_TYPE['banners']:
        BANNERW = 150
        BANNERH = 150
        
        WATERBALLW = 30
        WATERBALLH = 20

        WB = False
        b_paths = glob.glob('./assets/banners/*.png')
        b = random.choice(b_paths)
        good = False
        if 'good' in b.split('/')[-1].split('.')[0]:
            good = True
        
        banners = [Banners(b,SCREENWIDTH,SCREENHEIGHT,BANNERW,BANNERH,good)]
        water_balls = []
        score_streak = 0
        water_balls_count = 1
        
    elif GAME_TYPE['pisa']:
        stars = [getNewStar(),getNewStar()]
        stars[0]['x'] = int(SCREENWIDTH*0.5)
        stars[1]['x'] = int(SCREENWIDTH*0.8)

        newPipe1 = getRandomPipe()
        newPipe2 = getRandomPipe()
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
    
    elif GAME_TYPE['pisabal']:
        
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
        water_balls_count = 1
        
        
        stars = [getNewStar(),getNewStar()]
        stars[0]['x'] = int(SCREENWIDTH*0.5)
        stars[1]['x'] = int(SCREENWIDTH*0.8)

        newPipe1 = getRandomPipe()
        newPipe2 = getRandomPipe()
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
        
    
    
    pipeVelXBase = -0.25 #128
    starVelXBase = -0.25 #128

    #speeds
    
    BALLOONS = 0.1 #70
    if GAME_TYPE['pisabal']:
        BALLOONS = 0.25
    BANNERS = 0.1 #70 
    WATERBALLS = 0.45 #200 
    birdy_speed = 0.3 #150
    baseVelx = -0.25 #128
    
    
    playerVelY = 0 
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
                            water_balls.append(WaterBall(playerx+IMAGES['player'][0].get_width() + 5 + i*WATERBALLW,playery + 15,WATERBALLW,WATERBALLH,WATERBALLS))
                    else:
                        if playery > 3 * IMAGES['player'][0].get_height():
                            playerVelY = playerAccY * spaceConst
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
            """ if not HOPPED:
                if landmark.smile_level > -1 * (min_smile*1.2)//1 * -1:
                    mag = (landmark.smile_level - min_smile) * (max_acc - min_acc) / (max_smile - min_smile)  + min_acc
                    if mag > max_acc or landmark.smile_level>=max_smile*0.75 : mag = max_acc
                    if mag < min_acc: mag = min_acc
                    playerVelY = mag * smileConst
                    if not NOSOUND: SOUNDS['wing'].play()
                    HOPPED = True """
        elif landmark.smile_level<=-1*(min_smile*1.2)//1*-1 and HOPPED:
            HOPPED = False
        
        if GAME_MODES["smile"] or GAME_TYPE["pisabal"]:
            descentSpeed = 0.65
            if GAME_TYPE['balloons'] or GAME_TYPE['banners'] or GAME_TYPE['pisabal']:
                if not WB and  landmark.smile_level > -1 * (min_smile*1.2)//1 * -1:
                    mag = (landmark.smile_level - min_smile) * (max_acc - min_acc) / (max_smile - min_smile)  + min_acc
                    if mag > max_acc or landmark.smile_level>=max_smile*0.75 :
                        for i in range(water_balls_count):
                            water_balls.append(WaterBall(playerx+IMAGES['player'][0].get_width() + 5+ i * WATERBALLW,playery +15,WATERBALLW,WATERBALLH,WATERBALLS))
                        WB = True
                elif landmark.smile_level<=-1*(min_smile*1.2)//1*-1 and WB:
                    WB = False
            elif not GAME_TYPE['pisabal']:
                if not HOPPED:
                    if landmark.smile_level > -1 * (min_smile*1.2)//1 * -1:
                        mag = (landmark.smile_level - min_smile) * (max_acc - min_acc) / (max_smile - min_smile)  + min_acc
                        if mag > max_acc or landmark.smile_level>=max_smile*0.75 : mag = max_acc
                        if mag < min_acc: mag = min_acc
                        playerVelY = mag * smileConst
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
                    playery -= playerVelY *dt
                else: playerVelY = 0
            if playerVelY<0:
                if playery < SCREENHEIGHT - IMAGES['base'].get_height() - IMAGES['player'][playerIndex].get_height():
                    playery -= playerVelY * dt
            if playerVelY > -9:
                playerVelY -= descentSpeed * dt
            
            rotation = (playerVelY - playerMinAcc) * (maxAngle - minAngle) / (playerAccY -playerMinAcc)  +minAngle
            playerSurface = pygame.transform.rotate(IMAGES['player'][playerIndex], rotation)

        else:
            if playery < 5: playery = 5
            elif playery > SCREENHEIGHT-IMAGES['base'].get_height()-IMAGES['player'][playerIndex].get_height():
                playery = SCREENHEIGHT-IMAGES['base'].get_height()-IMAGES['player'][playerIndex].get_height()
            playerSurface = IMAGES['player'][playerIndex]


        
        SCREEN.blit(playerSurface, (playerx, playery))
        
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
                if (score+1) % 15 == 0:
                    if score not in proccessed_scores:
                        proccessed_scores.append(score)
                        BIG_STAR = True
                if not NOSOUND: SOUNDS['point'].play() 
                
            # move star to left
            for star in stars:
                star['x'] += starVelXBase * dt
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

        elif GAME_TYPE['pipes']:
            playerMidPos = (playerx,playery)
            if checkCrash(playerMidPos,upperPipes,lowerPipes):
                return {
                    'score':score,
                    'y': playery,
                    'up': upperPipes,
                    'lp': lowerPipes
                }
            else:
                for i in range(len(upperPipes)):
                    if playerMidPos[0] >= upperPipes[i]['x'] + IMAGES['pipe'][0].get_width()//2 and not upperPipes[i]['score']:
                        score += 1
                        upperPipes[i]['score'] = True
                        if not NOSOUND: SOUNDS['point'].play()
                    upperPipes[i]['x'] += pipeVelXBase * dt
                    lowerPipes[i]['x'] += pipeVelXBase * dt

                    SCREEN.blit(IMAGES['pipe'][0],(upperPipes[i]['x'],upperPipes[i]['y']))
                    SCREEN.blit(IMAGES['pipe'][1],(lowerPipes[i]['x'],lowerPipes[i]['y']))

                if upperPipes[-1]['x'] <= SCREENWIDTH*0.6:
                    newPipe = getRandomPipe()
                    upperPipes.append(newPipe[0])
                    lowerPipes.append(newPipe[1])
                    

                if len(upperPipes)>0 and upperPipes[0]['x'] < - IMAGES['pipe'][0].get_width():
                    upperPipes.pop(0)
                    lowerPipes.pop(0)

            if GAME_DIFFICULTY["arcade"] and time.time() - start_time > 3:
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
        
        elif GAME_TYPE['balloons']:
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
                            if b.color =='r':
                                if score >0:
                                    score -=1
                                    score_streak = 0
                                    water_balls_count = 1
                            else:
                                score += 1
                                score_streak += 1
                                if score_streak %5 == 0:
                                    water_balls_count += 1
            if water_balls and water_balls[-1].getx()>SCREENWIDTH:
                water_balls.pop(-1)

            if time.time() - start_time> 3:
                index = random.randint(0,len(words)-1)
                balloons.append(Balloon(words[index][1],words[index][0],SCREENWIDTH,SCREENHEIGHT,BALLOONW,BALLOONH))
                start_time = time.time()
                
        elif GAME_TYPE['banners']:
            
            if banners[0].getx() + banners[0].w < 0:
                banners.pop(0)
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
                                if score >0:
                                    score -=1
                                    score_streak = 0
                                    water_balls_count = 1
                            else:
                                score += 1
                                score_streak += 1
                                if score_streak %5 == 0:
                                    water_balls_count += 1
            if water_balls and water_balls[-1].getx()>SCREENWIDTH:
                water_balls.pop(-1)

            if time.time() - start_time> 3:
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
                    landmark.num_stars += 1
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
                star['x'] += starVelXBase * dt
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
                    'lp': lowerPipes
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

                if len(upperPipes)>0 and upperPipes[0]['x'] < - IMAGES['pipe'][0].get_width():
                    upperPipes.pop(0)
                    lowerPipes.pop(0)

            if GAME_DIFFICULTY["arcade"] and time.time() - start_time > 3:
                pipeVelXBase  -= 5
                starVelXBase -= 5
                pipeVelX = pipeVelXBase * dt
                starVelX = starVelXBase * dt
                if PIPEGAPSIZE > IMAGES['player'][0].get_height() * 2.5:
                    PIPEGAPSIZE -= 4
                descentSpeed += 0.06
                #if spaceConst 
                spaceConst += 0.01
                smileConst += 0.01
                altitudeConst += 0.01
                start_time = time.time()

        elif GAME_TYPE['pisabal']:
            
            
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
                if (score+1) % 15 == 0:
                    if score not in proccessed_scores:
                        proccessed_scores.append(score)
                        BIG_STAR = True
                if not NOSOUND: SOUNDS['point'].play() 
                
            # move star to left
            for star in stars:
                star['x'] += starVelXBase * dt
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
                    'lp': lowerPipes
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

                if len(upperPipes)>0 and upperPipes[0]['x'] < - IMAGES['pipe'][0].get_width():
                    upperPipes.pop(0)
                    lowerPipes.pop(0)

            
            if GAME_DIFFICULTY["arcade"] and time.time() - start_time > 3:
                pipeVelXBase  -= 5
                starVelXBase -= 5
                pipeVelX = pipeVelXBase * dt
                starVelX = starVelXBase * dt
                if PIPEGAPSIZE > IMAGES['player'][0].get_height() * 2.5:
                    PIPEGAPSIZE -= 4
                descentSpeed += 0.06
                #if spaceConst 
                spaceConst += 0.01
                smileConst += 0.01
                altitudeConst += 0.01
                start_time = time.time()
        
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
                            if b.color =='r':
                                if score >0:
                                    score -=1
                                    score_streak = 0
                                    water_balls_count = 1
                            else:
                                score += 1
                                score_streak += 1
                                if score_streak %5 == 0:
                                    water_balls_count += 1
            if water_balls and water_balls[-1].getx()>SCREENWIDTH:
                water_balls.pop(-1)

            if time.time() - start_time> 3:
                index = random.randint(0,len(words)-1)
                balloons.append(Balloon(words[index][1],words[index][0],SCREENWIDTH,SCREENHEIGHT,BALLOONW,BALLOONH))
                start_time = time.time()
        
        showScore(score)
        

        if iterloop %5 == 0:
            playerIndex = next(playerIndexGen)
            
        iterloop = (iterloop + 1) % 30      
        
        if BASES_LIST[0]['x'] + IMAGES['base'].get_width()<=0:
            BASES_LIST.pop(0)

        if len(BASES_LIST)<3:
            BASES_LIST.append({'x':BASES_LIST[-1]['x']+IMAGES['base'].get_width(),'y':SCREENHEIGHT*0.1})
        for base in BASES_LIST:
            base['x'] += baseVelx * dt
            SCREEN.blit(IMAGES['base'],(base['x'],int(SCREENHEIGHT-IMAGES['base'].get_height())))
        
        
    

        pygame.display.update()