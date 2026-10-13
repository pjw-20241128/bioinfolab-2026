import sys
from fasta import read_fasta, lengths_stats

infile = sys.argv[1]

seqs_read = read_fasta(infile)
stats_len = lengths_stats(seqs_read)

print(f"서열 개수는:\t{stats_len['count']}개")
print(f"전체 길이는:\t{stats_len['total']}bp")
print(f"평균 길이는:\t{stats_len['avrg']}bp")
print(f"가장 짧은 길이는:\t{stats_len['min']}")
print(f"가장 긴 길이는:\t{stats_len['max']}")