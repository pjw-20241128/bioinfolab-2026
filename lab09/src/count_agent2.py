import sys
from fasta import read_fasta

if len(sys.argv) != 2:
    print("사용법: python3 src/count_agent2.py <FASTA 파일>")
    sys.exit(1)

seqs = read_fasta(sys.argv[1])
print(len(seqs))
