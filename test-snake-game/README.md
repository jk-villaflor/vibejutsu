# Snake Game Collection

This project contains two versions of the classic Snake game:
- A Python version using `pygame`
- A browser version using Phaser.js, which can be served with Node.js

---

## 1. Python Snake Game (`pygame`)

### How to Run
1. Make sure you have Python installed (version 3.6 or higher recommended).
2. Install the required dependency:
   ```bash
   pip install pygame
   ```
3. Run the game:
   ```bash
   python snake_game.py
   ```

### Controls
- Arrow keys or WASD: Move the snake
- R: Restart after game over
- ESC: Exit after game over

### Features
- Score and timer display
- Game over screen with restart/exit options

---

## 2. Snake Game (Phaser.js Version)

A browser-based version of the snake game using [Phaser 3](https://phaser.io/).

### How to Run (Recommended: Node.js Server)
1. Make sure you have [Node.js](https://nodejs.org/) installed.
2. In the `test-snake-game` folder, install dependencies:
   ```bash
   npm install
   ```
3. Start the server:
   ```bash
   npm start
   ```
4. Open your browser and go to [http://localhost:3000](http://localhost:3000)

This will serve the game using a simple Express server (`server.js`).

### Alternative: Run in Browser with Local Web Server
If you prefer, you can use any local web server (e.g., `python -m http.server` or VSCode Live Server) and open `index.html` in your browser.

### Controls
- Arrow keys or WASD: Move the snake
- R: Restart after game over
- ESC: Exit after game over

### Features
- Score and timer display
- Game over screen with restart/exit options
- Responsive and smooth gameplay
- Snake head is a darker green for clarity

---

## File List
- `snake_game.py` — Python version (pygame)
- `snake_game_phaser.js` — Phaser.js version (browser/Node.js)
- `index.html` — HTML file for browser play
- `server.js` — Node.js Express server for Phaser version
- `package.json` — Node.js dependencies and scripts 