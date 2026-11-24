import sys
from fasta import read_fasta

# 사용법: python3 src/gene_density.py data/contigs.fa doc/prokka_out/sample.gff
# 유전체 길이, 유전자 밀도(1000 염기당 CDS 수), 코딩 밀도를 계산한다

fasta_file = sys.argv[1]
gff_file = sys.argv[2]

# 1. 전체 유전체 길이 = 모든 contig 길이의 합
seqs = read_fasta(fasta_file)
genome_len = 0
for name in seqs:
    genome_len = genome_len + len(seqs[name])

# 2. GFF 에서 CDS 의 개수와 길이 합을 구한다
cds_count = 0
cds_total = 0
with open(gff_file) as f:
    for line in f:
        if line.startswith("##FASTA"):
            break
        if line.startswith("#") or line.strip() == "":
            continue
        cols = line.rstrip("\n").split("\t")
        if len(cols) < 9 or cols[2] != "CDS":
            continue
        # GFF 좌표는 1부터 시작하고 양 끝을 포함하므로 1을 더한다
        length = int(cols[4]) - int(cols[3]) + 1
        cds_count = cds_count + 1
        cds_total = cds_total + length

if genome_len == 0 or cds_count == 0:
    print("유전체 길이나 CDS 개수가 0 입니다.")
    sys.exit()

# 3. 유전자 밀도와 코딩 밀도
genes_per_kb = cds_count / genome_len * 1000
coding_density = cds_total / genome_len * 100

print("contig 수:", len(seqs))
print("전체 유전체 길이:", genome_len, "bp")
print("CDS 개수:", cds_count)
print("1000 염기당 유전자 수:", round(genes_per_kb, 3))
print("CDS 길이 총합:", cds_total, "bp")
print("코딩 밀도:", round(coding_density, 2), "%")
