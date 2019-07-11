from gym.envs.registration import register

register(
    id='flappy_gym',
    entry_point='flappy_gym.envs:FlappyEnv',
)

