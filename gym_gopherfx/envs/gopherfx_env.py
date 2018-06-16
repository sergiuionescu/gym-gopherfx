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
    multiplier = 100
    action_investment = 1

    def __init__(self):
        self.observation_space = Box(low=0, high=1000, shape=(1,))
        self.action_space = Discrete(3)
        self.open_contracts = {'buy': [], 'sell': []}
        self.investment = 0
        self.investment_observation = None
        self.invested_at = 0
        self.elapsed = 0
        self.budget = 100
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
            contract = {'investment': self.action_investment * self.multiplier,
                        'observation': observation,
                        'invested_at': self.elapsed}

            action_code = 'buy'
            complementary_action_code = 'sell'
            reward = self.execute_contract(action_code, complementary_action_code, contract)

        elif action == 2:
            contract = {'investment': self.action_investment * self.multiplier,
                        'observation': observation,
                        'invested_at': self.elapsed}
            action_code = 'sell'
            complementary_action_code = 'buy'
            reward = self.execute_contract(action_code, complementary_action_code, contract)

        done = 0
        if self.elapsed >= self.episode_length - 1:
            done = 1
            self.elapsed = 0
        elif self.budget <= 0:
            done = 1
            reward = -1

        self.last_reward = reward
        self.elapsed += 1

        return observation, reward, done, {}

    def execute_contract(self, action_code, complementary_action_code, contract):
        reward = 0
        reward_modifier = 1
        if action_code == 'buy':
            reward_modifier = -1
        if len(self.open_contracts[complementary_action_code]):
            start_contract = self.open_contracts[complementary_action_code].pop(0)
            reward = reward_modifier * (contract['investment'] * (contract['observation'][1] + self.spread) -
                                        start_contract['investment'] *
                                        start_contract['observation'][1])
            self.budget += reward
            self.sell_info = tuple(
                [start_contract['observation'][0], contract['observation'][0], reward,
                 start_contract['observation'][1],
                 contract['observation'][1], self.elapsed - start_contract['invested_at'], action_code, self.budget])
        else:
            self.open_contracts[action_code].append(contract)
        return reward

    def get_observation(self):
        observation = tuple([self.data['date'][self.elapsed], self.data['rate'][self.elapsed]])
        return observation

    def reset(self):
        self.open_contracts = {'buy': [], 'sell': []}
        self.investment = 0
        self.budget = 100
        self.invested_at = 0
        self.investment_observation = None

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