import tkinter as tk
from tkinter import messagebox
import random

class SnakeLadderGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Snake & Ladders Game 🎲")
        self.max_players = 4
        self.token_colors = ["red", "blue", "green", "orange"]
        self.create_welcome_screen()

    def create_welcome_screen(self):
        self.welcome_frame = tk.Frame(self.root)
        self.welcome_frame.pack(pady=20)

        tk.Label(self.welcome_frame, text="🎉 Welcome to Snake & Ladders 🎉", font=("Arial", 20, "bold")).pack(pady=10)

        tk.Label(self.welcome_frame, text="Select Number of Players (2 to 4):", font=("Arial", 12)).pack()
        self.player_count_var = tk.IntVar(value=2)
        player_count_menu = tk.OptionMenu(self.welcome_frame, self.player_count_var, 2, 3, 4, command=self.update_player_inputs)
        player_count_menu.pack(pady=5)

        self.player_input_frame = tk.Frame(self.welcome_frame)
        self.player_input_frame.pack(pady=10)
        self.player_entries = []
        self.update_player_inputs(2)

        tk.Label(self.welcome_frame, text="Select Game Mode:", font=("Arial", 12)).pack(pady=(10, 0))
        self.game_mode = tk.StringVar(value="normal")
        tk.Radiobutton(self.welcome_frame, text="Normal", variable=self.game_mode, value="normal").pack()
        tk.Radiobutton(self.welcome_frame, text="Magic Key", variable=self.game_mode, value="magic", command=self.toggle_magic_key).pack()

        self.magic_key_label = tk.Label(self.welcome_frame, text="Enter Magic Key (1-6):", font=("Arial", 10))
        self.magic_key_entry = tk.Entry(self.welcome_frame, font=("Arial", 10))

        tk.Button(self.welcome_frame, text="Start Game ▶️", font=("Arial", 12, "bold"), command=self.start_game).pack(pady=20)

    def update_player_inputs(self, count):
        for widget in self.player_input_frame.winfo_children():
            widget.destroy()
        self.player_entries.clear()
        for i in range(int(count)):
            entry = tk.Entry(self.player_input_frame, font=("Arial", 12))
            entry.insert(0, f"Player {i + 1}")
            entry.pack(pady=2)
            self.player_entries.append(entry)

    def toggle_magic_key(self):
        if self.game_mode.get() == "magic":
            self.magic_key_label.pack()
            self.magic_key_entry.pack()
        else:
            self.magic_key_label.pack_forget()
            self.magic_key_entry.pack_forget()

    def start_game(self):
        self.num_players = self.player_count_var.get()
        self.player_names = [entry.get() for entry in self.player_entries]

        if self.game_mode.get() == "magic":
            try:
                self.magic_key = int(self.magic_key_entry.get())
                if not 1 <= self.magic_key <= 6:
                    raise ValueError
            except ValueError:
                messagebox.showerror("Invalid Input", "Magic key must be an integer between 1 and 6.")
                return
        else:
            self.magic_key = None

        self.positions = [1] * self.num_players
        self.tokens = []
        self.has_magic_key = [False] * self.num_players
        self.turn = 0
        self.snakes, self.ladders = self.generate_snakes_and_ladders()

        self.welcome_frame.destroy()
        self.create_game_ui()

    def create_game_ui(self):
        main_frame = tk.Frame(self.root)
        main_frame.pack()

        self.canvas = tk.Canvas(main_frame, width=600, height=600, bg="white")
        self.canvas.grid(row=0, column=0, padx=10, pady=10)
        self.draw_board()
        self.draw_ladders()
        self.draw_snakes()

        for i in range(self.num_players):
            x1, y1, x2, y2 = self.get_coords(1, offset=i * 10)
            token = self.canvas.create_oval(x1, y1, x2, y2, fill=self.token_colors[i])
            self.tokens.append(token)

        self.sidebar = tk.Frame(main_frame)
        self.sidebar.grid(row=0, column=1, sticky="n", padx=20)

        tk.Label(self.sidebar, text="🎮 Player Info", font=("Arial", 14, "bold")).pack(pady=5)

        self.player_labels = []
        self.player_position_labels = []
        for i, name in enumerate(self.player_names):
            frame = tk.Frame(self.sidebar)
            frame.pack(pady=3)
            name_label = tk.Label(frame, text=name, bg=self.token_colors[i], fg="white", width=15, font=("Arial", 10))
            name_label.pack(side="left", padx=2)
            pos_label = tk.Label(frame, text="Pos: 1", width=7)
            pos_label.pack(side="left")
            self.player_labels.append(name_label)
            self.player_position_labels.append(pos_label)

        self.dice_face_label = tk.Label(self.sidebar, text="🎲 Dice: -", font=("Arial", 14))
        self.dice_face_label.pack(pady=10)

        self.turn_label = tk.Label(self.sidebar, text="Turn: --", font=("Arial", 12, "bold"), fg="green")
        self.turn_label.pack(pady=5)

        self.roll_button = tk.Button(self.sidebar, text="Roll Dice 🎲", font=("Arial", 12), command=self.play_turn)
        self.roll_button.pack(pady=10)

        self.update_turn_display()

    def draw_board(self):
        size = 60
        for row in range(10):
            for col in range(10):
                x1 = col * size
                y1 = row * size
                x2 = x1 + size
                y2 = y1 + size
                color = "#f9f9f9" if (row + col) % 2 == 0 else "#d9d9d9"
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="black")
                number = 100 - (row * 10 + (col if row % 2 == 0 else 9 - col))
                self.canvas.create_text(x1 + 30, y1 + 30, text=str(number), font=("Arial", 9))

    def get_coords(self, pos, offset=0):
        row = (pos - 1) // 10
        col = (pos - 1) % 10
        if row % 2 == 1:
            col = 9 - col
        x1 = col * 60 + 10 + offset
        y1 = (9 - row) * 60 + 10
        return x1, y1, x1 + 30, y1 + 30

    def get_center(self, pos):
        x1, y1, x2, y2 = self.get_coords(pos)
        return (x1 + x2) // 2, (y1 + y2) // 2

    def generate_snakes_and_ladders(self, num_snakes=8, num_ladders=8):
        all_positions = list(range(2, 100))
        random.shuffle(all_positions)
        snakes = {}
        ladders = {}
        used = set()

        while len(ladders) < num_ladders:
            start, end = random.sample(all_positions, 2)
            if start < end and start not in used and end not in used:
                ladders[start] = end
                used.update([start, end])

        while len(snakes) < num_snakes:
            start, end = random.sample(all_positions, 2)
            if start > end and start not in used and end not in used:
                snakes[start] = end
                used.update([start, end])

        return snakes, ladders

    def draw_ladders(self):
        for start, end in self.ladders.items():
            x1, y1 = self.get_center(start)
            x2, y2 = self.get_center(end)

            offset = 10
            self.canvas.create_line(x1 - offset, y1, x2 - offset, y2, fill="brown", width=3)
            self.canvas.create_line(x1 + offset, y1, x2 + offset, y2, fill="brown", width=3)

            steps = 5
            for i in range(steps + 1):
                sx1 = x1 - offset + (i * (x2 - x1) / steps)
                sy1 = y1 + (i * (y2 - y1) / steps)
                sx2 = x1 + offset + (i * (x2 - x1) / steps)
                sy2 = y1 + (i * (y2 - y1) / steps)
                self.canvas.create_line(sx1, sy1, sx2, sy2, fill="brown", width=2)

    def draw_snakes(self):
        for start, end in self.snakes.items():
            x1, y1 = self.get_center(start)
            x2, y2 = self.get_center(end)

            mid_x = (x1 + x2) / 2
            mid_y = (y1 + y2) / 2
            ctrl1_x = (x1 + mid_x) / 2 + 30
            ctrl1_y = (y1 + mid_y) / 2 - 30
            ctrl2_x = (x2 + mid_x) / 2 - 30
            ctrl2_y = (y2 + mid_y) / 2 + 30

            points = [
                x1, y1,
                ctrl1_x, ctrl1_y,
                mid_x, mid_y,
                ctrl2_x, ctrl2_y,
                x2, y2
            ]
            self.canvas.create_line(points, fill="purple", width=4, smooth=True)
            self.canvas.create_text(mid_x, mid_y, text="🐍", font=("Arial", 16))

    def update_turn_display(self):
        for i, label in enumerate(self.player_position_labels):
            label.config(text=f"Pos: {self.positions[i]}")
        self.turn_label.config(text=f"🎯 {self.player_names[self.turn]}'s Turn")

    def play_turn(self):
        dice = random.randint(1, 6)
        self.dice_face_label.config(text=f"🎲 Dice: {dice}")
        player = self.turn

        if self.magic_key and not self.has_magic_key[player]:
            if dice == self.magic_key:
                self.has_magic_key[player] = True
            else:
                self.next_turn()
                return

        pos = self.positions[player] + dice
        if pos > 100:
            self.next_turn()
            return

        if pos in self.snakes:
            pos = self.snakes[pos]
        elif pos in self.ladders:
            pos = self.ladders[pos]

        self.positions[player] = pos
        x1, y1, x2, y2 = self.get_coords(pos, offset=player * 10)
        self.canvas.coords(self.tokens[player], x1, y1, x2, y2)
        self.update_turn_display()

        if pos == 100:
            self.game_won(player)
        else:
            self.next_turn()

    def next_turn(self):
        self.turn = (self.turn + 1) % self.num_players
        self.update_turn_display()

    def game_won(self, player_index):
        winner = self.player_names[player_index]
        result = messagebox.showinfo("🎉 Game Over", f"🏆 Congratulations {winner}!\nYou conquered the board! 🎉")
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    game = SnakeLadderGame(root)
    root.mainloop()
