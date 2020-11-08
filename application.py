import argparse

import tqdm

from tictactoe.game import Game
from tictactoe.player import Computer, Human


def train_agent(iterations):
    player_x = Computer('x', 'x', exp_rate=0.3)
    player_o = Computer('o', 'o', exp_rate=0.3)
    game = Game(player_x, player_o)
    for _ in tqdm.tqdm(range(iterations)):
        game.play()
    player_x.save_policy()
    player_o.save_policy()


def single_play(player_symbol):
    if player_symbol == 'x':
        play_game(Game(Human('Player One', 'x'), Computer('Player Two', 'o', exp_rate=0)))
    else:
        play_game(Game(Computer('Player One', 'x', exp_rate=0), Human('Player Two', 'o')))


def multi_play():
    play_game(Game(Human('Player One', 'x'), Human('Player Two', 'o')))


def play_game(game):
    while True:
        print(game.play())
        if input('Play again? (y/n): ').lower() != 'y':
            break


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('mode', choices=['single', 'multi', 'train'])
    parser.add_argument('--symbol', default='x', choices=['x', 'o'], help='Your symbol. x starts the game')
    parser.add_argument('--iterations', type=int, default=1000, help='How many games to train')
    args = parser.parse_args()
    if args.mode == 'single':
        single_play(args.symbol)
    elif args.mode == 'multi':
        multi_play()
    elif args.mode == 'train':
        train_agent(args.iterations)
