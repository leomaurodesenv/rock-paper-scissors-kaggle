import numpy as np
import pandas as pd
import random

T = np.zeros((3, 3, 3))

# a1 is the action of the opponent 1 step ago
# a1 is the action of the opponent 2 step ago
# b1 is my action 1 step ago
# b2 is my action 2 steps ago
a1, a2, b1, b2 = None, None, None, None

def agent(observation, configuration):
    global T, a1, a2, b2, b1
    if observation.step > 2:
        # last play
        a1 = observation.lastOpponentAction
        # increment
        T[a2, b2, a1] += 1
        # matrix, based on his a2 action
        Tb = T[a2]
        P = np.divide(Tb, np.maximum(1, Tb.sum(axis=1)).reshape(-1, 1))
        # update b2 and a2
        b2, a2 = b1, a1
        if np.sum(P[b1, :]) == 1:
            b1 = int((np.random.choice([0, 1, 2], p=P[b1, :]) + 1) % 3)
            return b1
        else:
            return int(np.random.randint(3))
    else:
        b2 = b1
        a2 = observation.lastOpponentAction if observation.step > 1 else None
        b1 = int(np.random.randint(3))
        return b1
