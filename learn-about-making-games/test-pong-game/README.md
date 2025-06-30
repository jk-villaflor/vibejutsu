# Pong Game

A classic Pong game implemented in Python using Pygame with computer AI and difficulty levels.

## Features

- **Two game modes**: 2 Player and vs Computer
- **Three difficulty levels**: Easy, Medium, Hard
- **Smart AI opponent** with realistic ball prediction
- **Realistic ball physics** with angle-based bouncing
- **Score tracking** (first to 11 points wins)
- **Smooth 60 FPS gameplay**
- **Modern visual design** with colored paddles
- **Menu system** for game mode and difficulty selection
- **Game over screen** with restart functionality

## Game Modes

### 2 Player Mode
- Classic two-player gameplay
- Both players control their own paddles

### vs Computer Mode
- Play against an AI opponent
- Choose from three difficulty levels:
  - **Easy**: AI makes many mistakes, easier to beat
  - **Medium**: Balanced AI with moderate accuracy
  - **Hard**: AI is very accurate and challenging

## Controls

### Menu Navigation
- `↑` (Up Arrow) / `↓` (Down Arrow) - Select game mode
- `←` (Left Arrow) / `→` (Right Arrow) - Change difficulty (in vs Computer mode)
- `ENTER` - Start game
- `ESC` - Quit game

### Game Controls
- **Left Paddle (Blue)**: 
  - `W` - Move up
  - `S` - Move down

- **Right Paddle (Red)** (2 Player mode only):
  - `↑` (Up Arrow) - Move up
  - `↓` (Down Arrow) - Move down

- **Game Controls**:
  - `R` - Restart game (when game is over)
  - `M` - Return to menu
  - `ESC` - Quit game

## Installation

1. Make sure you have Python 3.6+ installed
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Game

```bash
python pong_game.py
```

## Game Rules

- Each player controls a paddle on their side of the screen
- The ball bounces off paddles and the top/bottom walls
- If the ball passes a player's paddle, the opponent scores a point
- First player to reach 11 points wins
- The ball's bounce angle depends on where it hits the paddle

## AI Behavior

The computer AI uses advanced ball prediction:
- Calculates where the ball will be when it reaches the paddle
- Adjusts prediction accuracy based on difficulty level
- Easy: ±100 pixel error range
- Medium: ±50 pixel error range  
- Hard: ±20 pixel error range

## Technical Details

- Built with Pygame for smooth graphics and input handling
- Object-oriented design with separate classes for Paddle, Ball, Menu, and Game
- Realistic physics simulation with proper collision detection
- Responsive controls with smooth paddle movement
- Clean, modern UI with visual feedback
- State machine for menu, playing, and game over states

Enjoy playing Pong against friends or challenging the AI! 