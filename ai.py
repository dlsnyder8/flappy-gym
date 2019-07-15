import gym
from gym import error, spaces, utils
from gym.utils import seeding
import random
import numpy as np
from random import shuffle
from flappy_gym.envs.flappy_env import FlappyEnv
from flappy_gym import envs

env = gym.make('flappygym-v0')
env.reset()


LEARNINGRATE = 0.1
DISCOUNT = 0.95
EPISODES = 2500
actions = 2

DISCRETE_OS_SIZE = [20, 20]
qtable = np.random.uniform(low=-2, high=0, size=(288, 512, 2))  # 285 is highest the pipe can be


# def get_discrete_state(state):
#     # discretestate = (state)/ discrete_os_win_size
#     return qtable[state]


for i in range(EPISODES):
    action = np.random.randint(0, 2)
    # np.argmax(qtable[:,discretestate])
    # env.action_space.sample()
    new_state, reward, done, _ = env.step(action)
    env.render()










    # new_discrete_state = get_discrete_state(new_state)
    # if not done:
    #     max_future_q = np.max(qtable[:,new_discrete_state])
    #     currentq = qtable[:,(discretestate+(action,))]
    #
    #     new_q = (1-LEARNINGRATE)*currentq+LEARNINGRATE*(reward+DISCOUNT*max_future_q)
    #     qtable[:,(discretestate+ (action,))] = new_q
    #
    # elif new_state[0] >= env.goal_position:
    #     qtable[:,(discretestate+(action,))] = 0
    #
    # discretestate = new_discrete_state

env.close()




