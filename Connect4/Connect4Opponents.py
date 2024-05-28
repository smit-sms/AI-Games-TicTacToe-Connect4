import numpy as np
import pickle
import random
from tqdm import tqdm

class Opponent:
    def __init__(self):
        self.depth = 4  # Depth for minimax and alpha-beta pruning
    
    def choose_move(self, game, player):
        pass
    
    def simulate_drop_piece(self, game, board, col, player):
        temp_board = [row[:] for row in board]
        for row in reversed(range(game.rows)):
            if temp_board[row][col] == '-':
                temp_board[row][col] = player
                return temp_board, True
        return board, False  # Return the unchanged board and False if the column was full

class MinimaxOpponent(Opponent):
    def minimax(self, game, board, depth, player, maximizingPlayer):
        if depth == 0 or game.check_win() or game.is_full():
            return game.evaluate_board(board, player)

        if maximizingPlayer:
            maxEval = float('-inf')
            for col in range(game.cols):
                temp_board, valid_move = self.simulate_drop_piece(game, board, col, 'O')  # Assuming 'O' is maximizing
                if valid_move:
                    eval = self.minimax(game, temp_board, depth-1, player, False)
                    maxEval = max(maxEval, eval)
            return maxEval
        else:
            minEval = float('inf')
            for col in range(game.cols):
                temp_board, valid_move = self.simulate_drop_piece(game, board, col, 'X')  # Assuming 'X' is minimizing
                if valid_move:
                    eval = self.minimax(game, temp_board, depth-1, player, True)
                    minEval = min(minEval, eval)
            return minEval

    def choose_move(self, game, player):
        best_score = float('-inf')
        possible_moves = []
        for col in range(game.cols):
            if game.board[0][col] == '-':
                temp_board, valid_move = self.simulate_drop_piece(game, game.board, col, player)
                if valid_move:
                    score = self.minimax(game, temp_board, self.depth, player, player == 'O')
                    if score > best_score:
                        best_score = score
                        possible_moves = [(score, col)]
                    elif score == best_score:
                        possible_moves.append((score, col))
        if len(possible_moves) > 1:
            return random.choice([col for score, col in possible_moves])
        else:
            return possible_moves[0][1]

class AlphaBetaOpponent(Opponent):
    def minimax_with_alpha_beta(self, game, board, depth, alpha, beta, player, maximizingPlayer):
        if depth == 0 or game.check_win() or game.is_full():
            return game.evaluate_board(board, player)
        if maximizingPlayer:
            maxEval = float('-inf')
            for col in range(game.cols):
                temp_board, valid_move = self.simulate_drop_piece(game, board, col, 'O')  # Assuming 'O' is maximizing
                if valid_move:
                    eval = self.minimax_with_alpha_beta(game, temp_board, depth-1, alpha, beta, player, False)
                    maxEval = max(maxEval, eval)
                    alpha = max(alpha, eval)
                    if beta <= alpha:
                        break
            return maxEval
        else:
            minEval = float('inf')
            for col in range(game.cols):
                temp_board, valid_move = self.simulate_drop_piece(game, board, col, 'X')  # Assuming 'X' is minimizing
                if valid_move:
                    eval = self.minimax_with_alpha_beta(game, temp_board, depth-1, alpha, beta, player, True)
                    minEval = min(minEval, eval)
                    beta = min(beta, eval)
                    if beta <= alpha:
                        break
            return minEval
        
    def choose_move(self, game, player):
        best_score = float('-inf')
        possible_moves = []
        for col in range(game.cols):
            if game.board[0][col] == '-':
                temp_board, valid_move = self.simulate_drop_piece(game, game.board, col, player)
                if valid_move:
                    score = self.minimax_with_alpha_beta(game, temp_board, self.depth, float('-inf'), float('inf'), player, player == 'O')
                    if score > best_score:
                        best_score = score
                        possible_moves = [(score, col)]
                    elif score == best_score:
                        possible_moves.append((score, col))
        if len(possible_moves) > 1:
            return random.choice([col for score, col in possible_moves])
        else:
            return possible_moves[0][1]

class DefaultOpponent(Opponent):
    def get_move(self, game, player):
        for col in range(game.cols):
            temp_board, valid_move = self.simulate_drop_piece(game, game.board, col, player)
            if valid_move and self.check_win_on_board(game, temp_board, player):
                return col
    
    def choose_move(self, game, player):
        opp_player = 'X' if player == 'O' else 'O'
        winning_move = self.get_move(game, player)  # Check for a winning move first
        if winning_move:
            return winning_move
        blocking_move = self.get_move(game, opp_player) # If no winning move, check for a blocking move
        if blocking_move:
            return blocking_move
        # No immediate win or block, choose center column if available
        if game.board[game.rows-1][game.cols//2] == '-':
            return game.cols//2
        # Choose a random move as a fallback
        valid_moves = [col for col in range(game.cols) if game.board[0][col] == '-']
        return random.choice(valid_moves) if valid_moves else None
    
    def check_win_on_board(self, game, board, player):
        for row in range(game.rows):    # Check all rows for a win
            for col in range(game.cols - 3):
                if board[row][col] == player and board[row][col + 1] == player and board[row][col + 2] == player and board[row][col + 3] == player:
                    return True
        for col in range(game.cols):    # Check all columns for a win
            for row in range(game.rows - 3):
                if board[row][col] == player and board[row + 1][col] == player and board[row + 2][col] == player and board[row + 3][col] == player:
                    return True
        for row in range(game.rows - 3):    # Check positive diagonal
            for col in range(game.cols - 3):
                if board[row][col] == player and board[row + 1][col + 1] == player and board[row + 2][col + 2] == player and board[row + 3][col + 3] == player:
                    return True
        for row in range(3, game.rows): # Check negative diagonal
            for col in range(game.cols - 3):
                if board[row][col] == player and board[row - 1][col + 1] == player and board[row - 2][col + 2] == player and board[row - 3][col + 3] == player:
                    return True
        return False

class QLearningOpponent(Opponent):
    def __init__(self, epsilon=0, alpha=0.6, gamma=0.9, epsilon_decay=0.995, epsilon_min=0.01):
        self.Q = {}  # Q-table
        self.epsilon = epsilon  # Exploration rate
        self.alpha = alpha  # Learning rate
        self.gamma = gamma  # Discount factor
        self.epsilon_decay = epsilon_decay  # Decay rate for epsilon
        self.epsilon_min = epsilon_min  # Minimum value for epsilon
        self.load_q_table()

    def get_state(self, game):
        # Convert the game board to a tuple to use as a dictionary key
        return tuple(tuple(row) for row in game.board)

    def choose_move(self, game, player):
        state = self.get_state(game)
        if np.random.rand() < self.epsilon: # Exploration: Choose a random action
            return np.random.choice([col for col in range(game.cols) if game.board[0][col] == '-'])
        else: # Exploitation: Choose the best action based on current Q-values
            q_values = [self.Q.get((state, col), 0) for col in range(game.cols)]
            max_q_value = max(q_values)
            actions_with_max_q_value = [col for col, q in enumerate(q_values) if q == max_q_value]
            return np.random.choice(actions_with_max_q_value)

    def update_q_table(self, game, prev_state, action, reward, next_state, done):
        prev_q_value = self.Q.get((prev_state, action), 0)
        if done:
            self.Q[(prev_state, action)] = prev_q_value + self.alpha * (reward - prev_q_value)
        else:
            max_future_q = max([self.Q.get((next_state, col), 0) for col in range(game.cols)])
            self.Q[(prev_state, action)] = prev_q_value + self.alpha * (reward + self.gamma * max_future_q - prev_q_value)

    def train(self, game, iterations, opponent):
        for _ in tqdm(range(iterations)):
            game.reset_game()  # Reset the game to start a new game
            while not game.game_over:
                if game.turn == 'O':  # 'O' is the Q-Learning agent
                    # Capture the state before making a move
                    prev_state = game.get_state_representation()
                    # Choose and make a move based on the current policy or exploration
                    action = game.q_learning_opponent.choose_move(game, game.turn)
                    game.play(action)
                    # Capture the new state and compute the reward after the move
                    next_state = game.get_state_representation()

                    reward = 0
                    if game.check_win():
                        reward = 1 if game.turn == 'O' else -1  # Reward 1 for winning, -1 for losing
                    elif game.is_full():
                        reward = -0.5  # Slight negative reward for a draw
                    done = game.game_over  # Check if the game is over
                    # Update the Q-table based on the move
                    game.q_learning_opponent.update_q_table(game, prev_state, action, reward, next_state, done)
                else:
                    # Opponent's turn to play
                    col = opponent.choose_move(game, game.turn)
                    game.play(col)
            self.epsilon = max(self.epsilon_min, self.epsilon * self.epsilon_decay)

    def save_q_table(self, q_table):
        with open('q_table_connect4.pkl', 'wb') as f:
            pickle.dump(q_table, f)

    def load_q_table(self):
        try:
            with open('q_table_connect4.pkl', 'rb') as f:
                self.Q = pickle.load(f)
        except FileNotFoundError:
            self.Q = {}
