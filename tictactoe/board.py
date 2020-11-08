import numpy as np


class Board:
    _symbol_to_internal = {'x': 1, 'o': -1}
    _internal_to_symbol = {1: 'x', -1: 'o', 0: ' '}

    def __init__(self):
        self._grid = np.zeros(9)
        self._winner = None

    def put(self, symbol: str, cord: tuple):
        if self.ended:
            raise ValueError('Game is already over!')
        if cord not in self.available_positions():
            raise ValueError(f'Invalid coordinate: {cord}')
        row, col = cord
        try:
            self._grid[row * 3 + col] = self._symbol_to_internal[symbol]
        except KeyError:
            raise ValueError(f'Invalid symbol: {symbol}. Valid options: {self._symbol_to_internal.keys()}')
        self._winner = self._find_winner()

    def available_positions(self):
        return [(e // 3, e % 3) for e, v in enumerate(self._grid) if v == 0]

    @property
    def ended(self) -> bool:
        return not (self._winner is None and 0 in self._grid)

    @property
    def winner(self) -> str:
        return None if self._winner is None else self._internal_to_symbol[self._winner]

    def _find_winner(self):
        # rows
        for i in range(0, 9, 3):
            if abs(sum(self._grid[i:i + 3])) == 3:
                return self._grid[i]
        # columns
        for i in range(3):
            if abs(sum(self._grid[i::3])) == 3:
                return self._grid[i]
        # diagonal 1
        if abs(sum(self._grid[0:9:4])) == 3:
            return self._grid[0]
        # diagonal 2
        if abs(sum(self._grid[2:7:2])) == 3:
            return self._grid[2]
        return None

    @property
    def hash(self):
        return str(self._grid)

    def copy(self):
        copy = Board()
        copy._grid = self._grid.copy()
        return copy

    def __repr__(self):
        return str(self._grid.reshape((3, 3)))

    def pretty(self):
        s = '-' * 13
        for i in range(0, 9, 3):
            s += '\n| ' + ' | '.join(self._internal_to_symbol[sign] for sign in self._grid[i:i + 3]) + ' |'
            s += '\n' + '-' * 13
        return s
