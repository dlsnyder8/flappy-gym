from gym.envs.registration import register

register(
    id='flappygym-v0',
    entry_point='flappy_gym.envs:FlappyEnv',
)

