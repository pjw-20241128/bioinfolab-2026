FOLDER=$1
for x in $FOLDER/*.fasta
do
    echo -e "$x\t$(grep -c ">" "$x")"
done