import sys
import os

if len(sys.argv) < 2:
    print("사용법: python3 countseq.py <폴더명>")
    print(len(sys.argv))
    sys.exit(1)

foldername = sys.argv[1]

if os.path.isdir(foldername):
    print("오류: 같은 이름의 폴더가 이미 있습니다.:", foldername)
else:
    subfolders=["data", "src", "doc"]
    for sub in subfolders: 
        os.makedirs(f"{foldername}/{sub}")
