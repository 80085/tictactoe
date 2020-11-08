import pickle
from abc import ABC, abstractmethod

import numpy as np

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
        self.exp_rate = exp_rate
        self.decay_gamma = 0.9
        self.lr = 0.2
        self.states_value = self._load_policy() or {}
        self.states = []  # record all positions taken during one game

    def choose_action(self, board: Board):
        action = self._get_random_action(board) \
            if np.random.uniform(0, 1) < self.exp_rate \
            else self._find_best_action(board)
        board.put(self.symbol, action)
        self.states.append(board.hash)

    def end_round(self, reward: float):
        for state in reversed(self.states):
            if state not in self.states_value:
                self.states_value[state] = 0
            self.states_value[state] += self.lr * (self.decay_gamma * reward - self.states_value[state])
            reward = self.states_value[state]
        self.states.clear()

    def save_policy(self):
        with open('policy_' + str(self.symbol), 'wb') as f:
            pickle.dump(self.states_value, f)

    def _load_policy(self):
        try:
            with open('policy_' + str(self.symbol), 'rb') as f:
                return pickle.load(f)
        except FileNotFoundError:
            return None

    @staticmethod
    def _get_random_action(board: Board):
        positions = board.available_positions()
        idx = np.random.choice(len(positions))
        return positions[idx]

    def _find_best_action(self, board: Board):
        value_max = -999
        action = None
        for p in board.available_positions():  # for all available positions
            next_board = board.copy()  # create a copy of the board we can freely modify
            next_board.put(self.symbol, p)  # put our symbol on that square
            # if we don't know that state, we rate it low
            v = self.states_value.get(next_board.hash, 0)
            if v >= value_max:  # find the best action
                value_max = v
                action = p
        return action


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
