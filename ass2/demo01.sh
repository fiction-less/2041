#!/bin/dash

# echo writteb bysekf, furst half from privded exmples

touch test_file.txt
ls -l test_file.txt

for course in COMP1511 COMP1521 COMP2511 COMP2521 # keyword
do                                                # keyword
    echo $course                                  # builtin
    mkdir $course                                 # external command
    chmod 700 $course                             # external command
done
variable=dong
hi=hiiii
boy=girl
string=gae

echo 'This is not a "$variable"' but $hi

echo 'This is not a "$variable"' but $hi there

echo "This is a $variable" but $hi

echo 'This is not a $variable'

echo 'This is not a glob *.sh'

echo $boy

echo FOO${string}BAZ

echo -n "How many? "