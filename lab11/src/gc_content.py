import sys

# FASTQ 파일의 각 read 에 대해 GC 비율과 평균 품질을 함께 계산한다.
# GC 비율이 가장 높은 read 10개와 가장 낮은 read 10개를 골라,
# 그 read 들의 평균 품질이 전체 평균과 얼마나 차이 나는지 비교한다.

N_PICK = 10   # 양 극단에서 고를 read 수


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


def gc_ratio(seq):
    seq = seq.upper()
    gc = seq.count("G") + seq.count("C")
    return gc / len(seq)


def mean_quality(qual):
    scores = []
    for ch in qual:
        scores.append(ord(ch) - 33)
    return sum(scores) / len(scores)


def group_mean(rows):
    total = 0
    for name, gc, q in rows:
        total = total + q
    return total / len(rows)


def print_group(title, rows, overall):
    print(f"## {title}")
    print("name\tgc\tmean_quality")
    for name, gc, q in rows:
        print(f"{name}\t{gc:.3f}\t{q:.2f}")
    m = group_mean(rows)
    print(f"그룹 평균 품질: {m:.2f} (전체 평균과 차이: {m - overall:+.2f})")
    print()


if __name__ == "__main__":
    reads = read_fastq(sys.argv[1])

    # read 마다 (이름, GC 비율, 평균 품질) 을 만든다
    rows = []
    for name, seq, qual in reads:
        rows.append((name.split()[0], gc_ratio(seq), mean_quality(qual)))

    overall_gc = sum(r[1] for r in rows) / len(rows)
    overall_q = group_mean(rows)

    # GC 비율 기준으로 정렬하여 양 끝에서 10개씩 고른다
    rows_sorted = sorted(rows, key=lambda r: r[1])
    low = rows_sorted[:N_PICK]
    high = rows_sorted[-N_PICK:][::-1]

    print(f"전체 read 수: {len(rows)}")
    print(f"전체 평균 GC 비율: {overall_gc:.3f}")
    print(f"전체 평균 품질: {overall_q:.2f}")
    print()
    print_group(f"GC 비율이 가장 높은 read {N_PICK}개", high, overall_q)
    print_group(f"GC 비율이 가장 낮은 read {N_PICK}개", low, overall_q)
