#!/bin/dash

echo What is your name:
read name

echo What is your quest:
read quest

echo What is your favourite colour:
read colour

echo What is the airspeed velocity of an unladen swallow:
read velocity

echo Hello $name, my favourite colour is $colour too.

for n in one two three
do
    read line
    echo Line $n $line
done