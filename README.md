# TicTacToe and Connect4 - Adversarial Search and Reinforcement Learning

This project focuses on the implementation and analysis of various AI algorithms for playing TicTacToe and Connect4. The aim is to explore adversarial search techniques and reinforcement learning to develop intelligent agents that can play these games effectively. Both `TicTacToe` and `Connect4` are implemented using `Python` and the `tkinter` library to provide a graphical user interface (GUI). This allows users to play the games interactively and visualize the AI's decision-making process.

**Objective:**

The primary objective of this project is to apply adversarial search and reinforcement learning techniques to the TicTacToe and Connect4 games, comparing the performance of different AI algorithms in various scenarios. The analysis includes:
- Comparing the performance of each algorithm against a default opponent.
- Evaluating how different algorithms perform against each other.
- Analyzing the efficiency and effectiveness of Minimax with and without Alpha Beta Pruning.
- Assessing the learning capabilities of the Q-Learning algorithm.
  
**Algorithms and Opponents:**
1. **Minimax**: A classic AI algorithm that explores all possible moves to find the optimal strategy by maximizing the AI's chances of winning and minimizing the opponent's chances.
2. **Minimax with Alpha Beta Pruning**: An optimized version of the Minimax algorithm that prunes branches of the search tree that cannot influence the final decision, significantly improving efficiency.
3. **Q-Learning**: A reinforcement learning algorithm that allows the AI to learn from experience by updating its knowledge of the game environment over time.
4. **Default Opponent**: A semi-intelligent opponent that makes moves based on simple heuristics, such as selecting winning moves, blocking the opponent's winning moves, or choosing random moves when no immediate threats or opportunities are present.

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
