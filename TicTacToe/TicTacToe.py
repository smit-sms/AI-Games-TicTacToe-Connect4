from tqdm import tqdm
import csv
import tkinter as tk
from tkinter import messagebox, ttk
from TicTacToeOpponents import *


class TicTacToe:
    def __init__(self, player_x_strategy, player_o_strategy):
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        self.current_player = 'X'
        self.strategies = {'X': player_x_strategy, 'O': player_o_strategy}

    def make_move(self, row, col, player):
        if self.is_move_valid(row, col):
            self.board[row][col] = player
            return True
        return False

    def is_move_valid(self, row, col):
        return self.board[row][col] == ' '

    def switch_player(self):
        self.current_player = 'O' if self.current_player == 'X' else 'X'

    def check_win(self, player):
        # Check rows, columns, and diagonals for a win
        win_conditions = [
            [self.board[i][0] == self.board[i][1] == self.board[i][2] == player for i in range(3)],
            [self.board[0][i] == self.board[1][i] == self.board[2][i] == player for i in range(3)],
            [self.board[0][0] == self.board[1][1] == self.board[2][2] == player],
            [self.board[0][2] == self.board[1][1] == self.board[2][0] == player]
        ]
        return any(any(row) for row in win_conditions)

    def check_draw(self):
        return all(self.board[row][col] != ' ' for row in range(3) for col in range(3))

    def get_empty_cells(self):
        return [(row, col) for row in range(3) for col in range(3) if self.board[row][col] == ' ']

    def reset(self):
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        self.current_player = 'X'

class GUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.geometry("500x500")
        self.window.title("Tic Tac Toe")
        # Initialize player options and game settings
        self.player_x_option = tk.StringVar()
        self.player_o_option = tk.StringVar()
        self.player_options = ('Human', 'Computer')
        self.algorithm_options = ('Minimax', 'Alpha-Beta Pruning', 'Default Opponent', 'Q-Learning Agent')
        self.buttons = [[None for _ in range(3)] for _ in range(3)]  # Will be initialized after starting the game
        self.initialize_options()

    def initialize_options(self):
        # Player X selection
        ttk.Label(self.window, text="Player X:").grid(column=0, row=0, padx=10, pady=10)
        player_x_dropdown = ttk.Combobox(self.window, width=10, textvariable=self.player_x_option, state="readonly")
        player_x_dropdown['values'] = self.player_options
        player_x_dropdown.grid(column=1, row=0)
        player_x_dropdown.current(0)  # set default value

        # Algorithm selection for Player X
        ttk.Label(self.window, text="Algorithm:").grid(column=2, row=0, padx=10, pady=10)
        self.player_x_algorithm_option = tk.StringVar()
        player_x_algorithm_dropdown = ttk.Combobox(self.window, width=16, textvariable=self.player_x_algorithm_option, state="readonly")
        player_x_algorithm_dropdown['values'] = self.algorithm_options
        player_x_algorithm_dropdown.grid(column=3, row=0)
        player_x_algorithm_dropdown.current(0)  # set default value

        # Player O selection
        ttk.Label(self.window, text="Player O:").grid(column=0, row=1, padx=10, pady=10)
        player_o_dropdown = ttk.Combobox(self.window, width=10, textvariable=self.player_o_option, state="readonly")
        player_o_dropdown['values'] = self.player_options
        player_o_dropdown.grid(column=1, row=1)
        player_o_dropdown.current(0)  # set default value

        # Algorithm selection for Player O
        ttk.Label(self.window, text="Algorithm:").grid(column=2, row=1, padx=10, pady=10)
        self.player_o_algorithm_option = tk.StringVar()
        player_o_algorithm_dropdown = ttk.Combobox(self.window, width=16, textvariable=self.player_o_algorithm_option, state="readonly")
        player_o_algorithm_dropdown['values'] = self.algorithm_options
        player_o_algorithm_dropdown.grid(column=3, row=1)
        player_o_algorithm_dropdown.current(0)  # set default value
        
        self.train_button = ttk.Button(self.window, text="Train AI", command=self.train_ai)
        self.train_button.grid(column=1, row=2, columnspan=2, pady=10)
        
        analysis_button = ttk.Button(self.window, text="Analyze Performance", command=self.start_performance_analysis)
        analysis_button.grid(column=2, row=2, columnspan=4, pady=10)

        play_button = ttk.Button(self.window, text="Play Game", command=self.start_game)
        play_button.grid(column=0, row=2, columnspan=2, pady=10)

    def initialize_board(self):
        button_style = {'font': ('Helvetica', 15), 'bg': '#F0F0F0', 'activebackground': '#D0D0D0'}
        # Destroy previous board if exists
        for row in self.buttons:
            for button in row:
                if button is not None:
                    button.destroy()

        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        for i in range(3):
            for j in range(3):
                button = tk.Button(self.window, height=3, width=6,
                                   command=lambda row=i, col=j: self.make_move(row, col, True), **button_style)
                button.grid(row=i+5, column=j+1, padx=4, pady=4, sticky='nsw')  # Adjust grid placement
                self.buttons[i][j] = button

    def update_button(self, row, col, player):
        colors = {'X': 'pink', 'O': 'light green'}
        button = self.buttons[row][col]
        button.config(text=player, state='disabled', disabledforeground='black', bg=colors[player])

    def check_game_over(self):
        if self.game.check_win(self.game.current_player):
            messagebox.showinfo("Game Over", f"Player {self.game.current_player} wins!")
            self.reset_game()
            return True
        elif self.game.check_draw():
            messagebox.showinfo("Game Over", "It's a draw!")
            self.reset_game()
            return True
        return False

    def make_move(self, row, col, is_human):
        if self.game.is_move_valid(row, col):
            self.game.make_move(row, col, self.game.current_player)
            self.update_button(row, col, self.game.current_player)
            if not self.check_game_over():
                self.game.switch_player()
                self.trigger_computer_move()

    def start_game(self):
        player_x_strategy = self.get_strategy(self.player_x_algorithm_option.get())
        player_o_strategy = self.get_strategy(self.player_o_algorithm_option.get())
        self.game = TicTacToe(player_x_strategy, player_o_strategy)
        self.initialize_board()
        if self.player_x_option.get() == 'Computer':
            self.trigger_computer_move()

    def reset_game(self):
        # Resets the game to its initial state
        for row in self.buttons:
            for button in row:
                button.config(text='', state='normal', bg='SystemButtonFace')
        self.game.reset()

    def trigger_computer_move(self):
        # Trigger a computer move if the current player is a computer.
        if ((self.game.current_player == 'X' and self.player_x_option.get() == 'Computer') or 
        (self.game.current_player == 'O' and self.player_o_option.get() == 'Computer')) \
        and not self.check_game_over():
            self.window.after(400, self.perform_computer_move)

    def get_strategy(self, algorithm_name):
        if algorithm_name == "Minimax":
            return MinimaxOpponent()
        elif algorithm_name == "Alpha-Beta Pruning":
            return MinimaxWithAlphaBetaOpponent()
        elif algorithm_name == "Q-Learning Agent":
            return QLearningOpponent()
        elif algorithm_name == "Default Opponent":
            return DefaultOpponent()

    def perform_computer_move(self):
        row, col = self.game.strategies[self.game.current_player].choose_move(self.game)
        if self.game.make_move(row, col, self.game.current_player):
            self.update_button(row, col, self.game.current_player)
            if not self.check_game_over():
                self.game.switch_player()
                # Check if the next move is also a computer move
                self.trigger_computer_move()
            
    def train_ai(self):
        q_learning_agent = QLearningOpponent()
        
        # Define opponents for training
        opponents = [
            MinimaxOpponent(),
            MinimaxWithAlphaBetaOpponent(),
            DefaultOpponent(),
            QLearningOpponent()
        ]

        for opponent in opponents:
            # Dynamically adjust the game setup based on the opponent
            # Example: Q-learning agent as 'X' and opponent as 'O'
            if isinstance(opponent, QLearningOpponent):
                # For Q-learning vs Q-learning, might want to adjust parameters or handle differently
                self.game = TicTacToe(opponent, q_learning_agent)
            else:
                self.game = TicTacToe(q_learning_agent, opponent)

            # Perform training
            print(f"Training against {type(opponent).__name__}...")
            q_learning_agent.train(self.game, iterations=10000000)

        # After training against all opponents
        q_learning_agent.save_q_table()
        print("Training complete.")

    def start_performance_analysis(self):
        self.is_ai_playing = True  # Add this attribute to your __init__ method if it doesn't exist
        games = 500  # Number of games for analysis
        matchups = [
            (MinimaxOpponent(), DefaultOpponent(), "Minimax vs Default"),
            (MinimaxWithAlphaBetaOpponent(), DefaultOpponent(), "Alpha Beta vs Default"),
            (DefaultOpponent(), QLearningOpponent(), "Default vs Q-Learning"),
            (QLearningOpponent(), MinimaxOpponent(), "Q-Learning vs Minimax"),
            (QLearningOpponent(), MinimaxWithAlphaBetaOpponent(), "Q-Learning vs Alpha Beta"),
            (MinimaxOpponent(), MinimaxWithAlphaBetaOpponent(), "Minimax vs Alpha Beta")
        ]

        results = []

        for player_x_strategy, player_o_strategy, description in matchups:
            print(f"Starting {description}...")
            x_wins, o_wins, draws = 0, 0, 0
            for _ in tqdm(range(games)):
                winner = self.play_ai_vs_ai_game(player_x_strategy, player_o_strategy)
                if winner == 'X':
                    x_wins += 1
                elif winner == 'O':
                    o_wins += 1
                else:  # Assume draws for any other result
                    draws += 1
            result = {
                "Matchup": description,
                "AI 1": player_x_strategy.__class__.__name__,
                "AI 1 Wins": x_wins,
                "AI 2": player_o_strategy.__class__.__name__,
                "AI 2 Wins": o_wins,
                "Draws": draws
            }
            results.append(result)

        self.log_matchup_results_to_csv(results, games)
        self.is_ai_playing = False
    
    def log_matchup_results_to_csv(self, results, games):
        filename = f'tictactoe_performance_analysis_{games}.csv' 
        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Matchup", "AI 1", "AI 1 Wins", "AI 2", "AI 2 Wins", "Draws"])
            # Write the data
            for result in results:
                writer.writerow([
                    result["Matchup"],
                    result["AI 1"],
                    result["AI 1 Wins"],
                    result["AI 2"],
                    result["AI 2 Wins"],
                    result["Draws"]
                ])
        print(f"Results saved to {filename}")

    def play_ai_vs_ai_game(self, player_x_strategy, player_o_strategy):
        game = TicTacToe(player_x_strategy, player_o_strategy)
        while True:
            row, col = game.strategies[game.current_player].choose_move(game)
            game.make_move(row, col, game.current_player)
            if game.check_win(game.current_player):
                return game.current_player
            elif game.check_draw():
                return "Draw"
            game.switch_player()

    def run(self):
        self.window.mainloop()


if __name__ == "__main__":
    gui = GUI()
    gui.run()
