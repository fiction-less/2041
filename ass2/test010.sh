#!/bin/dash

x='###'
while test $x != '########'
do
    y='#'
    while test $y != $x
    do
        echo $y
        y="${y}#"
    done
    x="${x}#"
done

status=off
while test "$status" != on
do
    echo "status is $status"
    if test "$status" = "half on"
    then
        status="on"
    else
        status="half on"
    fi
done