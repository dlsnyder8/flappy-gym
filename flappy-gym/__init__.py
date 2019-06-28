from gym.envs.registration import register

register(
    id='flappy-gym',
    entry_point='flappy-gym.envs:FlappyEnv',
)

