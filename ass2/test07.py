#!/usr/bin/python3 -u

print("What is your name:")
name = input()

print("What is your quest:")
quest = input()

print("What is your favourite colour:")
colour = input()

print("What is the airspeed velocity of an unladen swallow:")
velocity = input()

print(f"Hello {name}, my favourite colour is {colour} too.")

for n in ["one", "two", "three"]:
    line = input()
    print(f"Line {n} {line}")
