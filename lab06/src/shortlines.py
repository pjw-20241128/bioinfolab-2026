import sys
import os

if len(sys.argv) < 3:
    print("사용법: python3 countseq.py <FASTA파일> <최소길이>")
    sys.exit(1)

filename=sys.argv[1]
minilen=sys.argv[2]

if not os.path.isfile(filename):
    print("오류: 폴더를 찾을 수 없습니다:", filename)
    sys.exit(2)
else: 
    if minilen.isdigit():
        min_length=int(minilen)
        count=0
        with open(filename) as f:
            for line in f:
                line = line.rstrip()
                if not line.startswith(">") and len(line)<min_length:
                    count +=1
        print(count)
    else:
        print("사용법: python3 countseq.py <FASTA파일> <최소길이>\n오류: 최소 길이에는 숫자를 입력해주세요.")

lengths={}
name=None

