import collections

import numpy as np


class QLearningAgent:
    def __init__(self, policy=None, exp_rate=0.3, learning_rate=0.2, decay_gamma=0.9):
        self.exp_rate = exp_rate
        self.decay_gamma = decay_gamma
        self.lr = learning_rate
        self.states = collections.defaultdict(float, policy or {})
        self.states_history = []

    def choose_action(self, actions: list, state_hash_function):
        """
        Let the agent choose one action based on its policy and setup
        :param actions: a list of possible actions
        :param state_hash_function: a function to generate the hash of new state, for a given action
        :return: the agents action
        """
        action = self._get_random_action(actions) \
            if np.random.uniform(0, 1) < self.exp_rate \
            else self._find_best_action(actions, state_hash_function)
        self.states_history.append(state_hash_function(action))
        return action

    def end_iteration(self, reward: float):
        """
        Update the states of the agent according to
            Q(state, action) ← (1−α) Q(state, action) + α(reward + γmax Q(next state, all actions))
        :param reward: the reward for this iteration
        """
        for state in reversed(self.states_history):
            self.states[state] += self.lr * (self.decay_gamma * reward - self.states[state])
            reward = self.states[state]
        self.states_history.clear()

    def _find_best_action(self, actions, state_hash_function):
        value_max = float('-inf')
        action = None
        for a in actions:
            # If we don't know that state, we rate it low
            v = self.states.get(state_hash_function(a), 0)
            if v > value_max:
                value_max = v
                action = a
        return action or self._get_random_action(actions)

    @staticmethod
    def _get_random_action(actions):
        return actions[np.random.choice(len(actions))]
