string=BAR
echo FOO${string}BAZ

row=1
while test $row != 11111111111
do
    echo $row
    row=1$row
done

if test Andrew = great
then
    echo correct
elif test Andrew = fantastic
then
    echo yes
else
    echo error
fi

if test -r /dev/null
then
    echo a
fi

if test -r nonexistantfile
then
    echo b
fi