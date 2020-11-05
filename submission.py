DEF_ENUM = {
    'rock': 0,
    'paper': 1,
    'scissors': 2
}

import random

def nash_equilibrium_agent(observation, configuration):
    return random.randint(0, 2)


# def nash_equilibrium_agent(observation, configuration):
#     return random.randint(0, 2)


# def copy_opponent_agent(observation, configuration):
#     if observation.step > 0:
#         return observation.lastOpponentAction
#     else:
#         return 0
