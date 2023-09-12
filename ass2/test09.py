#!/usr/bin/python3 -u

import os
import subprocess
import sys



print(f"This program is: {sys.argv[0]}")

file_name = sys.argv[2]
number_of_lines = sys.argv[5]

print(f"going to print the first {number_of_lines} lines of {file_name}")
print(f"My first argument is {sys.argv[1]}")
print(f"My second argument is {sys.argv[2]}")
print(f"My third argument is {sys.argv[3]}")
print(f"My fourth argument is {sys.argv[4]}")
print(f"My fifth argument is {sys.argv[5]}")

string = "BAR"
print(f"FOO{string}BAZ")

row = "1"
while row != "11111111111":
    print(row)
    row = f"1{row}"

if "Andrew" == "great":
    print("correct")
elif "Andrew" == "fantastic":
    print("yes")
else:
    print("error")

if os.access("/dev/null", os.R_OK):
    print("a")

if os.access("nonexistantfile", os.R_OK):
    print("b")

start = sys.argv[1]
finish = sys.argv[2]

number = start
while int(number) <= int(finish):
    print(number)
    number = subprocess.run(['expr', number, '+', '1'], text=True, stdout=subprocess.PIPE).stdout.rstrip('\n') # increment number

print('When old age shall this generation waste,')
print('Thou shalt remain, in midst of other woe')
print('Than ours, a friend to man, to whom thou sayst,')
print('"Beauty is truth, truth beauty",  -  that is all')
print('Ye know on earth, and all ye need to know.')
