import argparse
import os, csv

import gym
import numpy as np
import time
import gym_gopherfx

class RandomAgent(object):
    performance_file = "performance/USDJPY20180401.csv"

    def __init__(self, action_space):
        self.action_space = action_space

    def act(self, observation, reward, done):
        return np.random.randint(self.action_space.n)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=None)
    parser.add_argument('env_id', nargs='?', default='Gopherfx-v0', help='Select the environment to run')
    args = parser.parse_args()

    env = gym.make(args.env_id)
    env.seed(1)
    agent = RandomAgent(env.action_space)

    reward = 0
    done = False
    while True:
        ob = env.reset()
        with open(os.path.join(os.path.dirname(__file__), agent.performance_file), 'w') as pf:
            file_writer = csv.writer(pf)
            while True:
                action = agent.act(ob, reward, done)
                ob, reward, done, _ = env.step(action)

                if done:
                    break
                output = env.render()
                if output:
                    print(output)
                    file_writer.writerow(output)
        time.sleep(5)