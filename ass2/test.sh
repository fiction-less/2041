#!/bin/dash

PATH="$PATH:$(pwd)"

num=0

# tests basic + hollow printing
while [ "$num" -le 4 ]:
do

    python3.10 sheepy.py test0"$num".sh > temp.py
    if ! test "$(diff temp.py test0"$num".py)" = ""
    then
        echo autotest $num failed
        # diff temp.py test0"$num".py
    else
        echo autotest $num passed
    fi
    num=$((num + 1))


done
