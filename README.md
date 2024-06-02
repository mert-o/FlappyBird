## Flappy Bird but not.

A flappy bird variant where the player smiles for jumps.

### Setup (Tested on MacOS/Ubuntu/Windows 10)

- git clone https://github.com/mert-o/flappybird.git  
- cd flappybird 
- If you have conda: 
    - conda create --name \<name\> python=3.8.*  
    - conda actiave \<name\>  
- pip install -r requirements
- python flappy.py    

### How it works?  
- Calibrate the smile:  
    -- The game gets into a calibration mode on the start of the game, follow the instructions and also try to control the bird.  
    -- Each player should calibrate the game as described in the calibration mode.  
    -- As wanted, calibration mode can be activated from the main menu.  

- Setting new player:  
    -- You can change the current player by clicking the name of the current player on the right top of the screen.   
- Game modes:  
    -- Pipes: Classic Flappy bird game, try to pass through the gaps between the pipes.  
    -- Stars: An endless mode that you try to collect small stars and the big stars that add a star sticker to the head of the player.  
    -- Balloons: A bird holds an AK47... ( yes, a bird, not your typical bird)  
    -- The rest are combination of above modes.
- Inputs:  
    -- Space: the game is played by "Space" key.  
    -- Smile: the bird jumps if the player smiles. To jump again the player should stop smiling.  
    -- Altitude: the degree of smile of the player determines how high the bird should fly. The more the player smile, the more the bird goes up.  
    **Note**: Altitude mode is not available in Balloons/Banners mode.
- Difficulties:  
    -- Easy to Hard: the gap size gets smaller in harder modes.  
    -- Arcade: the game gets faster and the gap size gets smaller by time.  
    **NOTE**: Difficulties are only working in Pipes, Pipes&Stars and Pipes&Stars&Balloons modes.   
- Adding new avatars:  
    -- Go to the sprites/avatars folder and add any image you want that is either ".jpg" or ".png".  
- Landmarks: Demonstrates which landmarks on a face the mediapipe library is using by drawing on the player's face.

### Building Standalone Executable (Windows 10):
- I have used Pyinstaller for Windows 10 exe.
- Install the Pyinstaller: pip install pyinstaller
- Run ``` pyinstaller flappy.py --add-data assets;assets --add-data scores.json;. --add-data last_player.txt;. --add-data words.txt;. --windowed ```
- This doesn't include the dependencies for mediapie, so should be added by hand.
- The above command will create a flappy.spec file. In that file add:
 ```
 def get_mediapipe_path():
    import mediapipe
    mediapipe_path = mediapipe.__path__[0]
    return mediapipe_path
 ``` 
after the line: 
 ```
 block_cipher = None 
 ``` 
and add:
```
mediapipe_tree = Tree(get_mediapipe_path(), prefix='mediapipe', excludes=["*.pyc"])
a.datas += mediapipe_tree
a.binaries = filter(lambda x: 'mediapipe' not in x[0], a.binaries)
``` 
after the line:
```
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)
```  
- Now, run: 
```
pyinstaller flappy.spec
```