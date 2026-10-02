#!/usr/bin/bash
# countseq.sh — FASTA 파일의 서열 개수를 출력한다
# 사용법: countseq.sh <FASTA파일>
 
if [ -z "$1" ] || [ ! -f "$1" ]
then
    echo "오류: 파일을 찾을 수 없습니다."
    exit 1
fi

SEQ_COUNT=$(grep -c ">" "$1")
SEQ_NAME=$(grep ">" "$1" | tr ">" " ")
SEQ_TOTAL=$(grep -v ">" "$1" | tr -d '\n' | wc -m)

FILE="$1"
grep -c ">" "$FILE"

echo "파일: $FILE"
echo "서열 개수: $SEQ_COUNT"
echo "서열 이름:"
echo "$SEQ_NAME"
echo "총 염기 수(대략): $SEQ_TOTAL"