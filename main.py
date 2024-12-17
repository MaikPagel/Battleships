import tkinter as tk
import random

BOARD_SIZE = 10  # Board size
SHIPS = [
    ("Carrier", 5),
    ("Battleship", 4),
    ("Destroyer", 3),
    ("Submarine", 3),
    ("Patrol Boat", 2)
]

class BattleshipsGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Battleships")
        self.root.resizable(False, False)  # Fix window size

        # Player and computer boards
        self.player_board = [['~' for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        self.computer_board = [['~' for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]

        # Track guessed positions
        self.player_guesses = [['' for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        self.computer_guesses = [['' for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]

        # UI Frames
        self.frame_player = tk.Frame(root)
        self.frame_player.grid(row=0, column=0, padx=10)
        self.frame_computer = tk.Frame(root)
        self.frame_computer.grid(row=0, column=1, padx=10)

        # Ship placement
        self.ship_positions = []
        self.current_ship_index = 0  # Track current ship placement
        self.is_horizontal = True  # Default ship orientation

        # Setup boards
        self.setup_player_board()
        self.setup_computer_board()
        self.place_computer_ships()

        # Game variables
        self.current_turn = "Player"
        self.create_status_label()
        self.status_label.config(text=f"Place your {SHIPS[self.current_ship_index][0]} (Size: {SHIPS[self.current_ship_index][1]})")
        self.create_controls()

        # Key binding for rotating ships
        self.root.bind('r', lambda event: self.toggle_orientation())
                # Key binding for revealing computer ships
        self.root.bind('d', lambda event: self.reveal_computer_ships())
     
    def reveal_computer_ships(self):
        """Reveal the computer's ships for debugging purposes."""
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                if self.computer_board[row][col] == 'S':
                    self.computer_buttons[row][col].config(bg="green")  # Change color to green to show ships

    def setup_player_board(self):
        tk.Label(self.frame_player, text="Player's Board", font=("Arial", 10)).grid(row=0, column=0, columnspan=BOARD_SIZE)
        self.player_buttons = []
        for r in range(BOARD_SIZE):
            row = []
            for c in range(BOARD_SIZE):
                btn = tk.Button(self.frame_player, width=2, height=1, bg="lightblue",
                                command=lambda row=r, col=c: self.place_ship(row, col))
                btn.grid(row=r + 1, column=c)
                row.append(btn)
            self.player_buttons.append(row)

    def setup_computer_board(self):
        tk.Label(self.frame_computer, text="Computer's Board", font=("Arial", 10)).grid(row=0, column=0, columnspan=BOARD_SIZE)
        self.computer_buttons = []
        for r in range(BOARD_SIZE):
            row = []
            for c in range(BOARD_SIZE):
                btn = tk.Button(self.frame_computer, width=2, height=1, bg="lightgrey",
                                command=lambda row=r, col=c: self.player_guess(row, col))
                btn.grid(row=r + 1, column=c)
                row.append(btn)
            self.computer_buttons.append(row)

    def create_status_label(self):
        self.status_label = tk.Label(self.root, text="", font=("Arial", 12))
        self.status_label.grid(row=1, column=0, columnspan=2, pady=10)

    def create_controls(self):
        # Add a button to toggle ship orientation
        self.rotate_button = tk.Button(self.root, text="Rotate Ship (R)", command=self.toggle_orientation)
        self.rotate_button.grid(row=2, column=0, columnspan=2, pady=5)

    def toggle_orientation(self):
        self.is_horizontal = not self.is_horizontal
        orientation = "Horizontal" if self.is_horizontal else "Vertical"
        self.status_label.config(text=f"Ship orientation: {orientation}")

    def place_ship(self, row, col):
        ship_name, ship_size = SHIPS[self.current_ship_index]

        # Check if the ship can be placed without overlap and maintain the 1-grid rule
        if self.is_horizontal:
            if col + ship_size > BOARD_SIZE or not self.check_adjacent_spaces(row, col, ship_size, horizontal=True, is_player=True):
                self.status_label.config(text="Invalid position. Try again!")
                return
            for i in range(ship_size):
                self.player_board[row][col + i] = 'S'
                self.player_buttons[row][col + i].config(bg="blue")
        else:
            if row + ship_size > BOARD_SIZE or not self.check_adjacent_spaces(row, col, ship_size, horizontal=False, is_player=True):
                self.status_label.config(text="Invalid position. Try again!")
                return
            for i in range(ship_size):
                self.player_board[row + i][col] = 'S'
                self.player_buttons[row + i][col].config(bg="blue")

        # Move to the next ship
        self.current_ship_index += 1
        if self.current_ship_index < len(SHIPS):
            next_ship_name, next_ship_size = SHIPS[self.current_ship_index]
            self.status_label.config(text=f"Place your {next_ship_name} (Size: {next_ship_size})")
        else:
            self.status_label.config(text="All ships placed! Start guessing!")

    def check_adjacent_spaces(self, row, col, ship_size, horizontal=True, is_player=True):
        # Determine which board to check based on whether it's the player's or computer's turn
        board = self.player_board if is_player else self.computer_board
        
        # Check surrounding cells for overlap (including diagonals) to maintain the 1-grid rule
        for i in range(-1, ship_size + 1):  # Go one space before and after the ship's length
            for j in range(-1, 2):  # Check the 3 columns around each segment
                if horizontal:
                    check_row = row + j
                    check_col = col + i
                else:
                    check_row = row + i
                    check_col = col + j

                if 0 <= check_row < BOARD_SIZE and 0 <= check_col < BOARD_SIZE:
                    if board[check_row][check_col] == 'S':  # Adjacent to ship or ship segment
                        return False
        return True

    def place_computer_ships(self):
        for ship_name, ship_size in SHIPS:
            placed = False
            while not placed:
                is_horizontal = random.choice([True, False])
                row = random.randint(0, BOARD_SIZE - 1)
                col = random.randint(0, BOARD_SIZE - 1)

                if is_horizontal:
                    if col + ship_size <= BOARD_SIZE and self.check_adjacent_spaces(row, col, ship_size, horizontal=True, is_player=False):
                        for i in range(ship_size):
                            self.computer_board[row][col + i] = 'S'
                        placed = True
                else:
                    if row + ship_size <= BOARD_SIZE and self.check_adjacent_spaces(row, col, ship_size, horizontal=False, is_player=False):
                        for i in range(ship_size):
                            self.computer_board[row + i][col] = 'S'
                        placed = True

    def player_guess(self, row, col):
        if self.current_turn != "Player":
            return

        if self.computer_board[row][col] == 'S':
            self.computer_buttons[row][col].config(bg="red")
            self.status_label.config(text="Hit!")
            self.computer_board[row][col] = 'X'
        elif self.computer_board[row][col] == '~':
            self.computer_buttons[row][col].config(bg="white")
            self.status_label.config(text="Miss!")
            self.computer_board[row][col] = 'O'
        else:
            self.status_label.config(text="You already guessed that spot!")
            return

        if self.check_win(self.computer_board):
            self.status_label.config(text="You Win! All computer ships sunk.")
            self.create_restart_button()
            return

        self.current_turn = "Computer"
        self.root.after(1000, self.computer_turn)

    def computer_turn(self):
        while True:
            row = random.randint(0, BOARD_SIZE - 1)
            col = random.randint(0, BOARD_SIZE - 1)
            if self.player_board[row][col] == 'S':
                self.player_buttons[row][col].config(bg="red")
                self.status_label.config(text="Computer hit your ship!")
                self.player_board[row][col] = 'X'
                break
            elif self.player_board[row][col] == '~':
                self.player_buttons[row][col].config(bg="white")
                self.status_label.config(text="Computer missed!")
                self.player_board[row][col] = 'O'
                break

        if self.check_win(self.player_board):
            self.status_label.config(text="Game Over! Computer Wins!")
            self.create_restart_button()
            return

        self.current_turn = "Player"

    def check_win(self, board):
        for row in board:
            if 'S' in row:
                return False
        return True

    def create_restart_button(self):
        self.restart_button = tk.Button(self.root, text="Restart Game", command=self.restart_game)
        self.restart_button.grid(row=3, column=0, columnspan=2, pady=10)

    def restart_game(self):
        # Reset game variables
        self.current_turn = "Player"
        self.current_ship_index = 0
        self.is_horizontal = True

        # Reset boards
        self.player_board = [['~' for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        self.computer_board = [['~' for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]

        # Clear all buttons
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                self.player_buttons[r][c].config(bg="lightblue")
                self.computer_buttons[r][c].config(bg="lightgrey", state="normal")

        # Remove restart button
        self.restart_button.destroy()

        # Reset game state
        self.place_computer_ships()
        self.status_label.config(text=f"Place your {SHIPS[self.current_ship_index][0]} (Size: {SHIPS[self.current_ship_index][1]})")

if __name__ == "__main__":
    root = tk.Tk()
    game = BattleshipsGame(root)
    root.mainloop()
