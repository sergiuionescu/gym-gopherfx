from gym.envs.registration import register

register(
    id='Gopherfx-v0',
    entry_point='gym_gopherfx.envs:GopherfxEnv',
)