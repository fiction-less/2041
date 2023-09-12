#!/bin/dash

#for llops
for i in 1 2 3
do
    echo $i
done

for word in this is a string
do
    echo $word
done

for file in *.c
do
    echo $file
done

for c_file in *.c
do
    echo gcc -c $c_file
done

# testing some of the while and ifs

if test -r $file
then
    echo hi
fi
if [ -r $file ]
then
    echo hi
fi
if test -r /dev/null
then
    echo hi
fi
if [ -r /dev/null ]
then
    echo hi
fi
if test -r gpd$file$file2
then
    echo hi
fi
if [ -r gpd$file$file2 ]
then
    echo hi
fi

if test s = f
then
    echo hi
fi

if [ s$fo$dof = $god ]
then
    echo hi
fi
if test s$fo$dof != $god
then
    echo hi
fi
if [ "$fo$fow  m" = "$god" ]
then
    echo hi
fi

if test s=m
then
    echo hi
fi
if [ s$fo$dof=$god ]
then
    echo hi
fi
if test s$fo$dof!=$god$d
then
    echo hi
fi
if [ "$fo$fow  m"="$god" ]
then
    echo hi
fi

if test $fo=$god
then
    echo hi
fi
if [ $fo=$god ]
then
    echo hi
fi
if test "$fo$fow  m"="$god"
then
    echo hi
fi
if [ "$fo$fow  m"="$god" ]
then
    echo hi
fi

if test "m$andrew" = r
then
    echo hi
fi
if test s$fo$dof$2!=m$god
then
    echo hi
fi

while test 2 -le 3
do
    echo hi
    exit
done
while [ 2 -le 3 ]
do
    echo hi
    exit
done
