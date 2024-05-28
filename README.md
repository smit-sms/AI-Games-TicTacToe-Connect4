# TicTacToe and Connect4 - Adversarial Search and Reinforcement Learning

This project focuses on implementing and analyzing the performance of various AI algorithms for playing TicTacToe and Connect4. The algorithms implemented include:
- Minimax
- Minimax with Alpha Beta Pruning
- Q-Learning Algorithm
- Default Opponent (Semi-Intelligent)

**Objective:**

The main objective is to apply adversarial search and reinforcement learning techniques to TicTacToe and Connect4 games, comparing their performance in various scenarios including Human vs AI, AI vs AI, and Human vs Human.

**Algorithms and Opponents:**
1. **Default Opponent**: Implements basic strategies such as selecting winning moves, blocking the opponent's winning moves, or choosing random moves.
2. **Minimax Algorithm**: Explores all possible moves to make optimal decisions by maximizing the AI player's chances of winning and minimizing the opponent's chances.
3. **Minimax with Alpha Beta Pruning**: Optimizes the Minimax algorithm by pruning branches that cannot influence the final decision, improving efficiency.
4. **Q-Learning**: Uses reinforcement learning to learn the value of actions in different states through experience, allowing the AI to improve over time.

**Key Features:**
1. GUI: User-friendly graphical interface for both games.
2. AI Algorithms: Multiple algorithms are available for AI players.
3. Training: Train Q-Learning AI using the 'Train AI' button.
4. Performance Analysis: Run matchups between different algorithms and save results in CSV files.

## Implementation Details
**TicTacToe**

The TicTacToe game uses the `Tkinter` library for the graphical user interface (GUI). The implementation includes methods for making moves, checking for valid moves, switching players, and checking for win/draw conditions.

**Connect4**

Connect4 also uses the `Tkinter` library for the GUI and allows game modes similar to TicTacToe. The board size is **6x7**, which is standard for Connect4. The game includes methods for making moves, checking for valid moves, switching players, and checking for win/draw conditions.

**The Games can be played in three modes:**
- Human vs Human
- Human vs Computer
- Computer vs Computer

## Prerequisites
- Python 3.9 and above
- Required libraries:
  ```
  pip install tkinter tqdm numpy pickle
  ```

## Project Structure
- `TicTacToe/TicTacToe.py`: Main script for running the TicTacToe game.
- `TicTacToe/TicTacToeOpponents.py`: Contains implementations of various opponents for TicTacToe.
- `Connect4/Connect4.py`: Main script for running the Connect4 game.
- `Connect4/Connect4Opponents.py`: Contains implementations of various opponents for Connect4.

## Running the Project
To run the **TicTacToe GUI**, navigate to the TicTacToe directory and execute the following commands:
```
cd TicTacToe
python TicTacToe.py
```
To run the **Connect4 GUI**, navigate to the Connect4 directory and execute the following commands:
```
cd Connect4
python Connect4.py
```

**Training Q-Learning AI**

Use the `Train AI` button in the GUI to train the Q-Learning AI. The training progress will be displayed on the console, and the trained model will be saved in a pickle file in the respective game folder.

**Performance Analysis**

Use the `Analyze Performance` button in the GUI to run matchups between different algorithms. The results will be saved in a CSV file in the respective game folder.

**Note**
> The algorithms include options: **`Minimax`**, **`Minimax with Alpha Beta Pruning`**, **`Q-Learning Algorithm`**, and **`Default Opponent`**. You can play the game against any of these AIs with one player as human and the other as AI, or even AI vs AI.
