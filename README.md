# Tic Tac Toe
A command line based TicTacToe game with reinforced learning. 
The agent must first be trained which is done vs. another agent:

    python application.py train --iterations 10000
The policy is saved and will be reused for next training session. 

The game can be played as either x or o, where x plays first

    python application.py play --symbol o
    