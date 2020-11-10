import argparse

import tqdm

from tictactoe.game import Game
from tictactoe.player import Computer, Human


def train_agent(iterations):
    player_x = Computer('x')
    player_o = Computer('o')
    game = Game(player_x, player_o)
    for _ in tqdm.tqdm(range(iterations)):
        game.play()
    player_x.save_policy()
    player_o.save_policy()


def play_game(player_symbol):
    if player_symbol == 'x':
        game = Game(Human('x'), Computer('o', exp_rate=0.0))
    else:
        game = Game(Computer('x', exp_rate=0.0), Human('o'))
    while True:
        print(game.play())
        if input('Play again? (y/n): ').lower() != 'y':
            break


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('mode', choices=['play', 'train'])
    parser.add_argument('--symbol', default='x', choices=['x', 'o'], help='Your symbol. x starts the game')
    parser.add_argument('--iterations', type=int, default=10000, help='How many games to train')
    args = parser.parse_args()
    if args.mode == 'play':
        play_game(args.symbol)
    elif args.mode == 'train':
        train_agent(args.iterations)
