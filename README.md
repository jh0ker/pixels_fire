# pixels_basegame
An example that can be used to create a new pixels game.

### How to use
Create a new, empty repository, clone it and execute `git pull https://github.com/HackerspaceBremen/pixels_basegame.git` (You could just fork this repository, but you can only do that once)
Change the `README.md` and `pixels_info.json` and you can start coding!

You'll probably need to add code at three locations:

#### init
In `__init__(self)` you should initialize objects and introduce all variables that you'll use globally. 

#### update
`update(self)` gets called every gameloop. Your main game logic should go here. Also, you need to paint the next frame here. Use the pygame surface `self.screen` for this, since it's the one that will be sent to the display afterwards. The example code creates a new surface, fills it with a random color and paints it to a random location on the screen on each game update.

#### process_event_queue
Before `update` is called, `process_event_queue(self)` is called to process events from the keyboard and the controller. All events from joystick and keyboard are unified to have three properties: `player`, `type` and `button`. For more info on these events, check [this](https://gist.github.com/jh0ker/8a63a66d368d7b48c89d) gist. The sample method contains no code but the if-structure for all button push events of player 1.

### Dependencies
You'll need [this](https://github.com/HackerspaceBremen/pygame-ledpixels) to play the game. 
