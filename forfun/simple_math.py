#!/usr/bin/env python
# Wenchang Yang (wenchang@princeton.edu)
# Fri Jul 23 15:35:22 EDT 2021
#import xarray as xr, numpy as np, pandas as pd
#import matplotlib.pyplot as plt
#more imports
import random
from termcolor import colored, cprint
#
#
#start from here
numbers_set1 = range(10, 20)
#numbers_set2 = range(10)
numbers_set2 = range(1, 20)
operators = ['+', '-'][1:]

student = 'Sarah'
score = 0
points_per_problem = 5 
n_problems = 20
full_score = points_per_problem * n_problems
cprint('#'*10 + f'Simple Math Game for {student}'+'#'*10, 'green')
input(colored('Are you ready? Press Return to start:', 'green'))
for ii in range(1, n_problems+1):
    a = random.choice(numbers_set1)
    b = random.choice(numbers_set2)
    operator = random.choice(operators)
    if operator == '-' and a < b:
        a,b = b,a
    if operator == '+':
        true_ans = a + b
    else:
        true_ans = a - b
    s = f'[{ii:02d} of {n_problems}]: {a} {operator} {b} = '
    ans = input(s)
    try:
        ans = int(ans)
    except ValueError:
        cprint(f'You did not input a number! Your score is now {score}.', 'red')
        continue
    if ans == true_ans:
        score += points_per_problem
        cprint(f'You are right!:) Your score is now {score}.', 'green')
    else:
        cprint(f'You are wrong!:( Your score is now {score}.', 'red')

print(f'Your final score is {score}.') 
if score == full_score:
    cprint(f'Congratulations, {student}! You got a full score!', 'green')
else:
    cprint(f'Keep working, {student}. You can do it!', 'yellow')
 
    
