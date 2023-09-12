#!/usr/bin/python3 -u

import glob
import subprocess



subprocess.run(['touch', 'test_file.txt'])
subprocess.run(['ls', '-l', 'test_file.txt'])

for course in ["COMP1511", "COMP1521", "COMP2511", "COMP2521"]: # keyword
# keyword
    print(course) # builtin
    subprocess.run(['mkdir', course]) # external command
    subprocess.run(['chmod', '700', course]) # external command
variable = "dong"
hi = "hiiii"
boy = "girl"
string = "gae"

print(f'This is not a "$variable" but {hi}')

print(f'This is not a "$variable" but {hi} there')

print(f"This is a {variable} but {hi}")

print('This is not a $variable')

print('This is not a glob *.sh')

print(boy)

print(f"FOO{string}BAZ")

print("How many? ", end="")
