## --- name to value
DEF_ENUM = {'rock': 0, 'paper': 1, 'scissors': 2}

## --- count number of actions
DEF_ACTIONS = [0, 1, 2] ## possabilities
DEF_OPPOSITE = {0: 1, 1: 2, 2: 0}
DEF_LAST_ACTIONS = [0, 0, 0]
DEF_THRESHOLD = 20 # max memory

import random
from numpy.random import choice


def roulette_agent(observation, configuration):
    global DEF_LAST_ACTIONS
    if observation.step > 0:
        # see the last action
        idx = observation.lastOpponentAction
        # increment number of plays
        DEF_LAST_ACTIONS[idx] += 1
        ## -- compute probability
        tmpMax = max(DEF_LAST_ACTIONS)
        tmpProb = [(tmpMax-i) for i in DEF_LAST_ACTIONS]
        # clean memory
        if tmpMax > DEF_THRESHOLD:
            DEF_LAST_ACTIONS = [0, 0, 0]
        tmpSum = sum(tmpProb)
        if tmpSum == 0:
            # same probability
            return random.randint(0, 2)
        else:
            # else, compute probability
            tmpProb = [round(float(i/tmpSum), 6) for i in tmpProb]
            # guess the next action
            actionGuess = choice(DEF_ACTIONS, 1, p=tmpProb)[0]
            # return a nice move based on the guessing
            return DEF_OPPOSITE[actionGuess]
    else:
        # first move - random
        return random.randint(0, 2)
