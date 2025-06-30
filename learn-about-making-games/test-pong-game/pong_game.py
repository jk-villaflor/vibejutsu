import pygame
import sys
import random
import math

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PADDLE_WIDTH = 15
PADDLE_HEIGHT = 90
BALL_SIZE = 15
PADDLE_SPEED = 5
BALL_SPEED = 7
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
BLUE = (0, 100, 255)
RED = (255, 100, 100)
GREEN = (100, 255, 100)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)

# Game states
MENU = "menu"
PLAYING = "playing"
GAME_OVER = "game_over"

# Difficulty levels
EASY = "easy"
MEDIUM = "medium"
HARD = "hard"

class Paddle:
    def __init__(self, x, y, color, is_ai=False):
        self.rect = pygame.Rect(x, y, PADDLE_WIDTH, PADDLE_HEIGHT)
        self.color = color
        self.speed = PADDLE_SPEED
        self.score = 0
        self.is_ai = is_ai
        
    def move(self, up=True):
        if up and self.rect.top > 0:
            self.rect.y -= self.speed
        elif not up and self.rect.bottom < SCREEN_HEIGHT:
            self.rect.y += self.speed
            
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        # Add a subtle border
        pygame.draw.rect(screen, WHITE, self.rect, 2)

class Ball:
    def __init__(self):
        self.rect = pygame.Rect(SCREEN_WIDTH // 2 - BALL_SIZE // 2,
                               SCREEN_HEIGHT // 2 - BALL_SIZE // 2,
                               BALL_SIZE, BALL_SIZE)
        self.speed_x = BALL_SPEED * random.choice([-1, 1])
        self.speed_y = BALL_SPEED * random.choice([-1, 1])
        self.color = WHITE
        
    def move(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        
    def bounce(self, paddle):
        # Calculate the relative intersection point
        relative_intersect_y = (paddle.rect.centery - self.rect.centery)
        normalized_intersect = relative_intersect_y / (PADDLE_HEIGHT / 2)
        
        # Bounce angle (max 60 degrees)
        bounce_angle = normalized_intersect * math.pi / 3
        
        # Determine direction based on which paddle was hit
        if self.speed_x > 0:  # Ball was moving right
            self.speed_x = -BALL_SPEED * math.cos(bounce_angle)
        else:  # Ball was moving left
            self.speed_x = BALL_SPEED * math.cos(bounce_angle)
            
        self.speed_y = -BALL_SPEED * math.sin(bounce_angle)
        
    def reset(self):
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.speed_x = BALL_SPEED * random.choice([-1, 1])
        self.speed_y = BALL_SPEED * random.choice([-1, 1])
        
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        # Add a subtle glow effect
        pygame.draw.rect(screen, GRAY, self.rect, 1)

class Menu:
    def __init__(self, screen, font, small_font):
        self.screen = screen
        self.font = font
        self.small_font = small_font
        self.selected_option = 0
        self.game_mode = "2 Player"  # Default
        self.difficulty = MEDIUM  # Default
        self.options = ["2 Player", "vs Computer"]
        self.difficulties = [EASY, MEDIUM, HARD]
        self.difficulty_names = {"easy": "Easy", "medium": "Medium", "hard": "Hard"}
        
    def handle_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_option = (self.selected_option - 1) % len(self.options)
            elif event.key == pygame.K_DOWN:
                self.selected_option = (self.selected_option + 1) % len(self.options)
            elif event.key == pygame.K_LEFT:
                if self.selected_option == 1:  # vs Computer selected
                    current_idx = self.difficulties.index(self.difficulty)
                    self.difficulty = self.difficulties[(current_idx - 1) % len(self.difficulties)]
            elif event.key == pygame.K_RIGHT:
                if self.selected_option == 1:  # vs Computer selected
                    current_idx = self.difficulties.index(self.difficulty)
                    self.difficulty = self.difficulties[(current_idx + 1) % len(self.difficulties)]
            elif event.key == pygame.K_RETURN:
                self.game_mode = self.options[self.selected_option]
                return True
        return False
        
    def draw(self):
        self.screen.fill(BLACK)
        
        # Title
        title = self.font.render("PONG GAME", True, WHITE)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 100))
        self.screen.blit(title, title_rect)
        
        # Game mode options
        for i, option in enumerate(self.options):
            color = YELLOW if i == self.selected_option else WHITE
            text = self.small_font.render(option, True, color)
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, 250 + i * 50))
            self.screen.blit(text, text_rect)
            
            # Show difficulty selection for vs Computer
            if i == 1 and self.selected_option == 1:
                diff_text = self.small_font.render(f"Difficulty: {self.difficulty_names[self.difficulty]}", True, GREEN)
                diff_rect = diff_text.get_rect(center=(SCREEN_WIDTH // 2, 350))
                self.screen.blit(diff_text, diff_rect)
        
        # Instructions
        instructions = [
            "Use UP/DOWN to select game mode",
            "Use LEFT/RIGHT to change difficulty (vs Computer)",
            "Press ENTER to start game",
            "Press ESC to quit"
        ]
        
        for i, instruction in enumerate(instructions):
            text = self.small_font.render(instruction, True, GRAY)
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, 450 + i * 30))
            self.screen.blit(text, text_rect)
        
        pygame.display.flip()

class PongGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Pong Game")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 74)
        self.small_font = pygame.font.Font(None, 36)
        
        # Game state
        self.state = MENU
        self.menu = Menu(self.screen, self.font, self.small_font)
        
        # Game objects (will be initialized when game starts)
        self.left_paddle = None
        self.right_paddle = None
        self.ball = None
        self.game_active = True
        self.winner = None
        
    def initialize_game(self):
        # Create game objects based on menu selection
        self.left_paddle = Paddle(50, SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2, BLUE, False)
        
        if self.menu.game_mode == "vs Computer":
            self.right_paddle = Paddle(SCREEN_WIDTH - 50 - PADDLE_WIDTH, 
                                      SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2, RED, True)
        else:
            self.right_paddle = Paddle(SCREEN_WIDTH - 50 - PADDLE_WIDTH, 
                                      SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2, RED, False)
        
        self.ball = Ball()
        self.game_active = True
        self.winner = None
        
    def ai_move(self):
        if not self.right_paddle.is_ai or not self.game_active:
            return
            
        # Predict where the ball will be when it reaches the paddle
        if self.ball.speed_x > 0:  # Ball moving towards AI
            # Calculate time to reach paddle
            time_to_paddle = (self.right_paddle.rect.left - self.ball.rect.right) / self.ball.speed_x
            
            # Predict ball's Y position
            predicted_y = self.ball.rect.centery + (self.ball.speed_y * time_to_paddle)
            
            # Add difficulty-based error
            if self.menu.difficulty == EASY:
                error = random.uniform(-100, 100)
            elif self.menu.difficulty == MEDIUM:
                error = random.uniform(-50, 50)
            else:  # HARD
                error = random.uniform(-20, 20)
                
            predicted_y += error
            
            # Move paddle towards predicted position
            paddle_center = self.right_paddle.rect.centery
            if predicted_y < paddle_center - 10:
                self.right_paddle.move(up=True)
            elif predicted_y > paddle_center + 10:
                self.right_paddle.move(up=False)
        
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if self.state == MENU:
                    if self.menu.handle_input(event):
                        self.initialize_game()
                        self.state = PLAYING
                elif event.key == pygame.K_r and self.state == GAME_OVER:
                    self.reset_game()
                elif event.key == pygame.K_ESCAPE:
                    if self.state == PLAYING:
                        self.state = MENU
                    else:
                        return False
                elif event.key == pygame.K_m and self.state == PLAYING:
                    self.state = MENU
        return True
        
    def handle_input(self):
        if self.state != PLAYING:
            return
            
        keys = pygame.key.get_pressed()
        
        # Left paddle (W/S keys)
        if keys[pygame.K_w]:
            self.left_paddle.move(up=True)
        if keys[pygame.K_s]:
            self.left_paddle.move(up=False)
            
        # Right paddle (Up/Down arrows) - only if not AI
        if not self.right_paddle.is_ai:
            if keys[pygame.K_UP]:
                self.right_paddle.move(up=True)
            if keys[pygame.K_DOWN]:
                self.right_paddle.move(up=False)
            
    def update(self):
        if self.state != PLAYING or not self.game_active:
            return
            
        # AI move
        self.ai_move()
        
        # Move ball
        self.ball.move()
        
        # Ball collision with top and bottom
        if self.ball.rect.top <= 0 or self.ball.rect.bottom >= SCREEN_HEIGHT:
            self.ball.speed_y *= -1
            
        # Ball collision with paddles
        if self.ball.rect.colliderect(self.left_paddle.rect):
            self.ball.bounce(self.left_paddle)
        elif self.ball.rect.colliderect(self.right_paddle.rect):
            self.ball.bounce(self.right_paddle)
            
        # Ball out of bounds
        if self.ball.rect.left <= 0:
            self.right_paddle.score += 1
            self.ball.reset()
            if self.right_paddle.score >= 11:
                self.game_active = False
                self.winner = "Right Player" if not self.right_paddle.is_ai else "Computer"
                self.state = GAME_OVER
        elif self.ball.rect.right >= SCREEN_WIDTH:
            self.left_paddle.score += 1
            self.ball.reset()
            if self.left_paddle.score >= 11:
                self.game_active = False
                self.winner = "Left Player"
                self.state = GAME_OVER
                
    def draw(self):
        if self.state == MENU:
            self.menu.draw()
            return
            
        # Clear screen
        self.screen.fill(BLACK)
        
        # Draw center line
        for y in range(0, SCREEN_HEIGHT, 20):
            pygame.draw.rect(self.screen, GRAY, 
                           (SCREEN_WIDTH // 2 - 2, y, 4, 10))
        
        # Draw game objects
        self.left_paddle.draw(self.screen)
        self.right_paddle.draw(self.screen)
        self.ball.draw(self.screen)
        
        # Draw scores
        left_score = self.font.render(str(self.left_paddle.score), True, BLUE)
        right_score = self.font.render(str(self.right_paddle.score), True, RED)
        
        self.screen.blit(left_score, (SCREEN_WIDTH // 4, 20))
        self.screen.blit(right_score, (3 * SCREEN_WIDTH // 4, 20))
        
        # Draw game mode info
        mode_text = self.small_font.render(self.menu.game_mode, True, WHITE)
        self.screen.blit(mode_text, (10, 10))
        
        if self.menu.game_mode == "vs Computer":
            diff_text = self.small_font.render(f"Difficulty: {self.menu.difficulty_names[self.menu.difficulty]}", True, WHITE)
            self.screen.blit(diff_text, (10, 40))
        
        # Draw game over screen
        if self.state == GAME_OVER:
            # Semi-transparent overlay
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.set_alpha(128)
            overlay.fill(BLACK)
            self.screen.blit(overlay, (0, 0))
            
            # Winner text
            winner_text = self.font.render(f"{self.winner} Wins!", True, WHITE)
            winner_rect = winner_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
            self.screen.blit(winner_text, winner_rect)
            
            # Instructions
            restart_text = self.small_font.render("Press R to restart, M for menu, or ESC to quit", True, WHITE)
            restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
            self.screen.blit(restart_text, restart_rect)
        else:
            # Draw controls info
            if self.menu.game_mode == "2 Player":
                controls_text = self.small_font.render("W/S - Left Paddle | Up/Down - Right Paddle", True, GRAY)
            else:
                controls_text = self.small_font.render("W/S - Your Paddle | M - Menu", True, GRAY)
            self.screen.blit(controls_text, (10, SCREEN_HEIGHT - 30))
        
        pygame.display.flip()
        
    def reset_game(self):
        self.initialize_game()
        
    def run(self):
        running = True
        while running:
            running = self.handle_events()
            
            if self.state == PLAYING:
                self.handle_input()
                self.update()
                
            self.draw()
            self.clock.tick(FPS)
            
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = PongGame()
    game.run() 