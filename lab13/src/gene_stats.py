import sys
from parse_gff import read_gff

# GFF 파일에서 CDS 주석만 골라 길이와 방향을 분석한다
features = read_gff(sys.argv[1])

cds_list = []
for f in features:
    if f["type"] == "CDS":
        # GFF 좌표는 1부터 시작하고 양 끝을 포함하므로 1을 더한다
        f["length"] = f["end"] - f["start"] + 1
        cds_list.append(f)

if len(cds_list) == 0:
    print("CDS 주석이 없습니다.")
    sys.exit()

lengths = []
for f in cds_list:
    lengths.append(f["length"])

mean_len = sum(lengths) / len(lengths)

print("== CDS 길이 통계 ==")
print("개수:", len(cds_list))
print("평균 길이:", round(mean_len, 1), "bp")
print("최소 길이:", min(lengths), "bp")
print("최대 길이:", max(lengths), "bp")
print("평균 아미노산 개수 (평균 길이 / 3):", round(mean_len / 3, 1))

# 방향별 개수
plus = 0
minus = 0
for f in cds_list:
    if f["strand"] == "+":
        plus = plus + 1
    elif f["strand"] == "-":
        minus = minus + 1

print()
print("== 방향 ==")
print("정방향(+):", plus)
print("역방향(-):", minus)

# 가장 긴 CDS 다섯 개
cds_list.sort(key=lambda f: f["length"], reverse=True)

print()
print("== 가장 긴 CDS 5개 ==")
for f in cds_list[:5]:
    print(f["seqid"], f["start"], f["end"], f["strand"], f["length"], sep="\t")
    print("\t" + f["attributes"])
