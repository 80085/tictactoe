import itertools
import unittest

from tictactoe.board import Board


class BoardTest(unittest.TestCase):
    full_grid = list(itertools.product(range(3), repeat=2))

    def test_board_created_with_9_available_positions(self):
        positions = Board().available_positions()
        self.assertEqual(9, len(positions))
        self.assertEqual(self.full_grid, positions)

    def test_board_available_positions_updated(self):
        board = Board()
        board._grid[0] = 1
        board._grid[5] = -1
        positions = board.available_positions()
        self.assertEqual(7, len(positions))
        self.assertEqual(
            [p for p in self.full_grid if p not in [(0, 0), (1, 2)]],
            positions
        )

    def test_invalid_input_does_not_consume_position(self):
        board = Board()
        with self.assertRaisesRegex(ValueError, 'Invalid symbol'):
            board.put(' ', (0, 0))
        with self.assertRaisesRegex(ValueError, 'Invalid coordinate'):
            board.put('x', (0, 4))
        self.assertEqual(9, len(board.available_positions()))

    def test_game_ends_on_3_in_a_row(self):
        board = Board()
        for col in range(3):
            board.put('x', (0, col))
        self.assertTrue(board.ended)
        self.assertEqual('x', board.winner)

    def test_game_ends_when_grid_is_full(self):
        board = Board()
        board.put('x', (1, 1))
        board.put('o', (0, 0))
        board.put('x', (2, 0))
        board.put('o', (0, 2))
        board.put('x', (0, 1))
        board.put('o', (2, 1))
        board.put('x', (1, 2))
        board.put('o', (1, 0))
        board.put('x', (2, 2))
        self.assertTrue(board.ended)
        self.assertIsNone(board.winner)
        self.assertEqual(0, len(board.available_positions()))

    def test_may_not_play_an_ended_game(self):
        board = Board()
        for row in range(3):
            board.put('o', (row, 0))
        self.assertTrue(board.ended)
        with self.assertRaisesRegex(ValueError, 'Game is already over!'):
            board.put('o', (1, 1))


if __name__ == '__main__':
    unittest.main()
