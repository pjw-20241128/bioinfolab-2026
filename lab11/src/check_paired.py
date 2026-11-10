import sys

# 사용법: python3 src/check_paired.py data/SRR1553607_1.fastq data/SRR1553607_2.fastq
# paired-end 두 파일의 read 개수가 같은지, 같은 순서의 read 이름이 짝을 이루는지 확인한다.


def read_names(filename):
    """FASTQ 파일에서 read 이름(헤더의 첫 단어, @ 제외)만 순서대로 모은다."""
    names = []
    with open(filename) as f:
        for i, line in enumerate(f):
            if i % 4 == 0:
                names.append(line.rstrip().split()[0][1:])
    return names


def pair_key(name):
    """짝 비교용 이름: 끝의 /1, /2 같은 표시를 떼어 낸다.

    SRR1553607.1 처럼 '.숫자'는 read 번호이므로 떼면 안 된다.
    (떼면 SRR1553607.1 과 SRR1553607.2 가 같은 이름이 되어 버린다)
    """
    if len(name) >= 2 and name[-2] == "/" and name[-1] in "12":
        return name[:-2]
    return name


file1 = sys.argv[1]
file2 = sys.argv[2]

names1 = read_names(file1)
names2 = read_names(file2)

print("파일 1:", file1, "read 개수:", len(names1))
print("파일 2:", file2, "read 개수:", len(names2))

if len(names1) == len(names2):
    print("read 개수: 같음")
else:
    print("read 개수: 다름 (차이", abs(len(names1) - len(names2)), ")")

# 짧은 쪽 길이만큼 같은 순서의 read 이름을 비교한다
mismatch = 0
for i, (n1, n2) in enumerate(zip(names1, names2)):
    if pair_key(n1) != pair_key(n2):
        mismatch = mismatch + 1
        if mismatch <= 5:
            print("짝 불일치", i + 1, "번째:", n1, "/", n2)

print("비교한 read 쌍:", min(len(names1), len(names2)))
print("이름이 짝을 이루지 않는 쌍:", mismatch)

if len(names1) == len(names2) and mismatch == 0:
    print("결과: 두 파일은 올바른 paired-end 짝이다")
else:
    print("결과: 두 파일의 짝이 맞지 않는다")
