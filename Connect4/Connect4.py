import tkinter as tk
from tkinter import messagebox, ttk
import random
from Connect4Opponents import *
import csv

class Connect4GUI:
    def __init__(self, master):
        self.master = master
        self.master.geometry("500x500")  # Adjusted for Connect 4 board size
        self.master.title("Connect 4")
        self.q_learning_opponent = QLearningOpponent()
        # Player and Algorithm Options
        self.player_options = ('Human', 'Computer')
        self.algorithm_options = ('Minimax', 'Alpha-Beta Pruning', 'Default Opponent', 'Q-Learning')  # Assuming these are the implemented algorithms
        self.is_ai_playing = False
        self.initialize_options()

        # Board Setup
        self.rows = 6
        self.cols = 7
        self.win_length = 4
        self.canvas_height = 360
        self.canvas_width = 420
        self.cell_width = self.canvas_width / self.cols
        self.cell_height = self.canvas_height / self.rows

        self.canvas = tk.Canvas(master, width=self.canvas_width, height=self.canvas_height, bg='grey')
        self.canvas.grid(row=3, column=0, columnspan=4, pady=0) 
        self.canvas.bind("<Button-1>", self.handle_click)

        # Game Initialization
        self.initialize_game()

    def initialize_options(self):
        # Player 1 Selection
        ttk.Label(self.master, text="Player 1:").grid(column=0, row=0, padx=10, pady=10)
        self.player1_type = ttk.Combobox(self.master, width=12, values=self.player_options, state="readonly")
        self.player1_type.grid(column=1, row=0)
        self.player1_type.set('Human')  # Default value

        # Algorithm Selection for Player 1
        ttk.Label(self.master, text="Player 1 Algorithm:").grid(column=2, row=0, padx=10, pady=10)
        self.player1_algorithm = ttk.Combobox(self.master, width=20, values=self.algorithm_options, state="readonly")
        self.player1_algorithm.grid(column=3, row=0)
        self.player1_algorithm.set('Minimax')  # Default value

        # Player 2 Selection
        ttk.Label(self.master, text="Player 2:").grid(column=0, row=1, padx=10, pady=10)
        self.player2_type = ttk.Combobox(self.master, width=12, values=self.player_options, state="readonly")
        self.player2_type.grid(column=1, row=1)
        self.player2_type.set('Human')  # Default value

        # Algorithm Selection for Player 2
        ttk.Label(self.master, text="Player 2 Algorithm:").grid(column=2, row=1, padx=10, pady=10)
        self.player2_algorithm = ttk.Combobox(self.master, width=20, values=self.algorithm_options, state="readonly")
        self.player2_algorithm.grid(column=3, row=1)
        self.player2_algorithm.set('Minimax')  # Default value

        # Inside initialize_options method of Connect4GUI class
        train_ai_button = ttk.Button(self.master, text="Train AI", command=self.train_ai)
        train_ai_button.grid(column=1, row=2, columnspan=2, pady=10)
        
        analysis_button = ttk.Button(self.master, text="Analyze Performance", command=self.start_performance_analysis)
        analysis_button.grid(column=2, row=2, columnspan=4, pady=10)

        # Start Game Button
        play_button = ttk.Button(self.master, text="Start Game", command=self.initialize_game)
        play_button.grid(column=0, row=2, columnspan=2, pady=10)

    def start_performance_analysis(self):
        self.is_ai_playing = True
        games = 500  # Number of games for the analysis
        matchups = [
            (MinimaxOpponent(), DefaultOpponent(), "Minimax vs Default"),
            (AlphaBetaOpponent(), DefaultOpponent(), "Alpha Beta vs Default"),
            (DefaultOpponent(), QLearningOpponent(), "Default vs Q-Learning"),
            (QLearningOpponent(), MinimaxOpponent(), "Q-Learning vs Minimax"),
            (QLearningOpponent(), AlphaBetaOpponent(), "Q-Learning vs Alpha Beta"),
            (MinimaxOpponent(), AlphaBetaOpponent(), "Minimax vs Alpha Beta")
        ]

        results = []

        for ai1, ai2, description in matchups:
            result = {"Matchup": description, "AI 1": ai1.__class__.__name__, "AI 2": ai2.__class__.__name__, "Details": []}
            print(f"Starting {description}...")
            ai1_wins = 0
            ai2_wins = 0
            draws = 0
            for _ in tqdm(range(games)):
                winner = self.play_ai_vs_ai_game(ai1, ai2)
                if winner == ai1.__class__.__name__:
                    ai1_wins += 1
                elif winner == ai2.__class__.__name__:
                    ai2_wins += 1
                else:  # Assume draws for any other result
                    draws += 1
            result["AI 1 Wins"] = ai1_wins
            result["AI 2 Wins"] = ai2_wins
            result["Draws"] = draws
            results.append(result)

        # Log results to CSV
        self.log_matchup_results_to_csv(results, games)
        self.is_ai_playing = False

    def log_matchup_results_to_csv(self, results, games):
        filename = f"performance_analysis_connect4_{games}.csv"
        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            header = ["Matchup", "AI 1", "AI 1 Wins", "AI 2", "AI 2 Wins", "Draws"]
            writer.writerow(header)
            for stats in results:
                row = [
                    stats["Matchup"],
                    stats["AI 1"],
                    stats["AI 1 Wins"],
                    stats["AI 2"],
                    stats["AI 2 Wins"],
                    stats["Draws"]
                ]
                writer.writerow(row)

        print(f"Results saved to {filename}")
    
    def play_ai_vs_ai_game(self, ai_player_1, ai_player_2):
        self.reset_game()  # Resets the game to start a new match
        self.turn = 'X'  # Assuming 'X' starts. Adjust if your game logic differs.

        # Determine which AI is playing as 'X' and which as 'O'
        if isinstance(ai_player_1, QLearningOpponent):
            ai_X, ai_O = ai_player_2, ai_player_1
        else:
            ai_X, ai_O = ai_player_1, ai_player_2
        
        while not self.game_over:
            # Determine current AI based on turn
            current_ai = ai_X if self.turn == 'X' else ai_O
            # Get the move from the current AI
            move = current_ai.choose_move(self, current_ai)

            player_moved = self.drop_piece(move)
            if player_moved:
                if self.check_win():
                    return current_ai.__class__.__name__
                elif self.is_full():
                    return "Draw"
                self.change_turn()
            else:
                # invalid move, return draw for the game
                return "Draw"

    def initialize_game(self):
        self.board = [['-' for _ in range(self.cols)] for _ in range(self.rows)]
        self.turn = 'X'  # Player 1 always starts
        self.game_over = False
        self.draw_board()
        if self.player1_type.get() == "Computer":
            self.ai_move()  # If Player 1 is a computer, make the first move

    def draw_board(self):
        self.canvas.delete('all')  # Clear canvas before redrawing
        for row in range(self.rows):
            for col in range(self.cols):
                x1 = col * self.cell_width
                y1 = row * self.cell_height
                x2 = x1 + self.cell_width
                y2 = y1 + self.cell_height
                self.canvas.create_rectangle(x1, y1, x2, y2, fill='grey', outline='white')
                if self.board[row][col] != '-':
                    self.draw_piece(row, col, self.board[row][col])

    def draw_piece(self, row, col, player):
        x1 = col * self.cell_width + self.cell_width / 4
        y1 = row * self.cell_height + self.cell_height / 4
        x2 = x1 + self.cell_width / 2
        y2 = y1 + self.cell_height / 2
        color = 'red' if player == 'X' else 'yellow'
        self.canvas.create_oval(x1, y1, x2, y2, fill=color, outline='white')

    def handle_click(self, event):
        if self.game_over:
            self.reset_game()
        else:
            col = int(event.x // self.cell_width)
            self.play(col)
            self.draw_board()  # To show the last move

    def reset_game(self):
        self.board = [['-' for _ in range(self.cols)] for _ in range(self.rows)]
        self.turn = 'X'  # Player 1 always starts
        self.game_over = False
        self.draw_board()

    def play(self, col):
        if self.game_over:
            self.reset_game()
            return
        player_moved = self.drop_piece(col)
        self.draw_board()
        if player_moved:
            self.check_and_handle_game_end()
            self.change_turn()
            if not self.game_over:
                self.ai_move()
        else:
            self.draw_board()
            if not self.is_ai_playing:
                messagebox.showwarning("Error", "Column is full! Try a different one.")

    def drop_piece(self, col):
        if self.board[0][col] != '-':
            return False  # Column full
        for row in reversed(range(self.rows)):
            if self.board[row][col] == '-':
                self.board[row][col] = self.turn
                break
        return True

    def is_full(self):
        return all(self.board[0][col] != '-' for col in range(self.cols))

    def check_line(self, start_row, start_col, d_row, d_col):
        count = 0
        row, col = start_row, start_col
        while 0 <= row < self.rows and 0 <= col < self.cols and self.board[row][col] == self.turn:
            count += 1
            if count == self.win_length:
                return True
            row += d_row
            col += d_col
        return False
    
    def check_win(self):
        for row in range(self.rows):
            for col in range(self.cols):
                if self.board[row][col] == self.turn:
                    if (self.check_line(row, col, 0, 1) or  # Horizontal
                        self.check_line(row, col, 1, 0) or  # Vertical
                        self.check_line(row, col, 1, 1) or  # Diagonal /
                        self.check_line(row, col, 1, -1)):  # Diagonal \
                        return True
        return False

    def change_turn(self):
        self.turn = 'O' if self.turn == 'X' else 'X'

    def check_and_handle_game_end(self):
        if self.check_win():
            self.game_over = True
            if not self.is_ai_playing:
                messagebox.showinfo("Game Over", f"Player {self.turn} wins!")
        elif self.is_full():
            self.game_over = True
            if not self.is_ai_playing:
                messagebox.showinfo("Game Over", "Game is a draw!")

    def ai_move(self):
        if ((self.turn == 'X' and self.player1_type.get() != "Computer") or 
            (self.turn == 'O' and self.player2_type.get() != "Computer")):
            return  # Do not proceed if it's human's turn
        if (self.turn == 'X' and self.player1_type.get() == "Computer") or (self.turn == 'O' and self.player2_type.get() == "Computer"):
            self.master.after(300, lambda: self.execute_ai_move(self.turn))

    def execute_ai_move(self, player):
        # Choose the algorithm based on player type and selected algorithm
        algorithm = self.player1_algorithm.get() if player == 'X' else self.player2_algorithm.get()
        move = random.randint(0, self.cols-1)
        if algorithm == 'Default Opponent':
            opponent = DefaultOpponent()
        elif algorithm == 'Minimax':
            opponent = MinimaxOpponent()
        elif algorithm == 'Alpha-Beta Pruning':
            opponent = AlphaBetaOpponent()
        elif algorithm == 'Q-Learning':
            prev_state = self.get_state_representation()
            opponent = self.q_learning_opponent
        move = opponent.choose_move(self, player)
        if move is not None:
            self.play(move)
        
        # Update Q-table if Q-Learning was used
        if algorithm == 'Q-Learning':
            # Assume reward is 0 for ongoing game, 1 for win, -1 for loss
            reward = 0
            if self.check_win():
                reward = 1 if player == 'O' else -1  # Assuming 'O' is the Q-learning player
            elif self.is_full():
                reward = -1  # Penalize if the board is full and no one wins
            next_state = self.get_state_representation()
            done = self.game_over  # True if the game is over, otherwise False
            self.q_learning_opponent.update_q_table(self, prev_state, move, reward, next_state, done)
    
    def get_state_representation(self):
        state = ''
        for row in self.board:
            for cell in row:
                state += cell
        return state

    def train_ai(self):
        self.is_ai_playing = True
        iterations = 500
        # Define opponents for training
        opponents = [
            MinimaxOpponent(),
            AlphaBetaOpponent(),
            DefaultOpponent(),
            # QLearningOpponent()
        ]
        # initially explore while training
        self.q_learning_opponent.epsilon = 1
        for opponent in opponents:
            if isinstance(opponent, MinimaxOpponent):
                self.player1_algorithm.set('Minimax')
            elif isinstance(opponent, AlphaBetaOpponent):
                self.player1_algorithm.set('Alpha-Beta Pruning')
            elif isinstance(opponent, DefaultOpponent):
                self.player1_algorithm.set('Default Opponent')
                iterations = 1000000
            print(f"Starting training against {opponent.__class__.__name__}...")
            self.q_learning_opponent.train(self, iterations, opponent)

            # After training
            self.q_learning_opponent.save_q_table(self.q_learning_opponent.Q)  # Save the learned Q-table
        print("Training complete and Q-table saved.")
        self.is_ai_playing = False

    def evaluate_board(self, board, player):
        score = 0
        opp_player = 'X' if player == 'O' else 'O'
        # Center column preference remains a good heuristic.
        center_column = [board[i][self.cols // 2] for i in range(self.rows)]
        center_count = center_column.count(player)  # Assuming AI is 'O'
        score += center_count * 6  # Slightly increase the weight

        # Evaluate every row, column, and diagonal for potential scores
        for row in range(self.rows):
            for col in range(self.cols):
                if board[row][col] == '-':  # Only evaluate empty spaces for potential moves
                    score += self.score_position(board, row, col, player)  # Score for AI
                    score -= self.score_position(board, row, col, opp_player)  # Subtract score for opponent
        return score

    def score_position(self, board, row, col, player):
        score = 0
        opp_player = 'X' if player == 'O' else 'O'

        # Temporarily make the move on the board
        board[row][col] = player
        # Horizontal
        for c in range(max(0, col-3), min(self.cols-3, col+1)):
            window = board[row][c:c+4]
            score += self.evaluate_window(window, player)
        # Vertical
        if row <= self.rows - 4:
            window = [board[r][col] for r in range(row, row+4)]
            score += self.evaluate_window(window, player)
        # Positive Diagonal
        if row <= self.rows - 4 and 0 <= col <= self.cols - 4:
            window = [board[row+i][col+i] for i in range(4)]
            score += self.evaluate_window(window, player)
        # Negative Diagonal
        if row >= 3 and 0 <= col <= self.cols - 4:
            window = [board[row-i][col+i] for i in range(4)]
            score += self.evaluate_window(window, player)
        # Undo the move
        board[row][col] = '-'
        return score
    
    def evaluate_window(self, window, player):
        score = 0
        opp_player = 'X' if player == 'O' else 'O'

        # Count the pieces in the window
        player_count = window.count(player)
        opp_count = window.count(opp_player)
        empty_count = window.count('-')

        # Adjust scoring to prioritize blocking opponent wins
        if player_count == 3 and empty_count == 1:
            score += 100  # Favor moves that lead to a win
        elif opp_count == 3 and empty_count == 1:
            score -= 150  # Heavily penalize allowing the opponent to get 3 in a row
        if player_count == 2 and empty_count == 2:
            score += 10
        elif opp_count == 2 and empty_count == 2:
            score -= 50  # Penalize allowing the opponent to get 2 in a row with space
        return score


def main():
    root = tk.Tk()
    root.title("Connect 4")
    Connect4GUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
