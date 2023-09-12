#!/bin/dash

PATH="$PATH:$(pwd)"

num=4
echo Running subset 0

# tests basic + hollow printing
while [ "$num" -le 10 ]:
do

    python3.10 sheepy.py test0"$num".sh > temp.py
    if ! test "$(diff temp.py test0"$num".py)" = ""
    then
        echo autotest $num failed
        diff temp.py test0"$num".py
        exit
    else
        echo autotest $num passed
    fi
    num=$((num + 1))
    if [ $num = 3 ]
    then
        echo Running subset 1
    fi
    if [ $num = 9 ]
    then
        echo Running subset 2
    fi

done
