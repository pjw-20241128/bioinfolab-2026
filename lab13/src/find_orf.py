import sys

STOPS = ["TAA", "TAG", "TGA"]

# 역상보 서열을 만들 때 쓰는 짝 (A/T/G/C 외 문자는 N 으로 바꾼다)
COMPLEMENT = {"A": "T", "T": "A", "G": "C", "C": "G"}


def reverse_complement(seq):
    return "".join(COMPLEMENT.get(base, "N") for base in reversed(seq))


def find_orfs(seq, frame):
    orfs = []
    start = None

    for i in range(frame, len(seq) - 2, 3):
        codon = seq[i:i + 3]

        if codon == "ATG" and start is None:
            start = i
        elif codon in STOPS and start is not None:
            orfs.append((start, i + 3))
            start = None

    return orfs


seq = sys.argv[1].upper()
rc_seq = reverse_complement(seq)

# 정방향(+) 가닥과 역상보(-) 가닥에서 각각 세 개의 틀을 검사한다
for strand, s_seq in [("+", seq), ("-", rc_seq)]:
    print("가닥", strand, ":", s_seq)
    for frame in [0, 1, 2]:
        orfs = find_orfs(s_seq, frame)
        print("틀", strand + str(frame + 1), ":", orfs)
        for s, e in orfs:
            print("   ", s_seq[s:e], "길이", e - s)
