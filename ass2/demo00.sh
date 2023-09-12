#!/bin/dash

# from samples

echo This program is: $0

file_name=$2
number_of_lines=$5

echo going to print the first $number_of_lines lines of $file_name
echo My first argument is $1
echo My second argument is $2
echo My third argument is $3
echo My fourth argument is $4
echo My fifth argument is $5
echo 'When old age shall this generation waste,'
echo 'Thou shalt remain, in midst of other woe'
echo 'Than ours, a friend to man, to whom thou sayst,'
echo '"Beauty is truth, truth beauty",  -  that is all'
echo 'Ye know on earth, and all ye need to know.'


start=$1
finish=$2

number=$start
while test $number -le $finish
do
    echo $number
    number=`expr $number + 1`  # increment number
done
