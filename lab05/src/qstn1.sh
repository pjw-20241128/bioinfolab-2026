A=hello
B="hello world"
 
echo $A
echo "$B"
echo '$B'
touch $B
echo $?
ls | wc -l
ls nowhere | wc -l
