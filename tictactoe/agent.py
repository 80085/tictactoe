import collections

import numpy as np


class QLearningAgent:
    def __init__(self, policy=None, exp_rate=0.3, learning_rate=0.2, decay_gamma=0.9):
        self._exp_rate = exp_rate
        self._decay_gamma = decay_gamma
        self._learning_rate = learning_rate
        self._states_history = []
        self.states = collections.defaultdict(float, policy or {})

    def choose_action(self, actions: list, state_hash_function):
        """
        Let the agent choose one action based on its policy and setup
        :param actions: a list of possible actions
        :param state_hash_function: a function to generate the hash of new state, for a given action
        :return: the agents action
        """
        action = self._get_random_action(actions) \
            if np.random.uniform(0, 1) < self._exp_rate \
            else self._find_best_action(actions, state_hash_function)
        self._states_history.append(state_hash_function(action))
        return action

    def end_iteration(self, reward: float):
        """
        Update the states of the agent according to
            Q(state, action) ← (1−α) Q(state, action) + α(reward + γmax Q(next state, all actions))
        :param reward: the reward for this iteration
        """
        for state in reversed(self._states_history):
            self.states[state] += self._learning_rate * (self._decay_gamma * reward - self.states[state])
            reward = self.states[state]
        self._states_history.clear()

    def _find_best_action(self, actions, state_hash_function):
        value_max = float('-inf')
        action = None
        for a in actions:
            h = state_hash_function(a)
            if h in self.states and self.states[h] > value_max:
                value_max = self.states[h]
                action = a
        return action or self._get_random_action(actions)

    @staticmethod
    def _get_random_action(actions):
        return actions[np.random.choice(len(actions))]
