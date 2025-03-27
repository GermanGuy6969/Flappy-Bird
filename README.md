# Flappy Bird Clone

A Python implementation of the classic Flappy Bird game using Pygame.

## Description

This is a faithful recreation of Flappy Bird featuring:
- Animated bird sprite with realistic physics
- Scrolling pipes with random heights
- Score tracking with sprite numbers
- Sound effects
- Game over screen
- Responsive controls

## Prerequisites

- Python 3.x
- Pygame library

## Installation

1. Clone this repository or download the files
2. Install Pygame if you haven't already:
```bash
pip install pygame
```
3. Make sure you have all the required assets in the correct folder structure:

```
Flappy Bird Stuff/
├── Flappy.py
└── assets/
    ├── gameobjects/
    │   ├── background-day.png
    │   ├── base.png
    │   ├── pipe-green.png
    │   ├── yellowbird-downflap.png
    │   ├── yellowbird-midflap.png
    │   └── yellowbird-upflap.png
    ├── UI/
    │   ├── gameover.png
    │   └── Numbers/
    │       └── [0-9].png
    └── Sound Efects/
        ├── die.ogg
        ├── hit.ogg
        ├── point.ogg
        └── wing.ogg
```

## How to Play

1. Run the game:
```bash
python Flappy.py
```

2. Controls:
- Press SPACE to make the bird jump/flap
- Hold SPACE to continuously flap
- Press N to add 10 points (cheat code)
- Press SPACE to restart after game over

3. Gameplay:
- Navigate the bird through gaps between pipes
- Each pipe passed = 1 point
- Hitting pipes or the ground ends the game
- Reaching 101 points wins the game

## Features

- Full sprite animations
- Sound effects for all actions
- Score display using sprite numbers
- Game over screen
- Collision detection
- Progressive difficulty

## Contributing

Feel free to fork this project and submit pull requests with improvements!

## License

This project is for educational purposes only. Flappy Bird was originally created by Dong Nguyen.
