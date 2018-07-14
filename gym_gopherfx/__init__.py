from gym.envs.registration import register

register(
    id='Gopherfx-v0',
    entry_point='gym_gopherfx.envs:GopherfxV0Env',
)
register(
    id='Gopherfx-v1',
    entry_point='gym_gopherfx.envs:GopherfxV1Env',
)