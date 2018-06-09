import gym
from gym.spaces import Discrete, Box
import pandas as pd
import os
from gym import error, spaces, utils
from gym.utils import seeding


class GopherfxEnv(gym.Env):
    metadata = {'render.modes': ['human']}
    rates_file = "data/rates/USDJPY20180401.csv"
    spread = 0.015

    def __init__(self):
        self.observation_space = Box(low=0, high=1000, shape=(1,))
        self.action_space = Discrete(3)
        self.investment = 0
        self.investment_observation = None
        self.invested_at = 0
        self.elapsed = 0
        self.sell_info = None

        self.last_action = None
        self.last_reward = None

        self.data = pd.read_csv(os.path.join(os.path.dirname(__file__), self.rates_file), names=['date', 'rate'])
        self.episode_length, columns = self.data.shape

    def step(self, action):
        self.last_action = action
        self.sell_info = {}

        observation = self.get_observation()

        reward = 0
        if action == 0:
            pass
        elif action == 1:
            if self.investment == 0:
                self.investment = 100
                self.investment_observation = observation
                self.invested_at = self.elapsed
            else:
                reward = -1
        elif action == 2:
            if self.investment > 0:
                reward = self.investment * (observation[1] + self.spread) - self.investment * \
                         self.investment_observation[1]
                self.sell_info = tuple(
                    [self.investment_observation[0], observation[0], reward, self.investment_observation[1],
                     observation[1], self.elapsed - self.invested_at])
                self.investment = 0
                self.investment_observation = None
            else:
                reward = -1

        done = 0
        if self.elapsed >= self.episode_length - 1:
            done = 1
            self.elapsed = 0

        self.last_reward = reward
        self.elapsed += 1

        return observation, reward, done, {}

    def get_observation(self):
        observation = tuple([self.data['date'][self.elapsed], self.data['rate'][self.elapsed]])
        return observation

    def reset(self):
        self.investment = 0

    def render(self, mode='human', close=False):
        # output = "Action " + str(self.last_action) + ", reward " + str(self.last_reward) + " observation %s" % (
        #     self.get_observation(),)
        output = ""
        if self.sell_info:
            output = self.sell_info

        return output

    def _seed(self, seed=None):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]
