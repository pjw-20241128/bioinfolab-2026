#!/usr/bin/bash

if [ "$#" -ne 2 ]; then
    echo "오류: 인자 개수가 올바르지 않습니다."
    echo "사용법: $0 <FASTA파일> <최소길이>"
    exit 1
fi

FILE="$1"
MIN_LEN="$2"

if [ ! -f "$FILE" ]; then
    echo "오류: '$FILE' 파일이 존재하지 않습니다."
    exit 1
fi

if [[ ! "$MIN_LEN" =~ ^[0-9]+$ ]]; then
    echo "오류: 최소 길이는 0 이상의 정수이어야 합니다."
    exit 1
fi

SHORT_COUNT=0

while IFS= read -r line || [ -n "$line" ]
do
    if [[ "$line" =~ ^\> ]] || [ -z "$line" ]; then
        continue
    fi
    
    seq_line=$(echo -n "$line" | tr -d '\r ')
    line_len=${#seq_line}
    
    if [ "$line_len" -lt "$MIN_LEN" ]; then
        SHORT_COUNT=$(( SHORT_COUNT + 1 ))
    fi
done < "$FILE"

# 5. 최종 결과 출력
echo "최소 길이($MIN_LEN bp)보다 짧은 서열 줄 수: $SHORT_COUNT"