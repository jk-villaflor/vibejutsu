#!/usr/bin/env python3
"""
Simple test script to verify menu navigation works
"""

import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
YELLOW = (255, 255, 0)
GREEN = (100, 255, 100)

# Game states
MENU = "menu"
PLAYING = "playing"

# Difficulty levels
EASY = "easy"
MEDIUM = "medium"
HARD = "hard"

class Menu:
    def __init__(self, screen, font, small_font):
        self.screen = screen
        self.font = font
        self.small_font = small_font
        self.selected_option = 0
        self.game_mode = "2 Player"
        self.difficulty = MEDIUM
        self.options = ["2 Player", "vs Computer"]
        self.difficulties = [EASY, MEDIUM, HARD]
        self.difficulty_names = {"easy": "Easy", "medium": "Medium", "hard": "Hard"}
        
    def handle_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_option = (self.selected_option - 1) % len(self.options)
                print(f"Selected option: {self.options[self.selected_option]}")
            elif event.key == pygame.K_DOWN:
                self.selected_option = (self.selected_option + 1) % len(self.options)
                print(f"Selected option: {self.options[self.selected_option]}")
            elif event.key == pygame.K_LEFT:
                if self.selected_option == 1:  # vs Computer selected
                    current_idx = self.difficulties.index(self.difficulty)
                    self.difficulty = self.difficulties[(current_idx - 1) % len(self.difficulties)]
                    print(f"Difficulty: {self.difficulty_names[self.difficulty]}")
            elif event.key == pygame.K_RIGHT:
                if self.selected_option == 1:  # vs Computer selected
                    current_idx = self.difficulties.index(self.difficulty)
                    self.difficulty = self.difficulties[(current_idx + 1) % len(self.difficulties)]
                    print(f"Difficulty: {self.difficulty_names[self.difficulty]}")
            elif event.key == pygame.K_RETURN:
                self.game_mode = self.options[self.selected_option]
                print(f"Starting game: {self.game_mode}")
                return True
        return False
        
    def draw(self):
        self.screen.fill(BLACK)
        
        title = self.font.render("PONG GAME - MENU TEST", True, WHITE)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 100))
        self.screen.blit(title, title_rect)
        
        for i, option in enumerate(self.options):
            color = YELLOW if i == self.selected_option else WHITE
            text = self.small_font.render(option, True, color)
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, 250 + i * 50))
            self.screen.blit(text, text_rect)
            
            if i == 1 and self.selected_option == 1:
                diff_text = self.small_font.render(f"Difficulty: {self.difficulty_names[self.difficulty]}", True, GREEN)
                diff_rect = diff_text.get_rect(center=(SCREEN_WIDTH // 2, 350))
                self.screen.blit(diff_text, diff_rect)
        
        instructions = [
            "Use UP/DOWN to select game mode",
            "Use LEFT/RIGHT to change difficulty (vs Computer)",
            "Press ENTER to start game",
            "Press ESC to quit",
            "Check console for navigation feedback"
        ]
        
        for i, instruction in enumerate(instructions):
            text = self.small_font.render(instruction, True, GRAY)
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, 450 + i * 30))
            self.screen.blit(text, text_rect)
        
        pygame.display.flip()

def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Menu Test")
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 74)
    small_font = pygame.font.Font(None, 36)
    
    menu = Menu(screen, font, small_font)
    state = MENU
    
    print("Menu test started. Use arrow keys to navigate.")
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif state == MENU:
                    if menu.handle_input(event):
                        print("Game would start now!")
                        # For testing, just reset
                        menu.selected_option = 0
                        menu.game_mode = "2 Player"
                        menu.difficulty = MEDIUM
        
        if state == MENU:
            menu.draw()
        
        clock.tick(FPS)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main() 