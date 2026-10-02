#!/usr/bin/bash
#폴더의 구조를 보여줌
# 사용법: mkproject2.sh <FASTA파일>

NAME=$1
if [ -z "$1" ] 
then
    echo "사용법: $0 <FOLDER>"
    echo " 주어진 FOLDER의 서열 개수를 출력합니다."
    exit 1
fi

if [ -d "$1" ]
then
    echo "오류: 이미 같은 이름의 폴더가 있습니다."
    exit 1
fi

mkdir -p "$1"/data 

mkdir -p "$1"/src

mkdir -p "$1"/doc 
tree "$1"