import tkinter as tk
import random

# Color mapping for the game
COLORS = {1: "red", 2: "green", 3: "blue", 4: "yellow"}

class SimonSaysGUI:
    def __init__(self, root):
        self.root = root
        self.root.configure(bg='#2b2b2b')  # Dark background
        self.sequence = []
        self.user_sequence = []
        self.round = 1
        self.buttons = {}
        self.is_showing_sequence = False
        self.status = tk.Label(root, text="Welcome to Simon Says!", font=("Arial", 16), 
                              bg='#2b2b2b', fg='white')  # Dark bg, white text
        self.status.pack(pady=10)
        self.create_buttons()
        self.start_button = tk.Button(root, text="Start Game", font=("Arial", 14), 
                                     command=self.start_game, bg='#4a4a4a', fg='white',
                                     relief='raised', borderwidth=2)
        self.start_button.pack(pady=10)
        self.score_label = tk.Label(root, text="Score: 0", font=("Arial", 12),
                                   bg='#2b2b2b', fg='white')  # Dark bg, white text
        self.score_label.pack(pady=5)
        self.score = 0

    def create_buttons(self):
        frame = tk.Frame(self.root, bg='#2b2b2b')  # Dark background for frame
        frame.pack(pady=10)
        # Create 2x2 grid layout
        positions = [(0, 0), (0, 1), (1, 0), (1, 1)]  # 2x2 grid positions
        color_names = {1: "RED", 2: "GREEN", 3: "BLUE", 4: "YELLOW"}
        for i, (num, color) in enumerate(COLORS.items()):
            row, col = positions[i]
            # Set text color for contrast
            fg = 'black' if color == 'yellow' else 'white'
            btn = tk.Button(frame, bg=color, width=12, height=6,
                            text=color_names[num], fg=fg, font=("Arial", 14, "bold"),
                            command=lambda n=num: self.user_click(n),
                            state="disabled", relief="raised", borderwidth=4)
            btn.grid(row=row, column=col, padx=10, pady=10)
            self.buttons[num] = btn

    def start_game(self):
        self.sequence = []
        self.user_sequence = []
        self.round = 1
        self.score = 0
        self.score_label.config(text=f"Score: {self.score}")
        self.status.config(text="Game started! Watch the sequence.")
        self.start_button.config(state="disabled")
        for btn in self.buttons.values():
            btn.config(state="disabled")
        self.root.after(1000, self.next_round)

    def next_round(self):
        self.user_sequence = []
        self.sequence.append(random.randint(1, 4))
        self.status.config(text=f"Round {self.round}: Watch the sequence!")
        for btn in self.buttons.values():
            btn.config(state="disabled")
        self.is_showing_sequence = True
        self.root.after(1000, self.show_sequence, 0)

    def show_sequence(self, idx):
        if idx < len(self.sequence):
            num = self.sequence[idx]
            self.buttons[num].config(relief="sunken")
            self.root.after(500, lambda: self.hide_button(num, idx))
        else:
            self.status.config(text="Now repeat the sequence by clicking!")
            for btn in self.buttons.values():
                btn.config(state="normal")
            self.is_showing_sequence = False

    def hide_button(self, num, idx):
        self.buttons[num].config(relief="raised")
        self.root.after(250, lambda: self.show_sequence(idx+1))

    def user_click(self, num):
        if self.is_showing_sequence:
            return  # Ignore clicks during sequence display
        self.user_sequence.append(num)
        # Flash the button for feedback
        self.buttons[num].config(relief="sunken")
        self.root.after(150, lambda: self.buttons[num].config(relief="raised"))
        if self.user_sequence == self.sequence[:len(self.user_sequence)]:
            if len(self.user_sequence) == len(self.sequence):
                self.score += self.round
                self.score_label.config(text=f"Score: {self.score}")
                self.round += 1
                self.status.config(text="Correct! Next round...")
                for btn in self.buttons.values():
                    btn.config(state="disabled")
                self.root.after(1000, self.next_round)
        else:
            self.status.config(text="Wrong! Game Over. Press Start Game to play again.")
            for btn in self.buttons.values():
                btn.config(state="disabled")
            self.start_button.config(state="normal")

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Simon Says - Clickable GUI")
    game = SimonSaysGUI(root)
    root.mainloop() 