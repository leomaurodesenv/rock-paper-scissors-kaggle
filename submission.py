DEF_ENUM = {'rock': 0, 'paper': 1, 'scissors': 2}
DEF_ACTIONS = [0, 1, 2]
DEF_OPPOSITE = {0: 1, 1: 2, 2: 0}

import random

def guessing_agent(observation, configuration):
    print(observation)
    if observation.step > 0:
        lastObs = observation.lastOpponentAction
        tmp = DEF_ACTIONS[:]
        tmp.remove(lastObs)
        return random.choice(tmp)
    else:
        return random.randint(0, 2)
