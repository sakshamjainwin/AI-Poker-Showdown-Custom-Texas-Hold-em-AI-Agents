
# **Texas Hold'em Poker : Custom AI Agents**

This project simulates a competitive Texas Hold'em poker environment where multiple AI agents with unique strategies compete against each other. Using the `pypokerengine` library, this project allows for testing, benchmarking, and enhancing poker-playing agents through various decision-making strategies.

---

## **Project Overview**

The aim of this project is to develop, test, and evaluate AI players for Texas Hold'em poker. Multiple custom agents, each implementing distinct strategies, are included, along with baseline agents for comparison. This project serves as a foundation for understanding AI decision-making in poker and provides an excellent framework for experimenting with new strategies.

---

## **Features**

- **Custom AI Players**: Six AI players (`CustomPlayerSaksham_1` to `CustomPlayerSaksham_6`) designed with unique poker strategies, ranging from basic randomization to advanced logic incorporating win-rate estimation and bluffing.
- **Game Simulation**: A Python-based game engine for simulating poker matches.
- **Baseline Agents**: Includes pre-built agents (`FishPlayer`, `RandomPlayer`, `HonestPlayer`) for testing and benchmarking.
- **Machine Learning Integration**: Supports PyTorch-based decision-making models for AI players.
- **Customizable Framework**: Extendable structure for building and testing new agents.

---

## **Folder Structure**

- **`game.py`**: The main script to set up and run the poker game simulation.
- **`examples/players/`**: Contains all player implementations (baseline and custom).
- **`model.pth`**: Pre-trained PyTorch model used by some AI players.
- **`requirements.txt`**: Specifies project dependencies.
- **`round_robin.py`**: Simulates a round-robin tournament among agents.
- **`participants.csv`**: Records data and performance metrics of the players.

---

## **Custom Players**

Each custom agent (`CustomPlayerSaksham_X`) implements a unique strategy, as described below:

1. **`CustomPlayerSaksham_1`**:
   - Implements a basic strategy with random decision-making for calls, folds, and raises.
   - Includes logic to estimate the win rate of hole cards using Monte Carlo simulations.

2. **`CustomPlayerSaksham_2`**:
   - Enhances the logic by factoring in community cards to estimate hand strength.
   - Uses probabilistic decision-making for actions.

3. **`CustomPlayerSaksham_3`**:
   - A more advanced player with:
     - Win-rate calculations.
     - Bluffing mechanics.
     - Stack management to optimize decisions.

4. **`CustomPlayerSaksham_4`**:
   - Simplified simulation-based strategy focusing on community card analysis.
   - Trades complexity for faster computation.

5. **`CustomPlayerSaksham_5`**:
   - A hybrid strategy with enhanced randomization for more diverse gameplay.
   - Improves over `Saksham_1` by introducing adaptive decision-making.

6. **`CustomPlayerSaksham_6`**:
   - Combines win-rate estimation and randomness for a dynamic, unpredictable playstyle.
   - Adaptable to opponent behaviors during gameplay.

---

## **How to Run**

Follow these steps to run the project:

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your_username/ai-poker-showdown.git
   cd ai-poker-showdown
   ```

2. **Install Dependencies**:
   ```bash
   python -m venv env
   source env/bin/activate  # Linux/Mac
   env\Scripts\activate     # Windows
   pip install -r requirements.txt
   ```

3. **Run the Game**:
   ```bash
   python game.py
   ```

---

## **Adding Your Own Agent**

You can create your own AI poker player by following these steps:

1. Create a new file in `examples/players/`, e.g., `CustomPlayerYourName.py`.
2. Extend the `BasePokerPlayer` class and implement its required methods.
3. Example template:
   ```python
   from pypokerengine.players import BasePokerPlayer

   class CustomPokerPlayer(BasePokerPlayer):
       def declare_action(self, valid_actions, hole_card, round_state):
           # Example strategy
           return 'call', 0
   ```
4. Add your custom player to the `game.py` script.
5. Run the game to test your player against others.

---
