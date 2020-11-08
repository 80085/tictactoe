import pickle
from abc import ABC, abstractmethod

from tictactoe.agent import QLearningAgent
from tictactoe.board import Board


class Player(ABC):
    def __init__(self, name: str, symbol: str):
        """
        A TicTacToe player

        :param name: name of player
        :param symbol: 'x' or 'o'
        """
        self.name = name
        self.symbol = symbol

    @abstractmethod
    def choose_action(self, board: Board):
        pass

    @abstractmethod
    def end_round(self, reward: float):
        pass


class Computer(Player):
    def __init__(self, name: str, symbol: str, exp_rate=0.3):
        super().__init__(name, symbol)
        self.agent = QLearningAgent(policy=self._load_policy(), exp_rate=exp_rate)

    def _copy_board_and_get_new_hash(self, action, board: Board):
        new_board = board.copy()
        new_board.put(self.symbol, action)
        return new_board.hash

    def choose_action(self, board: Board):
        action = self.agent.choose_action(
            board.available_positions(),
            lambda x: self._copy_board_and_get_new_hash(x, board)
        )
        board.put(self.symbol, action)

    def end_round(self, reward: float):
        self.agent.end_iteration(reward)

    def save_policy(self):
        with open('policy_' + str(self.symbol), 'wb') as f:
            pickle.dump(self.agent.states, f)

    def _load_policy(self):
        try:
            with open('policy_' + str(self.symbol), 'rb') as f:
                return pickle.load(f)
        except FileNotFoundError:
            return None


class Human(Player):

    def choose_action(self, board: Board):
        while True:
            print(board.pretty())
            row = int(input('Row: ')) - 1
            col = int(input('Col: ')) - 1
            try:
                board.put(self.symbol, (row, col))
                break
            except ValueError:
                pass

    def end_round(self, reward: float):
        if reward == 1:
            print(f'Congratulations {self.name}! You won!')
        elif reward == 0:
            print(f'Too bad {self.name}, you lost.')
        else:
            print(f'Not bad, not good. You drew the game {self.name}.')
