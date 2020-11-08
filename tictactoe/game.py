import itertools

from tictactoe.board import Board
from tictactoe.player import Player


class Game:
    def __init__(self, player_one: Player, player_two: Player):
        self.player_one = player_one
        self.player_two = player_two
        self._validate()

    def _validate(self):
        if self.player_one.symbol == self.player_two.symbol:
            raise ValueError('Both player cannot have the same symbol')

    def play(self):
        board = Board()
        players = itertools.cycle([self.player_one, self.player_two])
        current_player = None
        while not board.ended:
            current_player = next(players)
            current_player.choose_action(board)
        if board.winner is not None:
            current_player.end_round(1)
            next(players).end_round(0)
        else:
            current_player.end_round(0.2)
            next(players).end_round(0.5)
        return board.pretty()
