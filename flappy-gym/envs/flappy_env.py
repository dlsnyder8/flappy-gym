import gym
from gym import error, spaces, utils
from gym.utils import seeding
import numpy as np
import random
import pygame
import time
class FlappyEnv(gym.Env):

    metadata = {'render.modes': ['human']}

    def __init__(self):
        self.display_width = 288
        self.display_height = 512
        pygame.init()
        self.win = pygame.display.set_mode((self.display_width, self.display_height))
        pygame.display.set_caption("Flappy Bird")
        self.font = pygame.font.Font("score_font.ttf", 50)

        # game images and sounds
        self.bg = pygame.image.load('bg copy.png').convert()
        self.char = pygame.image.load('flappy copy.png').convert()
        self.ground = pygame.image.load('ground copy.png')
        self.bottom_pipe = pygame.image.load('pipemain2 copy 2.png').convert()
        self.top_pipe = pygame.transform.rotate(bottom_pipe, 180)
        self.flap_sound = pygame.mixer.Sound('Flapsound copy.wav')
        self.point_sound = pygame.mixer.Sound('point copy.wav')
        self.hit_sound = pygame.mixer.Sound('hit copy.wav')

        clock = pygame.time.Clock()
        self.pipe_width = self.bottom_pipe.get_rect().width
        self.pipe_height = self.bottom_pipe.get_rect().height()
        self.char_width = self.char.get_rect().width
        self.char_height = char.get_rect().height
        self.pipe_separation = 140
        self.score = 0

        # actions and observation space (not 100% sure what these are for yet)
        self.action_space = spaces.Discrete(2)
        self.observation_space = spaces.Box(low=0, high=255, shape=(self.display_height, self.display_width, 3), dtype=np.uint8)

    # Bird Class
    class Bird(object):

        def __init__(self, x, y):
            self.x = x
            self.y = y
            self.hitbox = (self.x, self.y, self.char_width, self.char_height)

    # Pipe Class
    class Pipe(object):
        def __init__(self, x):
            self.x = x
            self.bottom_disp = random.randint(0, 110)
            self.top_of_bottom = self.display_height - self.pipe_height + 70 - self.bottom_disp
            self.hitboxbot = (self.x, self.top_of_bottom, self.pipe_width, self.pipe_height)
            self.hitboxtop = (self.x, 0, self.pipe_width, self.top_of_bottom - self.pipe_separation - self.pipe_height)

        # draws two pipe in the same y-plane
        def draw(self, win):
            win.blit(self.bottom_pipe, (self.x, self.top_of_bottom))
            win.blit(self.top_pipe, (self.x, self.top_of_bottom - self.pipe_separation - self.pipe_height))
            self.x -= 2
            self.hitboxbot = (self.x, self.top_of_bottom, self.pipe_width, self.pipe_height)
            self.hitboxtop = (self.x, 0, self.pipe_width, self.top_of_bottom - self.pipe_separation - self.pipe_height)


    def _step(self, action):
        """

        Parameters
        ----------
        action :

        Returns
        -------
        ob, reward, episode_over, info : tuple
            ob (object) :
                an environment-specific object representing your observation of
                the environment.
            reward (float) :
                amount of reward achieved by the previous action. The scale
                varies between environments, but the goal is always to increase
                your total reward.
            episode_over (bool) :
                whether it's time to reset the environment again. Most (but not
                all) tasks are divided up into well-defined episodes, and done
                being True indicates the episode has terminated. (For example,
                perhaps the pole tipped too far, or you lost your last life.)
            info (dict) :
                 diagnostic information useful for debugging. It can sometimes
                 be useful for learning (for example, it might contain the raw
                 probabilities behind the environment's last state change).
                 However, official evaluations of your agent are not allowed to
                 use this for learning.
        """
        self._take_action(action)
        self.status = self.env.step()
        reward = self._get_reward()
        ob = self.env.getState()
        episode_over = self.status != hfo_py.IN_GAME
        return ob, reward, episode_over, {}

    def _reset(self):
        pass

    def _render(self, mode='human', close=False):
        pass

    def _take_action(self, action):
        pass

    def _get_reward(self):
        """ Reward is given for XY. """
        if self.status == FOOBAR:
            return 1
        elif self.status == ABC:
            return self.somestate ** 2
        else:
            return 0
