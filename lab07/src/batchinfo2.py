import sys
import glob
from fasta import read_fasta, lengths_stats, gc_content

infolder=sys.argv[1]
outfilename= sys.argv[2]

with open(outfilename, "w") as out:

    for inf in sorted(glob.glob(infolder + "/*.fasta")):
        seqs_read = read_fasta(inf)
        stats_len = lengths_stats(seqs_read)

        if len(seqs_read) >0:
            total_gcrate = sum(gc_content(seq) for seq in seqs_read.values())
            avrg_gcrate = total_gcrate / len(seqs_read)
        else: avrg_gcrate = 0.0

        count = stats_len["count"]
        total_len = stats_len["total"]

        out.write(f"{inf}\t{count}\t{total_len}\t{avrg_gcrate:.3f}\n")

print(f"결과를 {'outfilename'}으로 저장했습니다.")