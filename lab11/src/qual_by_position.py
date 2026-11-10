import sys

# FASTQ 파일의 모든 read 에서 같은 위치(1번째, 2번째, ... 염기)의 품질 점수를 모아
# 위치별 평균 품질을 계산하고, "위치<TAB>평균 품질" 형식으로 출력한다.
# FastQC 의 Per base sequence quality 그래프의 평균값(파란 선)과 같은 값이다.


def read_fastq(filename):
    records = []
    with open(filename) as f:
        lines = f.readlines()
    for i in range(0, len(lines), 4):
        name = lines[i].rstrip()[1:]
        seq = lines[i + 1].rstrip()
        qual = lines[i + 3].rstrip()
        records.append((name, seq, qual))
    return records


def quality_by_position(reads):
    # totals[i]: i번째 위치 품질 점수의 합, counts[i]: 그 위치까지 길이가 되는 read 수
    totals = []
    counts = []
    for name, seq, qual in reads:
        for i, ch in enumerate(qual):
            q = ord(ch) - 33          # Phred+33 문자 -> 품질 점수
            if i == len(totals):      # 처음 보는 위치면 칸을 늘린다
                totals.append(0)
                counts.append(0)
            totals[i] = totals[i] + q
            counts[i] = counts[i] + 1
    means = []
    for i in range(len(totals)):
        means.append(totals[i] / counts[i])
    return means


if __name__ == "__main__":
    reads = read_fastq(sys.argv[1])
    means = quality_by_position(reads)

    print("position\tmean_quality")
    for i, m in enumerate(means):
        print(f"{i + 1}\t{m:.2f}")      # 위치는 1부터 센다
