#!/bin/dash



echo hello world
exit
echo this will not be printed
exit 0
echo this will double not be printed
exit 3

for word in Houston 1202 alarm
do
    echo $word
    exit 0
done

for word in Houston 1202 alarm
do
    echo $word
    exit
done

echo *
cd /tmp
echo *
cd ..
echo *