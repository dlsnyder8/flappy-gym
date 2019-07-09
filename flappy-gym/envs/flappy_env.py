import gym
from gym import error, spaces, utils
from gym.utils import seeding
import numpy as np
import random
import pygame
import time

pygame.init()
# variables for display
display_width = 288
display_height = 512
font = pygame.font.Font("score_font.ttf", 50)

# images and sounds
bg = pygame.image.load('bg copy.png').convert()
char = pygame.image.load('flappy copy.png').convert()
ground = pygame.image.load('ground copy.png')
bottom_pipe = pygame.image.load('pipemain2 copy 2.png').convert()
top_pipe = pygame.transform.rotate(bottom_pipe, 180)
flap_sound = pygame.mixer.Sound('Flapsound copy.wav')
point_sound = pygame.mixer.Sound('point copy.wav')
hit_sound = pygame.mixer.Sound('hit copy.wav')
clock = pygame.time.Clock()
# other variables
pipe_width = bottom_pipe.get_rect().width
pipe_height = bottom_pipe.get_rect().height()
ground_height = ground.get_rect().height
ground_width = ground.get_rect().width
char_width = char.get_rect().width
char_height = char.get_rect().height
bg_width = bg.get_rect().width
pipe_separation = 140
airtime = 4
score = 0
x = 100  # unchanged
y = 300
flap = 0
# run = True
is_flap = False  # true when bird flaps
background_position = 0


point_received_1 = False
point_received_2 = False
is_hit = True


class Bird(object):
    def __init__(self, x_pos, y_pos):
        self.x = x_pos
        self.y = y_pos
        self.hitbox = (self.x, self.y, self.char_width, self.char_height)

    def dist_from_pipe(self):
        pipe_one, pipe_two = FlappyEnv.pipe_return()
        if point_received_2:
            return pipe_one.x - self.x
        elif point_received_1:
            return pipe_two.x - self.x


# Pipe Class
class Pipe(object):
    def __init__(self, x_pos):
        self.x = x_pos
        self.bottom_disp = random.randint(0, 110)
        self.top_of_bottom = display_height - pipe_height + 70 - self.bottom_disp
        self.hitboxbot = (self.x, self.top_of_bottom, pipe_width, pipe_height)
        self.hitboxtop = (self.x, 0, pipe_width, self.top_of_bottom - pipe_separation - pipe_height)

    # draws two pipes in the same y-plane
    def draw(self, win):
        win.blit(bottom_pipe, (self.x, self.top_of_bottom))
        win.blit(top_pipe, (self.x, self.top_of_bottom - pipe_separation - pipe_height))
        self.x -= 2
        self.hitboxbot = (self.x, self.top_of_bottom, pipe_width, pipe_height)
        self.hitboxtop = (self.x, 0, pipe_width, self.top_of_bottom - pipe_separation - pipe_height)

pipe = Pipe(display_width)
pipe2 = Pipe(display_width + 169)
birdbox = Bird(x, y)


class FlappyEnv(gym.Env):

    def __init__(self):

        # GLOBALIZED VARIABLE(S):
        global score

        score = 0
        self.win = pygame.display.set_mode((display_width, display_height))
        pygame.display.set_caption("Flappy Bird")

        # actions and observation space
        self.action_space = spaces.Discrete(2)
        self.observation_space = spaces.Box(low=0, high=255, shape=(display_height, display_width, 3), dtype=np.uint8)

    metadata = {'render.modes': ['human']}
    screenshot_image_data = ""

    def _step(self, action):

        # GLOBALIZED VARIABLE(S):
        global background_position, char, birdbox, pipe, pipe2, is_flap, flap, y, point_received_1, point_received_2, screenshot_image_data, score

        pygame.event.pump()
        reward = 0.25  # standard reward given for every step
        terminal = False

        # '0' AS AN ACTION MEANS DO NOTHING
        # '1' AS AN ACTION MEANS FOR THE BIRD TO FLAP

        relative_x = background_position % bg_width

        # checks for collision
        is_crash = ((pipe.x + pipe_width >= birdbox.x >= pipe.x - 28) and
                   ((birdbox.y + char_height > pipe.top_of_bottom) or
                    (birdbox.y < pipe.top_of_bottom - pipe_separation))) or (
                              (pipe2.x + pipe_width >= birdbox.x >= pipe2.x - 28)
                              and ((birdbox.y + char_height > pipe2.top_of_bottom)
                                   or (birdbox.y < pipe2.top_of_bottom - pipe_separation))) or (
                              y + char_height) > (display_height - ground_height + 10)

        if not is_crash:

            if not is_flap:

                if action == 1:
                    flap_sound.play()
                    y -= (airtime ** 2)
                    is_flap = True
                    flap += 1
                    char = pygame.transform.rotate(pygame.image.load('upflap.png'), 20)

            else:
                if flap < 8:
                    y -= (airtime ** 2)
                    flap += 1
                    char = pygame.transform.rotate(pygame.image.load('midflap.png'), 15)

                elif 7 < flap < 13:
                    flap += 1
                    char = pygame.transform.rotate(pygame.image.load('midflap.png'), -15)

                elif flap == 13:
                    is_flap = False
                    flap = 0
                    char = pygame.transform.rotate(pygame.image.load('flappy.png'), -40)

            y -= (airtime ** 2) * -0.4

            # scrolling background
            relative_x = background_position % bg_width
            self.win.blit(bg, (relative_x - bg_width, 0))
            background_position -= 2

            if relative_x < display_width:
                relative_x = background_position % bg_width
                self.win.blit(bg, (relative_x, 0))

            # pipe spawning & score updating
            pipe.draw(self.win)
            pipe2.draw(self.win)
            if 98 <= pipe.x + pipe_width <= x and point_received_1 == False:
                # point_sound.play()
                point_received_1 = True
                score += 1
                reward = 1      # reward for passing a pipe
            if 98 < pipe2.x + pipe_width <= x and point_received_2 == False:
                # point_sound.play()
                point_received_2 = True
                score += 1
                reward = 1      # reward for passing a pipe
            if pipe.x < 0 - pipe_width:
                pipe = Pipe(288)
                point_received_1 = False
            if pipe2.x < 0 - pipe_width:
                pipe2 = Pipe(288)
                point_received_2 = False

            # scrolling ground
            self.win.blit(ground, (relative_x - ground_width, display_height - ground_height))
            if relative_x < display_width:
                self.win.blit(ground, (relative_x, display_height - ground_height))

            #display_score(score)
            self.win.blit(char, (x, y))
            birdbox = bird(x, y)

        else:
            terminal = True
            # y -= (AIRTIME ** 2) * -0.4  # falling after crash
            self.__init__()
            reward = -1  # negative rewards for crashing

            # makes sure the hit sound doesn't keep playing
            # if is_hit:
            #     hit_sound.play()
            #     self.is_hit = False
            # if (y + char_height) > (display_height - ground_height + 10):  # when it hit the ground, crash fxn will be called
            #     crash()

            self.win.blit(bg, (relative_x - bg_width, 0))

            if relative_x < display_width:
                self.win.blit(bg, (relative_x, 0))

            self.win.blit(bottom_pipe, (pipe.x + 2, pipe.top_of_bottom))
            self.win.blit(top_pipe, (pipe.x + 2, pipe.top_of_bottom - pipe_separation - pipe_height))
            self.win.blit(bottom_pipe, (pipe2.x + 2, pipe2.top_of_bottom))
            self.win.blit(top_pipe, (pipe2.x + 2, pipe2.top_of_bottom - pipe_separation - pipe_height))
            self.win.blit(ground, (0, display_height - ground_height))
            self.win.blit(char, (x, y))
            self.win.blit(ground, (0, display_height - ground_height))

        screenshot_image_data = pygame.surfarray.array3d(pygame.display.get_surface())
        return screenshot_image_data, reward, terminal, {}
        # display_score(score)

    @staticmethod
    def pipe_return():

        # GLOBALIZED VARIABLE(S):
        global pipe, pipe2

        return pipe, pipe2

    @staticmethod
    def _reset():

        # GLOBALIZED VARIABLE(S):
        global score, x, y, flap, is_flap, background_position, pipe, pipe2, birdbox, point_received_1, point_received_2, is_hit, screenshot_image_data

        score = 0
        x = 100  # unchanged
        y = 300
        flap = 0
        # run = True
        is_flap = False  # true when bird flaps

        background_position = 0
        pipe = Pipe(display_width)
        pipe2 = Pipe(display_width + 169)
        birdbox = bird(x, y)

        point_received_1 = False
        point_received_2 = False
        is_hit = True

        screenshot_image_data,_,_,_ = step(0)
        return screenshot_image_data

    @staticmethod
    def _render(self, mode='human', close=False):
        pygame.display.update()
        clock.tick(30)
