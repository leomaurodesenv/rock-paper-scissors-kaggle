import numpy as np
import pandas as pd
import random

import collections
from kaggle_environments.envs.rps.utils import get_score

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
class Markov:

    table = None
    action_seq = None

    def __init__(self):
        self.action_seq = []
        self.table = collections.defaultdict(lambda: [1, 1, 1])

    def run(self, observation, configuration):
        k = 2
        if observation.step % 250 == 0: # refresh table every 250 steps
            self.action_seq, self.table = [], collections.defaultdict(lambda: [1, 1, 1])
        if len(self.action_seq) <= 2 * k + 1:
            action = int(np.random.randint(3))
            if observation.step > 0:
                self.action_seq.extend([observation.lastOpponentAction, action])
            else:
                self.action_seq.append(action)
            return action
        # update table
        key = ''.join([str(a) for a in self.action_seq[:-1]])
        self.table[key][observation.lastOpponentAction] += 1
        # update action seq
        self.action_seq[:-2] = self.action_seq[2:]
        self.action_seq[-2] = observation.lastOpponentAction
        # predict opponent next move
        key = ''.join([str(a) for a in self.action_seq[:-1]])
        if observation.step < 500:
            next_opponent_action_pred = np.argmax(self.table[key])
        else:
            # add stochasticity for second part of the game
            scores = np.array(self.table[key])
            next_opponent_action_pred = np.random.choice(3, p=scores/scores.sum()) 
        # make an action
        action = (next_opponent_action_pred + 1) % 3
        # if high probability to lose -> let's surprise our opponent with sudden change of our strategy
        if observation.step > 900:
            action = next_opponent_action_pred
        self.action_seq[-1] = action
        return int(action)

## -------------------------------------------------------------------------
class MemoryPatterns:
    # how many steps in a row are in the pattern (multiplied by two)
    memory_length = None
    # current memory of the agent
    current_memory = None
    # list of memory patterns
    memory_patterns = None

    def __init__(self):
        self.memory_length = 6
        self.current_memory = []
        self.memory_patterns = []


    def find_pattern(self, memory):
        """ find appropriate pattern in memory """
        for pattern in self.memory_patterns:
            actions_matched = 0
            for i in range(self.memory_length):
                if pattern["actions"][i] == memory[i]:
                    actions_matched += 1
                else:
                    break
            # if memory fits this pattern
            if actions_matched == self.memory_length:
                return pattern
        # appropriate pattern not found
        return None

    def run(self, obs, conf):
        """ your ad here """
        # if it's not first step, add opponent's last action to agent's current memory
        if obs.step > 0:
            self.current_memory.append(obs.lastOpponentAction)
        # if length of current memory is bigger than necessary for a new memory pattern
        if len(self.current_memory) > self.memory_length:
            # get momory of the previous step
            previous_step_memory = self.current_memory[:self.memory_length]
            previous_pattern = self.find_pattern(previous_step_memory)
            if previous_pattern == None:
                previous_pattern = {
                    "actions": previous_step_memory.copy(),
                    "opp_next_actions": [
                        {"action": 0, "amount": 0, "response": 1},
                        {"action": 1, "amount": 0, "response": 2},
                        {"action": 2, "amount": 0, "response": 0}
                    ]
                }
                self.memory_patterns.append(previous_pattern)
            for action in previous_pattern["opp_next_actions"]:
                if action["action"] == obs.lastOpponentAction:
                    action["amount"] += 1
            # delete first two elements in current memory (actions of the oldest step in current memory)
            del self.current_memory[:2]
        my_action = random.randint(0, 2)
        pattern = self.find_pattern(self.current_memory)
        if pattern != None:
            my_action_amount = 0
            for action in pattern["opp_next_actions"]:
                # if this opponent's action occurred more times than currently chosen action
                # or, if it occured the same amount of times, choose action randomly among them
                if (action["amount"] > my_action_amount or
                        (action["amount"] == my_action_amount and random.random() > 0.5)):
                    my_action_amount = action["amount"]
                    my_action = action["response"]
        self.current_memory.append(my_action)
        return int(my_action)

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
                key, maxP = 0, -1
                for i, p in enumerate(P):
                    if maxP < p:
                        key, maxP = i, p
                return int(self.lastAction[key])
            # random action
            return int(np.random.randint(3))
        else:
            # random action
            return int(self.lastAction[0])

## -------------------------------------------------------------------------
agents = [
    dTransitionMatrix(),
    ndTransitionMatrix(),
    dCounterTransitionMatrix(),
    Markov(),
    MemoryPatterns()
]
multi = multiAgent(agents)

def agent(observation, configuration):
    global multi
    return multi.run(observation, configuration)
