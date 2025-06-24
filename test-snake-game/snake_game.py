import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 600, 400
CELL_SIZE = 20

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# Directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Set up display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Snake Game')
clock = pygame.time.Clock()

font = pygame.font.SysFont('Arial', 25)

def draw_snake(snake):
    for segment in snake:
        pygame.draw.rect(screen, GREEN, (*segment, CELL_SIZE, CELL_SIZE))

def draw_food(position):
    pygame.draw.rect(screen, RED, (*position, CELL_SIZE, CELL_SIZE))

def random_food_position(snake):
    while True:
        x = random.randint(0, (WIDTH - CELL_SIZE) // CELL_SIZE) * CELL_SIZE
        y = random.randint(0, (HEIGHT - CELL_SIZE) // CELL_SIZE) * CELL_SIZE
        if (x, y) not in snake:
            return (x, y)

def game_over_screen(score):
    screen.fill(BLACK)
    msg = font.render(f'Game Over! Score: {score}', True, WHITE)
    screen.blit(msg, (WIDTH // 2 - msg.get_width() // 2, HEIGHT // 2 - msg.get_height() // 2 - 20))
    instr = font.render('Press R to Restart or ESC to Exit', True, WHITE)
    screen.blit(instr, (WIDTH // 2 - instr.get_width() // 2, HEIGHT // 2 - instr.get_height() // 2 + 20))
    pygame.display.flip()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return 'reset'
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

def main():
    while True:
        snake = [(WIDTH // 2, HEIGHT // 2)]
        direction = RIGHT
        food = random_food_position(snake)
        score = 0

        running = True
        start_ticks = pygame.time.get_ticks()  # Start time in milliseconds
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if (event.key == pygame.K_UP or event.key == pygame.K_w) and direction != DOWN:
                        direction = UP
                    elif (event.key == pygame.K_DOWN or event.key == pygame.K_s) and direction != UP:
                        direction = DOWN
                    elif (event.key == pygame.K_LEFT or event.key == pygame.K_a) and direction != RIGHT:
                        direction = LEFT
                    elif (event.key == pygame.K_RIGHT or event.key == pygame.K_d) and direction != LEFT:
                        direction = RIGHT

            # Move snake
            new_head = (snake[0][0] + direction[0] * CELL_SIZE, snake[0][1] + direction[1] * CELL_SIZE)
            
            # Check collisions
            if (
                new_head[0] < 0 or new_head[0] >= WIDTH or
                new_head[1] < 0 or new_head[1] >= HEIGHT or
                new_head in snake
            ):
                result = game_over_screen(score)
                if result == 'reset':
                    running = False  # Break inner loop to restart
                break

            if running:
                snake.insert(0, new_head)
                if new_head == food:
                    score += 1
                    food = random_food_position(snake)
                else:
                    snake.pop()

                screen.fill(BLACK)
                draw_snake(snake)
                draw_food(food)
                score_text = font.render(f'Score: {score}', True, WHITE)
                screen.blit(score_text, (5, 5))
                # Draw timer
                elapsed_seconds = (pygame.time.get_ticks() - start_ticks) // 1000
                time_text = font.render(f'Time: {elapsed_seconds}s', True, WHITE)
                screen.blit(time_text, (WIDTH - time_text.get_width() - 5, 5))
                pygame.display.flip()
                clock.tick(10)

if __name__ == '__main__':
    main() 