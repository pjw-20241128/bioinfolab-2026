# 길이가 L 인 서열에서 k-mer 의 개수를 구한다.
# 사용법: python3 src/count_kmers.py


def count_kmers(L, k):
    """길이 L 인 서열에서 나올 수 있는 k-mer 개수 (L - k + 1) 를 돌려준다.

    - k > L 이면 k-mer 를 하나도 만들 수 없으므로 0 을 돌려준다.
    - L 이 음수이거나 k 가 1 보다 작으면 의미가 없으므로 ValueError 를 낸다.
    """
    if L < 0:
        raise ValueError(f"L 은 0 이상이어야 합니다: L={L}")
    if k < 1:
        raise ValueError(f"k 는 1 이상이어야 합니다: k={k}")
    if k > L:
        return 0
    return L - k + 1


def count_by_hand(L, k):
    """함수 공식을 쓰지 않고, 길이 L 인 서열을 실제로 만들어 창을 밀며 센다."""
    seq = "A" * L
    n = 0
    i = 0
    while i + k <= len(seq):
        kmer = seq[i:i + k]
        if len(kmer) == k:
            n += 1
        i += 1
    return n


if __name__ == "__main__":
    cases = [(10, 5), (10, 1), (10, 10), (10, 11), (1, 1),
             (0, 3), (5, 3), (100, 21), (3, 7), (1000, 31)]

    print("L\tk\t직접계산\t함수\t일치")
    all_ok = True
    for L, k in cases:
        hand = count_by_hand(L, k)
        func = count_kmers(L, k)
        ok = hand == func
        all_ok = all_ok and ok
        print(f"{L}\t{k}\t{hand}\t{func}\t{'O' if ok else 'X'}")

    # 1~30 범위의 모든 조합도 확인
    for L in range(0, 31):
        for k in range(1, 31):
            if count_by_hand(L, k) != count_kmers(L, k):
                all_ok = False
                print(f"불일치: L={L}, k={k}")

    print("모든 조합 일치" if all_ok else "불일치가 있음")

    # 수업 예제 서열로도 확인 (src/kmers.py 와 같은 서열)
    seq = "TATGGGGTGC"
    k = 5
    kmers = [seq[i:i + k] for i in range(len(seq) - k + 1)]
    print(f"예제 서열 {seq}: 실제 {len(kmers)}개, 함수 {count_kmers(len(seq), k)}개")
