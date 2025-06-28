#!/usr/bin/env python3
"""
Simon Says Game - Python Implementation

DESIGN NOTES AND REASONING:

1. GAME MECHANICS:
   - Simon Says is a memory game where players must repeat an increasingly longer sequence
   - The game generates random sequences and checks if the player can repeat them correctly
   - Each round adds one more step to the sequence, making it progressively harder
   - This tests working memory capacity and pattern recognition

2. TECHNICAL DECISIONS:
   - Using random.randint() for sequence generation ensures unpredictability
   - List data structure for storing sequences allows easy appending and comparison
   - Input validation prevents crashes from invalid user input
   - Clear visual feedback with print statements and formatting
   - Score tracking motivates continued play

3. USER EXPERIENCE CONSIDERATIONS:
   - Clear instructions at the start
   - Visual separation between game phases (display vs input)
   - Immediate feedback on correct/incorrect responses
   - Final score display provides closure and achievement
   - Simple input method (number keys) reduces cognitive load

4. EDUCATIONAL VALUE:
   - Demonstrates list operations (append, comparison)
   - Shows input validation and error handling
   - Illustrates game loop patterns
   - Teaches basic scoring systems
   - Shows how to create engaging user interfaces with text

5. ACCESSIBILITY:
   - Text-based interface works on any system
   - No external dependencies required
   - Clear, readable output formatting
   - Simple input method accessible to all users
"""

import random
import time
import os

class SimonSays:
    def __init__(self):
        """Initialize the game with default settings"""
        self.sequence = []
        self.score = 0
        self.colors = {
            1: "RED",
            2: "GREEN", 
            3: "BLUE",
            4: "YELLOW"
        }
        
    def clear_screen(self):
        """Clear the terminal screen for better visual experience"""
        os.system('cls' if os.name == 'nt' else 'clear')
        
    def display_welcome(self):
        """Display welcome message and game instructions"""
        print("=" * 50)
        print("🎮 SIMON SAYS GAME 🎮")
        print("=" * 50)
        print("\nHOW TO PLAY:")
        print("1. Watch the sequence of colors that Simon shows")
        print("2. Repeat the sequence by entering the numbers:")
        print("   1 = RED, 2 = GREEN, 3 = BLUE, 4 = YELLOW")
        print("3. Each round adds one more color to remember")
        print("4. Try to get the highest score possible!")
        print("\n" + "=" * 50)
        
    def generate_sequence(self, length):
        """Generate a random sequence of specified length"""
        return [random.randint(1, 4) for _ in range(length)]
        
    def display_sequence(self, sequence):
        """Display the sequence to the player with visual effects"""
        print("\n🎯 SIMON SAYS: Watch carefully!")
        print("-" * 30)
        
        for i, color_num in enumerate(sequence, 1):
            color_name = self.colors[color_num]
            print(f"Step {i}: {color_name} ({color_num})")
            time.sleep(1)  # Pause to let player see each step
            
        print("-" * 30)
        print("⏰ Time to repeat the sequence!")
        time.sleep(0.5)
        
    def get_player_input(self, sequence_length):
        """Get and validate player input for the sequence"""
        player_sequence = []
        
        print(f"\nEnter {sequence_length} numbers (1-4), one at a time:")
        
        for i in range(sequence_length):
            while True:
                try:
                    user_input = input(f"Step {i+1}: ").strip()
                    
                    # Validate input
                    if not user_input:
                        print("❌ Please enter a number!")
                        continue
                        
                    number = int(user_input)
                    
                    if number < 1 or number > 4:
                        print("❌ Please enter a number between 1 and 4!")
                        continue
                        
                    player_sequence.append(number)
                    break
                    
                except ValueError:
                    print("❌ Please enter a valid number!")
                    
        return player_sequence
        
    def check_sequence(self, original, player):
        """Compare the original sequence with player's input"""
        if len(original) != len(player):
            return False
            
        for i in range(len(original)):
            if original[i] != player[i]:
                return False
                
        return True
        
    def display_result(self, is_correct, original_sequence, player_sequence):
        """Display the result of the round"""
        print("\n" + "=" * 30)
        
        if is_correct:
            print("✅ CORRECT! Well done!")
            print(f"🎉 Your score: {self.score}")
        else:
            print("❌ WRONG! Game Over!")
            print(f"Original sequence: {[self.colors[num] for num in original_sequence]}")
            
            # Handle invalid numbers in player sequence
            player_colors = []
            for num in player_sequence:
                if num in self.colors:
                    player_colors.append(self.colors[num])
                else:
                    player_colors.append(f"INVALID({num})")
            print(f"Your sequence: {player_colors}")
            
        print("=" * 30)
        
    def play_round(self, round_num):
        """Play a single round of the game"""
        print(f"\n🎲 ROUND {round_num}")
        print("-" * 20)
        
        # Generate and display sequence
        self.sequence = self.generate_sequence(round_num)
        self.display_sequence(self.sequence)
        
        # Get player input
        player_sequence = self.get_player_input(round_num)
        
        # Check if correct
        is_correct = self.check_sequence(self.sequence, player_sequence)
        
        if is_correct:
            self.score += round_num
            self.display_result(True, self.sequence, player_sequence)
            return True
        else:
            self.display_result(False, self.sequence, player_sequence)
            return False
            
    def display_final_score(self):
        """Display the final score and game summary"""
        print("\n" + "🎯" * 20)
        print("GAME OVER!")
        print(f"Final Score: {self.score}")
        print("🎯" * 20)
        
        # Provide feedback based on score
        if self.score >= 15:
            print("🌟 EXCELLENT! You have amazing memory!")
        elif self.score >= 10:
            print("👍 GOOD JOB! You did well!")
        elif self.score >= 5:
            print("👌 NOT BAD! Keep practicing!")
        else:
            print("💪 KEEP TRYING! Practice makes perfect!")
            
    def play_game(self):
        """Main game loop"""
        self.clear_screen()
        self.display_welcome()
        
        input("\nPress Enter to start the game...")
        
        round_num = 1
        while True:
            self.clear_screen()
            
            if not self.play_round(round_num):
                break
                
            # Ask if player wants to continue
            if round_num >= 3:  # After round 3, ask if they want to continue
                continue_choice = input("\nContinue to next round? (y/n): ").lower().strip()
                if continue_choice != 'y':
                    break
                    
            round_num += 1
            
        self.display_final_score()

def main():
    """Main function to run the game"""
    print("Starting Simon Says Game...")
    
    # Create and play the game
    game = SimonSays()
    game.play_game()
    
    # Ask if player wants to play again
    while True:
        play_again = input("\nPlay again? (y/n): ").lower().strip()
        if play_again == 'y':
            game = SimonSays()  # Reset game
            game.play_game()
        elif play_again == 'n':
            print("Thanks for playing! 👋")
            break
        else:
            print("Please enter 'y' or 'n'")

if __name__ == "__main__":
    main() 