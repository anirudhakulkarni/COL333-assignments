# MDP model for taxi agent problem
'''The taxi agent interacts in the environment in episodes. In each episode, the taxi starts in a randomly chosen grid cell. There is a passenger at one of the four depot locations chosen randomly and that passenger wishes to be transported to one of the other depot locations. The destination is different from the source and also selected randomly. The taxi must move towards the passenger’s grid cell (called the source), pick up the passenger, go to the destination location (called the destination), and drop the passenger there. The episode ends when the passenger is deposited at the destination location.'''
import numpy as np


class TaxiAgent:
    def __init__(self, env, agent_id):
        self.env = env
        self.agent_id = agent_id
        self.state = None
        self.action = None
        self.reward = 0
        self.next_state = None
        self.next_action = None
        self.next_reward = 0
        self.terminal = False
        self.action_space = env.action_space
        self.state_space = env.state_space
        self.state_space_size = len(self.state_space)
        self.action_space_size = len(self.action_space)
        self.Q = np.zeros((self.state_space_size, self.action_space_size))
        self.Q_table = np.zeros(
            (self.state_space_size, self.action_space_size))

    def reset(self):
        self.state = self.env.reset()
        self.action = None
        self.reward = 0
        self.next_state = None
        self.next_action = None
        self.next_reward = 0
        self.terminal = False

    def step(self, action):
        self.next_state, self.next_reward, self.terminal, _ = self.env.step(
            action)
        self.next_action = self.get_action(self.next_state)
        self.next_reward = self.get_reward(self.next_state)
        self.state = self.next_state
        self.action = self.next_action
        self.reward = self.next_reward
        return self.next_state, self.next_reward, self.terminal, self.next_action

    def get_action(self, state):
        return self.action_space[np.argmax(self.Q[state])]

    def get_reward(self, state):
        return self.env.get_reward(state)

    def update_Q(self, state, action, reward, next_state, next_action, next_reward):
        self.Q[state, action] = self.Q[state, action] + self.alpha * \
            (reward + self.gamma *
             self.Q[next_state, next_action] - self.Q[state, action])
        self.Q_table[state, action] = self.Q_table[state, action] + self.alpha * \
            (reward + self.gamma *
             self.Q_table[next_state, next_action] - self.Q_table[state, action])
        self.Q_table_count[state,
                           action] = self.Q_table_count[state, action] + 1
        self.Q_table_count_sum[state,
                               action] = self.Q_table_count_sum[state, action] + 1
        self.Q_table_max[state, action] = max(
            self.Q_table_max[state, action], self.Q_table[state, action])
        self.Q_table_min[state, action] = min(
            self.Q_table_min[state, action], self.Q_table[state, action])
        self.Q_table_mean[state, action] = self.Q_table_mean[state, action] + (
            self.Q_table[state, action] - self.Q_table_mean[state, action]) / self.Q_table_count[state, action]
        self.Q_table_std[state, action] = self.Q_table_std[state, action] + (
            self.Q_table[state, action] - self.Q_table_mean[state, action]) * (self.Q_table[state, action] - self.Q_table_mean[state, action])
        self.Q_table_count_max[state, action] = max(
            self.Q_table_count_max[state, action], self.Q_table_count[state, action])
        self.Q_table_count_min[state, action] = min(
            self.Q_table_count_min[state, action], self.Q_table_count[state, action])

class TaxiEnv:
    def __init__(self):
        self.state_space = [0, 1, 2, 3]
        self.action_space = ["N", "S", "E", "W", "pickup", "putdown"]
        self.reward_matrix = np.array([[-1, -1, -1, -1],
                                       [1, -1, -1, -1],
                                       [-1, 1, -1, -1],
                                       [-1, -1, 1, -1],
                                       [-1, -1, -1, 1]])
        self.reward_matrix_count = np.zeros((4, 4))
        self.reward_matrix_count_sum = np.zeros((4, 4))
        self.reward_matrix_max = np.zeros((4, 4))
        self.reward_matrix_min = np.zeros((4, 4))
        self.reward_matrix_mean = np.zeros((4, 4))
        self.reward_matrix_std = np.zeros((4, 4))
        self.reward_matrix_count_max = np.zeros((4, 4))
        self.reward_matrix_count_min = np.zeros((4, 4))

    def reset(self):
        self.state = np.random.randint(0, 4)
        self.reward = 0
        self.terminal = False
        return self.state

    def step(self, action):
        self.next_state = np.random.randint(0, 4)
        self.reward = self.reward_matrix[self.state, action]
        self.terminal = False
        return self.next_state, self.reward, self.terminal, self.action_space[action]

    def get_reward(self, state):
        return self.reward_matrix[state, self.state]

    def update_reward_matrix(self, state, action, reward):
        self.reward_matrix[state, action] = reward
        self.reward_matrix_count[state, action] = self.reward_matrix_count[state, action] + 1
