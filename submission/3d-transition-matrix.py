import numpy as np
import pandas as pd
import random

opt = 3
T = np.zeros((opt, opt, opt))
P = np.zeros((opt, opt, opt))

# transaction choice
t = [None, None, None]

def agent(observation, configuration):
    global T, P, t, opt
    if observation.step > 2:
        t[2] = observation.lastOpponentAction
        T[t[0], t[1], t[2]] += 1
        T0 = T[t[0]]
        P = np.divide(T0, np.maximum(1, T0.sum(axis=1)).reshape(-1, 1))
        t[0], t[1] = t[1], t[2]
        if np.sum(P[t[2], :]) == 1:
            return int((np.random.choice([0, 1, 2], p=P[t[2], :]) + 1) % opt)
        else:
            return int(np.random.randint(opt))
    else:
        # first play
        if observation.step == 1:
            t[0] = observation.lastOpponentAction
        # second play
        elif observation.step == 2:
            t[1] = observation.lastOpponentAction
        # random choice
        return int(np.random.randint(opt))
