#!/usr/bin/env python
# Wenchang Yang (wenchang@princeton.edu)
# Fri Jul 23 15:35:22 EDT 2021
#import xarray as xr, numpy as np, pandas as pd
#import matplotlib.pyplot as plt
#more imports
import random
from termcolor import colored, cprint
import sys, os
#
#
#start from here
student = 'Sarah'
msgs_good = ['good job', 'correct', 'wonderful',  ' -v Tingting 太棒了']
msgs_bad = ['oh no', "sorry but  wrong", 'too bad',  ' -v Tingting 做错了']
voices = [' ', '-v Tingting',]# '-v Dongmei', '-v Haohao', '-v Panpan']
#numbers_set1 = range(11,20)
#numbers_set2 = range(1,20)
numbers_set1 = range(10,1000)
numbers_set2 = range(10,1000)
numbers_set_mul = range(2,10)
numbers_set_div = range(2,10)
div = chr(247)
operators = []    
if len(sys.argv)>1:#subset of operators
    if 'x' in sys.argv or 'mul' in sys.argv:
        operators.append('x') 
        if '100' in sys.argv:
            numbers_set_mul = range(2,100)
    if '/' in sys.argv or 'div' in sys.argv:
        operators.append(div) 
    if '+' in sys.argv or 'add' in sys.argv:
        operators.append('+') 
    if '-' in sys.argv or 'sub' in sys.argv:
        operators.append('-') 
if not operators:
    operators = ['+', '-', 'x', div] #+ ['x',] # 50% 'x'
        
happyFace ='\U0001F600'
frowningFace = '\U0001F641'

score = 0
n_problems = 20#25
points_per_problem = 100//n_problems#4
full_score = points_per_problem * n_problems
cprint('#'*10 + f'Math Game for {student}'+'#'*10, 'green')
#input(colored(happyFace + ' Are you ready? Press Return to start:', 'green'))
s = colored(happyFace + ' Are you ready? Press Return to start:', 'green')
print(s)
os.system(f'say Are you ready, {student}? Press Return to start:')
input()
for ii in range(1, n_problems+1):
    operator = random.choice(operators)
    if operator == 'x':
	    a = random.choice(numbers_set_mul)
	    b = random.choice(numbers_set_mul)
    elif operator == div:
	    a = random.choice(numbers_set_div)
	    b = random.choice(numbers_set_div)
	    a = a*b
    else:
        a = random.choice(numbers_set1)
        b = random.choice(numbers_set2)
    if operator == '-' and a < b:
        a,b = b,a
    #if operator == 'x' and a > b:
    #    a,b = b,a
    if operator == '+':
        true_ans = a + b
    elif operator == '-':
        true_ans = a - b
    elif operator == 'x':
	    true_ans = a*b	
    elif operator == div:
	    true_ans = a//b	
    else:
	    true_ans = None
		
    #s = f'[{ii:02d} of {n_problems}]: {a} {operator} {b} = '
    s = f'[{ii:02d} of {n_problems}]:\n{a:4d}\n{operator}{b:3d} \n----'
    print(s)
    voice = random.choice(voices)
    if operator == div:
        if voice.startswith('-v'):
            os.system(f'say {voice} {a} 除以 {b}')
        else:
            os.system(f'say {a} divided by {b}')
    elif operator == 'x':
        if voice.startswith('-v'):
            os.system(f'say {voice} {a} 乘以 {b}')
        else:
            os.system(f'say {a} times {b}')
    elif operator == '-':
        if voice.startswith('-v'):
            os.system(f'say {voice} {a} 减 {b}')
        else:
            os.system(f'say {a} minus {b}')
    else:
        os.system(f'say {voice} {a} {operator} {b}')
    ans = input('= ')
    try:
        ans = int(ans)
    except ValueError:
        cprint(f'You did not input a number! Your score is now {score} of {ii*points_per_problem}.', 'red')
        os.system(f'say {random.choice(msgs_bad)}')
        continue
    if ans == true_ans:
        score += points_per_problem
        cprint(happyFace + f' You are right!:) Your score is now {score} of {ii*points_per_problem}.', 'green')
        os.system(f'say {random.choice(msgs_good)}')
    else:
        cprint(frowningFace + f' You are wrong!:(Your score is now {score} of {ii*points_per_problem}.', 'red')
        os.system(f'say {random.choice(msgs_bad)}')

print(f'Your final score is {score}.') 
if score == full_score:
    cprint(happyFace*2 + f' Congratulations, {student}! You got a full score {full_score}!', 'green')
    os.system(f'say Congratulations, {student}! You got a full score {full_score}!')
elif score>=full_score - 2*points_per_problem:
    cprint(happyFace + f' Good job, {student}. Keep working!', 'green')
    os.system(f'say Good job, {student}. Keep working!')
else:
    cprint(frowningFace + f' Keep working, {student}. You can do it!', 'yellow')
    os.system(f'say Keep working, {student}. You can do it!')
