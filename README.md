## Flappy Bird but not.


### Setup (Tested on MacOS and Ubuntu)

- git clone https://github.com/mert-o/flappybird.git  
- cd flappybird  
- conda create --name \<name\> python=3.8.*  
- conda actiave \<name\>  
- pip install -r requirements (Requires cmake)  
- python flappy.py  

### How it works?  
- Calibrate the smile:  
    -- The game gets into a calibration mode on the start of the game and also not seeing a face for 5 seconds.  
    -- Each player should calibrate the game as described in the calibration mode.  
    -- As wanted, calibration mode can be activated from the main menu.  
    
- Game modes:  
    -- Pipes: Classic Flappy bird game, try to pass through the gaps between the pipes.  
    -- Stars: An endless mode that you try to collect small stars and the big stars that add a star sticker to the head of the player.  
- Inputs:  
    -- Space: the game is played by "Space" key.  
    -- Smile: the bird jumps if the player smiles. To jump again the player should stop smiling.  
    -- Altitude: the degree of smile of the player determines how high the bird should fly. The more the player smile, the more the bird goes up.    
- Difficulties:  
    NOTE: Difficulties are only working in pipes mode.  
    -- Easy to Hard: the gap size gets smaller in harder modes.  
    -- Arcade: the game gets faster and the gap size gets smaller by time.  

- Landmarks: Demonstrates which landmarks on a face the mediapipe library is using by drawing on the player's face.

- FX: Will be used to add special effects to the game. Doesn't work right now.
    

### New:  
- Difficulty levels.  
- Now the game asks for calibration after 5 seconds of not seeing a face.  
- Two modes are combined; pipes and stars.  


### Fix:  
- Smile is not very eye dependent now.  


### Notes:  
Effects are not working right now, will do it with media pipe.  

### To do:
- Browser version  
- Multiplayer mode

### Reference:  
- The game part of this project is stemmed from: https://github.com/sourabhv/FlapPyBird
