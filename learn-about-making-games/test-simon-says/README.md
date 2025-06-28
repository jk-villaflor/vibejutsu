# Simon Says Game - Python Implementation

## 🎮 Game Overview

This repository contains **two implementations** of the classic Simon Says memory game:

1. **Text-based version** (`simon_says.py`) - Terminal-based game with keyboard input
2. **GUI version** (`simon_says_gui.py`) - Clickable interface with colored buttons

Players must watch and remember an increasingly longer sequence of colors, then repeat it back correctly.

## 🚀 Features

### Text-Based Version (`simon_says.py`)
- **Progressive Difficulty**: Each round adds one more color to remember
- **Score Tracking**: Earn points for each successful round
- **Input Validation**: Robust error handling for invalid inputs
- **Visual Feedback**: Clear, formatted output with emojis and symbols
- **Replayability**: Option to play multiple games
- **Cross-Platform**: Works on any system with Python
- **No Dependencies**: Uses only Python standard library

### GUI Version (`simon_says_gui.py`)
- **Clickable Interface**: Use mouse to click colored buttons
- **Dark Theme**: Modern dark background with high contrast
- **2x2 Grid Layout**: Compact, intuitive button arrangement
- **Visual Feedback**: Buttons flash when pressed and during sequence display
- **Real-time Scoring**: Live score updates during gameplay
- **Smooth Animations**: Button press animations and sequence timing

## 🎯 How to Play

### Text-Based Version
1. **Watch the Sequence**: Simon will show you a sequence of colors
2. **Remember the Order**: Pay attention to the order of colors shown
3. **Repeat the Sequence**: Enter the numbers corresponding to each color:
   - 1 = RED
   - 2 = GREEN
   - 3 = BLUE
   - 4 = YELLOW
4. **Progress**: Each round gets longer and more challenging
5. **Score**: Earn points for each successful round

### GUI Version
1. **Click "Start Game"**: Begin a new game session
2. **Watch the Sequence**: Colored buttons will light up in sequence
3. **Click to Repeat**: Click the buttons in the same order shown
4. **Progress**: Each round adds one more color to remember
5. **Score**: Your score updates automatically with each successful round

## 🛠️ Technical Implementation Notes

### Design Decisions

#### Text-Based Version
1. **Object-Oriented Design**: Used a `SimonSays` class to encapsulate game logic
2. **State Management**: Game state (score, sequence) is maintained within the class
3. **Input Validation**: Comprehensive validation prevents crashes and improves UX
4. **Visual Design**: Clear formatting with separators, emojis, and consistent styling
5. **Error Handling**: Graceful handling of invalid inputs and edge cases

#### GUI Version
1. **Tkinter Framework**: Uses Python's built-in GUI library for cross-platform compatibility
2. **Event-Driven Architecture**: Responds to button clicks and timer events
3. **Dark Theme Design**: Modern UI with dark background and white text
4. **Grid Layout**: 2x2 button arrangement for intuitive gameplay
5. **Animation System**: Button press feedback and sequence timing

### Key Components

#### Text-Based Version
- **`generate_sequence()`**: Creates random sequences using `random.randint()`
- **`display_sequence()`**: Shows the sequence with timed pauses for visibility
- **`get_player_input()`**: Collects and validates player input
- **`check_sequence()`**: Compares original and player sequences
- **`play_round()`**: Orchestrates a single round of gameplay
- **`play_game()`**: Main game loop with progression logic

#### GUI Version
- **`create_buttons()`**: Sets up the 2x2 grid of colored buttons
- **`show_sequence()`**: Displays the sequence with button animations
- **`user_click()`**: Handles player button clicks and validates input
- **`next_round()`**: Manages game progression and scoring
- **`start_game()`**: Initializes new game sessions

### Educational Value

This implementation demonstrates:
- **List Operations**: Appending, comparison, enumeration
- **Input/Output**: User interaction and formatted output
- **Control Flow**: Loops, conditionals, and game state management
- **Error Handling**: Try-catch blocks and input validation
- **Game Design**: Scoring systems and progressive difficulty
- **GUI Programming**: Event handling, layouts, and animations
- **UI/UX Design**: Color schemes, spacing, and user feedback

## 📋 Requirements

### Text-Based Version
- Python 3.6 or higher
- No external dependencies required

### GUI Version
- Python 3.6 or higher
- Tkinter (usually included with Python)
- On Arch Linux/CachyOS: `sudo pacman -S tk`

## 🏃‍♂️ How to Run

### Text-Based Version
1. Navigate to the game directory:
   ```bash
   cd learn-about-making-games/test-simon-says
   ```

2. Run the text-based game:
   ```bash
   python simon_says.py
   ```

3. Follow the on-screen instructions to play!

### GUI Version
1. Navigate to the game directory:
   ```bash
   cd learn-about-making-games/test-simon-says
   ```

2. Install tkinter (if not already installed):
   ```bash
   # On Arch Linux/CachyOS:
   sudo pacman -S tk
   
   # On Ubuntu/Debian:
   sudo apt-get install python3-tk
   
   # On macOS (with Homebrew):
   brew install python-tk
   ```

3. Run the GUI game:
   ```bash
   python simon_says_gui.py
   ```

4. Click "Start Game" and enjoy the clickable interface!

## 🎨 Game Flow

### Text-Based Version
```
Welcome Screen → Instructions → Round 1 → Round 2 → ... → Game Over → Final Score
```

### GUI Version
```
Welcome Screen → Start Game → Round 1 → Round 2 → ... → Game Over → Restart
```

Each round follows this pattern:
1. Display round number
2. Generate and show sequence
3. Collect player input (keyboard or mouse)
4. Validate and compare
5. Show results and update score
6. Continue or end game

## 🏆 Scoring System

Both versions use the same scoring system:
- **Round 1**: 1 point (1 color)
- **Round 2**: 2 points (2 colors)
- **Round 3**: 3 points (3 colors)
- And so on...

**Score Feedback (Text-based version):**
- 15+ points: 🌟 EXCELLENT! You have amazing memory!
- 10-14 points: 👍 GOOD JOB! You did well!
- 5-9 points: 👌 NOT BAD! Keep practicing!
- 0-4 points: 💪 KEEP TRYING! Practice makes perfect!

## 🔧 Customization Ideas

You could extend these games by:
- Adding sound effects (with external libraries like `pygame`)
- Implementing different difficulty modes
- Adding a high score system with file persistence
- Creating additional GUI themes or layouts
- Adding multiplayer support
- Implementing different color schemes or themes
- Adding accessibility features (keyboard shortcuts, screen reader support)

## 📚 Learning Objectives

This project teaches:
- **Python Fundamentals**: Variables, loops, functions, classes
- **Game Development**: Core game loop patterns
- **User Interface Design**: Both text-based and graphical UI principles
- **Input Validation**: Robust error handling
- **State Management**: Tracking game progress
- **Algorithm Design**: Sequence generation and comparison
- **GUI Programming**: Event handling, layouts, and user interaction
- **Cross-Platform Development**: Ensuring compatibility across different systems

## 🤝 Contributing

Feel free to modify and improve these games! Some ideas:
- Add new features to either version
- Improve the UI/UX design
- Optimize the code performance
- Add comprehensive tests
- Create additional game modes
- Implement sound effects or animations

## 📄 License

This is an educational project. Feel free to use and modify as needed! 