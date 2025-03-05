import tkinter as tk
import random

class OddEvenCricket:
    def __init__(self, root):
        self.root = root
        self.root.title("Odd Even Cricket")
        self.root.geometry("800x600")  # 200% larger UI

        # Status Label
        self.status_label = tk.Label(root, text="Press 1 for Even or 2 for Odd:", font=("Arial", 24))
        self.status_label.pack(pady=20)

        # Toss Buttons (Even/Odd)
        self.choice_frame = tk.Frame(root)
        self.even_button = tk.Button(self.choice_frame, text="Even", font=("Arial", 20), width=10, height=2, command=lambda: self.choose_odd_even(1))
        self.odd_button = tk.Button(self.choice_frame, text="Odd", font=("Arial", 20), width=10, height=2, command=lambda: self.choose_odd_even(2))
        self.even_button.pack(side=tk.LEFT, padx=20)
        self.odd_button.pack(side=tk.LEFT, padx=20)
        self.choice_frame.pack()

        # Number Selection Buttons (1-10)
        self.number_frame = tk.Frame(root)
        self.number_buttons = []
        for i in range(1, 11):
            btn = tk.Button(self.number_frame, text=str(i), font=("Arial", 18), width=5, height=2, command=lambda num=i: self.select_number(num))
            btn.pack(side=tk.LEFT, padx=5, pady=5)
            self.number_buttons.append(btn)
        self.number_frame.pack()
        
        # Info Label
        self.info_label = tk.Label(root, text="", font=("Arial", 20))
        self.info_label.pack(pady=20)

        # Play Again Button (Initially Hidden)
        self.play_again_button = tk.Button(root, text="Play Again", font=("Arial", 20), width=15, height=2, command=self.reset_game)
        self.play_again_button.pack(pady=20)
        self.play_again_button.pack_forget()

        self.reset_game()

    def reset_game(self):
        """Resets the game for a new match."""
        self.player_score = 0
        self.computer_score = 0
        self.target = None
        self.is_first_innings = True
        self.is_player_batting = None
        self.toss_won = False
        self.toss_choice = None

        self.status_label.config(text="Press 1 for Even or 2 for Odd:")
        self.info_label.config(text="")
        self.enable_choice_buttons(True)
        self.enable_number_buttons(False)
        self.play_again_button.pack_forget()

    def enable_choice_buttons(self, enable):
        """Enable/disable Even/Odd buttons."""
        state = tk.NORMAL if enable else tk.DISABLED
        self.even_button.config(state=state)
        self.odd_button.config(state=state)

    def enable_number_buttons(self, enable):
        """Enable/disable number buttons (1-10)."""
        state = tk.NORMAL if enable else tk.DISABLED
        for btn in self.number_buttons:
            btn.config(state=state)

    def choose_odd_even(self, choice):
        """Handles the toss selection."""
        self.toss_choice = choice
        self.status_label.config(text="Enter your number (1-10):")
        self.enable_choice_buttons(False)
        self.enable_number_buttons(True)

    def select_number(self, player_num):
        """Handles the toss number selection."""
        if not self.toss_won:
            comp_num = random.randint(1, 10)
            total = player_num + comp_num
            player_wins = (total % 2 == 0 and self.toss_choice == 1) or (total % 2 == 1 and self.toss_choice == 2)

            toss_result = f"You chose {player_num}, Computer chose {comp_num}.\n"
            if player_wins:
                self.status_label.config(text="You won the toss! Choose to Bat or Bowl:")
                self.show_bat_bowl_choice()
            else:
                self.is_player_batting = random.choice([True, False])  # Computer decides
                self.status_label.config(text=f"Computer won the toss and chose to {'Bat' if self.is_player_batting else 'Bowl'}.")
                self.enable_number_buttons(True)
                self.toss_won = True
            return

        # If toss was already done, handle the game play
        comp_num = random.randint(1, 10)
        turn_info = f"You chose: {player_num}, Computer chose: {comp_num}\n"

        if player_num == comp_num:  # OUT condition
            turn_info += "OUT!\n"
            if self.is_first_innings:
                self.target = (self.player_score if self.is_player_batting else self.computer_score) + 1
                turn_info += f"Target to chase: {self.target}\n"
                self.is_first_innings = False
                self.is_player_batting = not self.is_player_batting
                self.status_label.config(text=f"{'You' if self.is_player_batting else 'Computer'} now batting!")
                self.info_label.config(text=turn_info)
                return
            self.end_game()
            return

        if self.is_player_batting:
            self.player_score += player_num
            turn_info += f"Your Score: {self.player_score}\n"
            if not self.is_first_innings and self.player_score >= self.target:
                turn_info += f"You win by {self.player_score - self.computer_score} runs!\n"
                self.end_game()
                return
        else:
            self.computer_score += comp_num
            turn_info += f"Computer's Score: {self.computer_score}\n"
            if not self.is_first_innings and self.computer_score >= self.target:
                turn_info += f"Computer wins by {self.computer_score - self.player_score} runs!\n"
                self.end_game()
                return

        self.info_label.config(text=turn_info)

    def show_bat_bowl_choice(self):
        """Displays Bat/Bowl choice buttons for the player."""
        self.choice_frame.pack_forget()
        self.choice_frame = tk.Frame(self.root)
        self.choice_frame.pack()

        bat_button = tk.Button(self.choice_frame, text="Bat", font=("Arial", 20), width=10, height=2, command=lambda: self.start_game(True))
        bat_button.pack(side=tk.LEFT, padx=20)

        bowl_button = tk.Button(self.choice_frame, text="Bowl", font=("Arial", 20), width=10, height=2, command=lambda: self.start_game(False))
        bowl_button.pack(side=tk.LEFT, padx=20)

    def start_game(self, is_player_batting):
        """Starts the game after toss."""
        self.is_player_batting = is_player_batting
        self.status_label.config(text=f"You chose to {'Bat' if is_player_batting else 'Bowl'}. Enter a number (1-10):")
        self.enable_number_buttons(True)

    def end_game(self):
        """Ends the game and shows results."""
        self.status_label.config(text="Game Over! Press Play Again to restart.")
        self.enable_number_buttons(False)
        self.play_again_button.pack()

if __name__ == "__main__":
    root = tk.Tk()
    game = OddEvenCricket(root)
    root.mainloop()
