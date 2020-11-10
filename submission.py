DEF_ENUM = {
    'rock': 0,
    'paper': 1,
    'scissors': 2
}

DEF_GUESS = {
    0: 2, # pedra -> tesoura
    1: 0, # papel -> pedra
    2: 1  # tesoura -> papel
}

import random

def nice_guess_agent(observation, configuration):
    print(observation)
    if observation.step > 0:
        return DEF_GUESS[observation.lastOpponentAction]
    else:
        return random.randint(0, 2)
