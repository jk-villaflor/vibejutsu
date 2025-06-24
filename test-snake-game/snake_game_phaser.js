// Phaser 3 Snake Game
// To run: Use with a local web server and include Phaser 3 via CDN in your HTML

const config = {
    type: Phaser.AUTO,
    width: 600,
    height: 400,
    backgroundColor: '#000000',
    parent: 'phaser-example',
    scene: {
        preload: preload,
        create: create,
        update: update
    }
};

const CELL_SIZE = 20;
const WIDTH = 600;
const HEIGHT = 400;

let snake;
let food;
let direction;
let nextDirection;
let score = 0;
let scoreText;
let timerText;
let cursors;
let wasd;
let elapsed = 0;
let gameOver = false;
let restartText;
let startTime;
let snakeRects = [];
let foodRect;

const directions = {
    left: { x: -1, y: 0 },
    right: { x: 1, y: 0 },
    up: { x: 0, y: -1 },
    down: { x: 0, y: 1 }
};

const game = new Phaser.Game(config);

function preload() {}

function create() {
    snake = [
        { x: Math.floor(WIDTH / 2 / CELL_SIZE), y: Math.floor(HEIGHT / 2 / CELL_SIZE) }
    ];
    direction = directions.right;
    nextDirection = direction;
    score = 0;
    elapsed = 0;
    gameOver = false;
    this.time.removeAllEvents();
    this.input.keyboard.resetKeys();
    startTime = this.time.now;

    // Create snake rectangles
    snakeRects = [];
    for (let i = 0; i < snake.length; i++) {
        let color = i === 0 ? 0x006400 : 0x00ff00; // Head: dark green, Body: light green
        let rect = this.add.rectangle(snake[i].x * CELL_SIZE, snake[i].y * CELL_SIZE, CELL_SIZE, CELL_SIZE, color).setOrigin(0);
        snakeRects.push(rect);
    }

    // Create food rectangle
    food = spawnFood();
    foodRect = this.add.rectangle(food.x * CELL_SIZE, food.y * CELL_SIZE, CELL_SIZE, CELL_SIZE, 0xff0000).setOrigin(0);

    scoreText = this.add.text(5, 5, 'Score: 0', { font: '20px Arial', fill: '#fff' });
    timerText = this.add.text(WIDTH - 120, 5, 'Time: 0s', { font: '20px Arial', fill: '#fff' });
    restartText = this.add.text(WIDTH / 2, HEIGHT / 2, '', { font: '24px Arial', fill: '#fff' }).setOrigin(0.5);

    cursors = this.input.keyboard.createCursorKeys();
    wasd = this.input.keyboard.addKeys({
        up: Phaser.Input.Keyboard.KeyCodes.W,
        down: Phaser.Input.Keyboard.KeyCodes.S,
        left: Phaser.Input.Keyboard.KeyCodes.A,
        right: Phaser.Input.Keyboard.KeyCodes.D,
        r: Phaser.Input.Keyboard.KeyCodes.R,
        esc: Phaser.Input.Keyboard.KeyCodes.ESC
    });

    this.time.addEvent({ delay: 80, callback: moveSnake, callbackScope: this, loop: true });
}

function update(time, delta) {
    if (gameOver) {
        if (Phaser.Input.Keyboard.JustDown(wasd.r)) {
            this.scene.restart();
        } else if (Phaser.Input.Keyboard.JustDown(wasd.esc)) {
            this.game.destroy(true);
        }
        return;
    }

    // Controls
    if ((cursors.left.isDown || wasd.left.isDown) && direction !== directions.right) {
        nextDirection = directions.left;
    } else if ((cursors.right.isDown || wasd.right.isDown) && direction !== directions.left) {
        nextDirection = directions.right;
    } else if ((cursors.up.isDown || wasd.up.isDown) && direction !== directions.down) {
        nextDirection = directions.up;
    } else if ((cursors.down.isDown || wasd.down.isDown) && direction !== directions.up) {
        nextDirection = directions.down;
    }

    // Timer
    let newElapsed = Math.floor((time - startTime) / 1000);
    if (newElapsed !== elapsed) {
        elapsed = newElapsed;
        timerText.setText('Time: ' + elapsed + 's');
    }
}

function moveSnake() {
    if (gameOver) return;
    direction = nextDirection;
    const head = { x: snake[0].x + direction.x, y: snake[0].y + direction.y };

    // Check collisions
    if (
        head.x < 0 || head.x >= WIDTH / CELL_SIZE ||
        head.y < 0 || head.y >= HEIGHT / CELL_SIZE ||
        snake.some(segment => segment.x === head.x && segment.y === head.y)
    ) {
        gameOver = true;
        restartText.setText('Game Over! Score: ' + score + '\nTime: ' + elapsed + 's\nPress R to Restart or ESC to Exit');
        return;
    }

    snake.unshift(head);
    // Add new rectangle for new head
    let scene = this.scene ? this : this.scene;
    let headRect = scene.add.rectangle(head.x * CELL_SIZE, head.y * CELL_SIZE, CELL_SIZE, CELL_SIZE, 0x006400).setOrigin(0); // Dark green for head
    snakeRects.unshift(headRect);

    if (head.x === food.x && head.y === food.y) {
        score++;
        scoreText.setText('Score: ' + score);
        food = spawnFood();
        foodRect.setPosition(food.x * CELL_SIZE, food.y * CELL_SIZE);
    } else {
        // Remove tail
        snake.pop();
        let tailRect = snakeRects.pop();
        tailRect.destroy();
    }

    // Update all snake rect positions (should only need to update new head and removed tail)
    // (Handled above by adding/removing rects)
}

function draw(scene) {
    scene.children.removeAll();
    scene.add.text(5, 5, 'Score: ' + score, { font: '20px Arial', fill: '#fff' });
    scene.add.text(WIDTH - 120, 5, 'Time: ' + elapsed + 's', { font: '20px Arial', fill: '#fff' });
    if (gameOver) {
        scene.add.text(WIDTH / 2, HEIGHT / 2, 'Game Over! Score: ' + score + '\nTime: ' + elapsed + 's\nPress R to Restart or ESC to Exit', { font: '24px Arial', fill: '#fff', align: 'center' }).setOrigin(0.5);
    }
    // Draw snake
    snakeRects.forEach(rect => {
        scene.add.rectangle(rect.x, rect.y, CELL_SIZE, CELL_SIZE, 0x00ff00).setOrigin(0);
    });
    // Draw food
    scene.add.rectangle(foodRect.x, foodRect.y, CELL_SIZE, CELL_SIZE, 0xff0000).setOrigin(0);
}

function spawnFood() {
    let position;
    while (true) {
        position = {
            x: Phaser.Math.Between(0, (WIDTH - CELL_SIZE) / CELL_SIZE),
            y: Phaser.Math.Between(0, (HEIGHT - CELL_SIZE) / CELL_SIZE)
        };
        if (!snake.some(segment => segment.x === position.x && segment.y === position.y)) {
            return position;
        }
    }
} 