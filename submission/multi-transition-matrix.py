import numpy as np
import pandas as pd
import random

## -------------------------------------------------------------------------
class dTransitionMatrix:
    # transition matrix
    T = None
    # a1 is the action of the opponent 1 step ago
    # a2 is the action of the opponent 2 steps ago
    a1 = None
    a2 = None

    def __init__(self):
        self.T = np.zeros((3, 3))
        self.a1, self.a2 = None, None

    def run(self, observation, configuration):
        if observation.step > 1:
            self.a1 = observation.lastOpponentAction
            self.T[self.a2, self.a1] += 1
            P = np.divide(self.T, np.maximum(1, self.T.sum(axis=1)).reshape(-1, 1))
            self.a2 = self.a1
            if np.sum(P[self.a1, :]) == 1:
                return int((np.random.choice([0, 1, 2], p=P[self.a1, :]) + 1) % 3)
            else:
                return int(np.random.randint(3))
        else:
            if observation.step == 1:
                self.a2 = observation.lastOpponentAction
            return int(np.random.randint(3))

## -------------------------------------------------------------------------
class ndTransitionMatrix:

    T = None
    # transaction choice
    t = None

    def __init__(self):
        self.T = np.zeros((3, 3, 3))
        self.t = [None, None, None]

    def run(self, observation, configuration):
        if observation.step > 2:
            self.t[2] = observation.lastOpponentAction
            self.T[self.t[0], self.t[1], self.t[2]] += 1
            T0 = self.T[self.t[0]]
            P = np.divide(T0, np.maximum(1, T0.sum(axis=1)).reshape(-1, 1))
            self.t[0], self.t[1] = self.t[1], self.t[2]
            if np.sum(P[self.t[2], :]) == 1:
                return int((np.random.choice([0, 1, 2], p=P[self.t[2], :]) + 1) % 3)
            else:
                return int(np.random.randint(3))
        else:
            # first play
            if observation.step == 1:
                self.t[0] = observation.lastOpponentAction
            # second play
            elif observation.step == 2:
                self.t[1] = observation.lastOpponentAction
            # random choice
            return int(np.random.randint(3))

## -------------------------------------------------------------------------
class dCounterTransitionMatrix:

    T = None
    # a1 is the action of the opponent 1 step ago
    # b1 is my action 1 step ago
    # b2 is my action 2 steps ago
    a1 = None
    b1 = None
    b2 = None

    def __init__(self):
        self.T = np.zeros((3, 3))
        self.a1, self.b1, self.b2 = None, None, None

    def run(self, observation, configuration):
        if observation.step > 2:
            self.a1 = observation.lastOpponentAction
            self.T[self.b2, self.a1] += 1
            P = np.divide(self.T, np.maximum(1, self.T.sum(axis=1)).reshape(-1, 1))
            self.b2 = self.b1
            if np.sum(P[self.b1, :]) == 1:
                self.b1 = int((np.random.choice([0, 1, 2], p=P[self.b1, :]) + 1) % 3)
                return self.b1
            else:
                return int(np.random.randint(3))
        else:
            self.b2 = self.b1
            self.b1 = int(np.random.randint(3))
            return self.b1

## -------------------------------------------------------------------------
class multiAgent:
    
    agents = None
    score = None
    lastAction = None

    def __init__(self, agents):
        self.agents = agents
        self.score      = np.zeros(len(agents))
        self.lastAction = np.zeros(len(agents))

    def checkResult(self, lastOpponentAction):
        for key in range(len(self.agents)):
            myLast = self.lastAction[key]
            if (lastOpponentAction + 1) % 3 == myLast:
                self.score[key] += 1

    def run(self, observation, configuration):
        # calculate actions
        for key, agent in enumerate(self.agents):
            self.lastAction[key] = agent.run(observation, configuration)
        # check action step
        if observation.step > 1:
            # validate results
            self.checkResult(observation.lastOpponentAction)
            # calculate probabilities
            if sum(multi.score) > 1:
                P = np.divide(multi.score, sum(multi.score))
                if sum(P) == 1.0:
                    keys = [key for key in range(len(self.agents))]
                    better = np.random.choice(keys, p=P)
                    return int(self.lastAction[better])
            # random action
            return int(np.random.randint(3))
        else:
            # random action
            return int(self.lastAction[0])

## -------------------------------------------------------------------------
agents = [
    dTransitionMatrix(),
    ndTransitionMatrix(),
    dCounterTransitionMatrix()
]
multi = multiAgent(agents)

def agent(observation, configuration):
    global multi
    return multi.run(observation, configuration)
