def read_fasta(filename):
    """FASTA 파일을 읽어 {이름: 서열} 딕셔너리로 돌려준다."""
    seqs = {}
    name = None
    with open(filename) as f:
        for line in f:
            line = line.rstrip()
            if line.startswith(">"):
                name = line[1:].split()[0]
                seqs[name] = ""
            else:
                seqs[name] = seqs[name] + line.upper()
    return seqs

def lengths_stats(seqs):
    """read_fasta로부터 딕셔너리를 받아 그의 정보 5개를 돌려준다."""

    if not seqs:
        return{"count": 0, "total": 0, "avrg": 0.0, "min_len": 0, "max_len": 0 }
    lengths = []
    for seq in seqs.values():
        lengths.append(len(seq))

    count = len(lengths)
    total = sum(lengths)
    avrg = total / count
    min_len = min(lengths)
    max_len = max(lengths)
    return{
        "count": count,
        "total": total,
        "avrg": avrg,
        "min": min_len,
        "max": max_len
    }

def reverse_complement(seq):
    """서열의 염기를 상보적인 염기로 치환하고 역순으로 바꾼다."""
    cmplmtry = {"A": "T", "T": "A", "G": "C", "C": "G"}
    result =""
    for base in seq:
        result = result + cmplmtry[base]
    return result[::-1]

if __name__ == "__main__":
    test_seq = "ATGC"
    print(reverse_complement(reverse_complement(test_seq))== test_seq)

def write_fasta(seqs, filename):
    """{이름: 서열} 딕셔너리를 FASTA 파일로 저장한다."""
    with open(filename, "w") as out:
        for name in seqs:
            out.write(">" + name + "\n")
            out.write(seqs[name] + "\n")
 
def gc_content(seq):
    """서열의 GC 비율을 0과 1 사이의 수로 돌려준다."""
    if len(seq) == 0:
        return 0.0
    gc = seq.count("G") + seq.count("C")
    return gc / len(seq)
 
 
if __name__ == "__main__":
    import sys
    seqs = read_fasta(sys.argv[1])
    for name in seqs:
        print(name, len(seqs[name]), round(gc_content(seqs[name]), 3))