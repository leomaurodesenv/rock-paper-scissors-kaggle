# Rock, Paper, Scissors - Kaggle

Welcome to the [Rock, Paper, Scissors simulation competition](https://www.kaggle.com/c/rock-paper-scissors/)! (Or is it Paper, Scissors, Rock?)

How can such a simple game with three possible outcomes be anything other than random chance? Well, it's time to determine if artificial intelligence can learn game theory…

**Playground Simulation Competition** - In this repository, we present the set of strategies to "solve" this problem.  

**Disclaimer** - It is just a serie of attempts and theories.  

---
## Theories

- v0.1: Random approach.  
- v0.2: Nice guess - Based on the last action.
- v0.3: Guessing - Random based on the last action.
- v1.1: Roulette - Guess based on the last actions.
- v1.2: Roulette - Guess based on the last actions, more decimals.
- v1.3: Roulette - Guess based on the last actions, with threshold.
- v2.0: 2D Transaction-Matrix - Infer the next action based on the last action.
- v2.1: 3D Transaction-Matrix - Infer the next action based on the last two actions.
- v3.0: 2D Counter Transaction-Matrix - Infer the next action based on the my previous action.
- v3.1: 3D Counter Transaction-Matrix - Infer the next action based on the my previous action, and his last action.
- v4.0: Multi Transaction-Matrix - Combine many transaction-matrix strategies.

---
## Local test

Create a [environment](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/), and install dependences.
```shell
$ pip install --upgrade pip
$ pip install jupyter-client==6.1.5
$ pip install jupyterlab
$ pip install notebook
$ pip install voila
```

---
## Also look ~

- Created by Leonardo Mauro ~ [leomaurodesenv](https://github.com/leomaurodesenv/)
