import numpy as np
import pickle
import random
from tqdm import tqdm


class Opponent:
    def choose_move(self, game):
        pass

    def evaluate(self, game):
        if game.check_win('X'):
            return 10
        elif game.check_win('O'):
            return -10
        else:
            return 0


class MinimaxOpponent(Opponent):
    def minimax(self, game, depth, is_maximizing):
        score = self.evaluate(game)
        if score == 10: # If Maximizer has won the game return evaluated score
            return score - depth
        if score == -10: # If Minimizer has won the game return evaluated score
            return score + depth
        # If there are no more moves and no winner then it is a tie
        if game.check_draw():
            return 0

        # If this maximizer's move
        if is_maximizing:
            best = -1000
            # Traverse all cells
            for (i, j) in game.get_empty_cells():
                # Make the move
                game.board[i][j] = 'X'
                # Call minimax recursively and choose the maximum value
                best = max(best, self.minimax(game, depth + 1, not is_maximizing))
                # Undo the move
                game.board[i][j] = ' '
            return best
        else:
            best = 1000
            # Traverse all cells
            for (i, j) in game.get_empty_cells():
                # Make the move
                game.board[i][j] = 'O'
                # Call minimax recursively and choose the minimum value
                best = min(best, self.minimax(game, depth + 1, not is_maximizing))
                # Undo the move
                game.board[i][j] = ' '
            return best

    def choose_move(self, game):
        best_score = -1000
        possible_moves = []
        # Traverse all cells and return the cell with optimal value.
        for (i, j) in game.get_empty_cells():
            game.board[i][j] = 'X'  # Make the move as X (AI)
            score = self.minimax(game, 0, False)  # Evaluate this move
            game.board[i][j] = ' '  # Undo the move

            # If the value of the current move is more than the best score then
            # update best score
            if score > best_score:
                best_score = score
                possible_moves = [(score, (i,j))]
            elif score == best_score:
                possible_moves.append((score, (i,j)))
        if len(possible_moves) > 1:
            return random.choice([move for score, move in possible_moves])
        else:
            return possible_moves[0][1]
    

class MinimaxWithAlphaBetaOpponent(Opponent):
    def minimax_with_alpha_beta(self, game, depth, is_maximizing, alpha, beta):
        score = self.evaluate(game)
        if score == 10:  # If Maximizer has won the game return evaluated score
            return score - depth
        if score == -10: # If Minimizer has won the game return evaluated score
            return score + depth
        # If there are no more moves and no winner then it is a tie
        if game.check_draw():
            return 0

        # If this maximizer's move
        if is_maximizing:
            best = -1000
            # Traverse all cells
            for (i, j) in game.get_empty_cells():
                game.board[i][j] = 'X' # Make the move
                # Call minimax recursively and choose the maximum value
                value = self.minimax_with_alpha_beta(game, depth + 1, False, alpha, beta)
                game.board[i][j] = ' ' # Undo the move
                best = max(best, value)
                # Update the alpha value
                alpha = max(alpha, best)
                if beta <= alpha:
                    break
            return best
        else:
            best = 1000
            # Traverse all cells
            for (i, j) in game.get_empty_cells():
                game.board[i][j] = 'O' # Make the move
                # Call minimax recursively and choose the minimum value
                value = self.minimax_with_alpha_beta(game, depth + 1, True, alpha, beta)
                game.board[i][j] = ' ' # Undo the move
                best = min(best, value)
                # Update the beta value
                beta = min(beta, best)
                if beta <= alpha:
                    break
            return best

    def choose_move(self, game):
        best_score = -1000
        alpha = -1000
        beta = 1000
        possible_moves = []
        # Traverse all cells and return the cell with optimal value.
        for (i, j) in game.get_empty_cells():
            game.board[i][j] = 'X'  # Make the move as X (AI)
            score = self.minimax_with_alpha_beta(game, 0, False, alpha, beta)  # Evaluate this move
            game.board[i][j] = ' '  # Undo the move 
            # If the value of the current move is more than the best score then
            # update best score
            if score > best_score:
                best_score = score
                possible_moves = [(score, (i,j))]
            elif score == best_score:
                possible_moves.append((score, (i,j)))
        if len(possible_moves) > 1:
            return random.choice([move for score, move in possible_moves])
        else:
            return possible_moves[0][1]


class DefaultOpponent(Opponent):
    def get_winning_move(self, game):
        for (row, col) in game.get_empty_cells():
            game.board[row][col] = game.current_player
            if game.check_win(game.current_player):
                game.board[row][col] = ' '
                return (row, col)  # Return this winning move
            game.board[row][col] = ' '
        return None

    def get_blocking_move(self, game):
        opponent = 'O' if game.current_player == 'X' else 'X'
        for (row, col) in game.get_empty_cells():
            game.board[row][col] = opponent
            if game.check_win(opponent):
                game.board[row][col] = ' '
                return (row, col)  # Return this blocking move
            game.board[row][col] = ' '

    def choose_move(self, game):
        # Check for a winning move first
        winning_move = self.get_winning_move(game)
        if winning_move:
            return winning_move

        # If no winning move, check for a blocking move
        blocking_move = self.get_blocking_move(game)
        if blocking_move:
            return blocking_move

        # If no winning or blocking move, choose a random empty cell
        return game.get_empty_cells()[0]


class QLearningOpponent(Opponent):
    def __init__(self):
        self.q_table = {}
        self.learning_rate = 0.1
        self.gamma = 0.95  # Discount factor
        self.epsilon = 0.1  # Exploration rate
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995  # Decay rate for epsilon
        self.load_q_table()

    def get_state(self, game):
        return str(game.board) # Convert the game board to a string to use as a state

    def update_q_value(self, game, state, action, reward, next_state):
        old_value = self.q_table.get((state, tuple(action)), 0)
        empty_cells = game.get_empty_cells()
        if empty_cells:  # Check if there are any empty cells left
            next_max = max(self.q_table.get((next_state, a), 0) for a in empty_cells)
        else:
            next_max = 0 # Default value when no moves are available
        self.q_table[(state, tuple(action))] = old_value + self.learning_rate * (reward + self.gamma * next_max - old_value)
    
    def train(self, game, iterations=1000):
        for iteration in tqdm(range(iterations), desc="Training AI"):
            game.reset()
            # Decrease epsilon over time
            self.epsilon = max(self.epsilon_min, self.epsilon - self.epsilon_min * (iteration / 200))
            state = self.get_state(game)

            while not game.check_win('X') and not game.check_win('O') and not game.check_draw():
                action = self.choose_move(game)
                game.make_move(action[0], action[1], game.current_player)

                reward = 0
                if game.check_win(game.current_player):
                    reward = 1
                elif game.check_draw():
                    reward = 0.5
                else:
                    reward = 0
                
                next_state = self.get_state(game)
                self.update_q_value(game, state, action, reward, next_state)

                state = next_state
                game.switch_player()
        self.save_q_table()

    def load_q_table(self):
        try:
            with open('q_table_tictactoe.pkl', 'rb') as f:
                self.q_table = pickle.load(f)
        except FileNotFoundError:
            self.q_table = {}

    def save_q_table(self):
        with open('q_table_tictactoe.pkl', 'wb') as f:
            pickle.dump(self.q_table, f)

    def choose_move(self, game):
        state = self.get_state(game)
        if np.random.uniform(0, 1) < self.epsilon:
            action = random.choice(game.get_empty_cells())  # Explore
        else:
            q_values = {action: self.q_table.get((state, action), 0) for action in game.get_empty_cells()}
            max_q = max(q_values.values())
            action = random.choice([a for a, q in q_values.items() if q == max_q])  # Exploit
        return action
