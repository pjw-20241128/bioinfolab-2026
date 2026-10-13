fasta.py 에 들어 있는 함수 목록
ㄴ read_fasta / lengths_stats / gc_content / reverse_complemet / write_fasta

각 함수가 무엇을 받아서 무엇을 돌려주는지 한 줄 설명
ㄴ read_fasta는 FASTA파일의 경로를 인자로 받아 서열이름과 염기서열을 딕셔너리에 돌려준다.
ㄴ lengths_stats는 read_fasta에서 만든 서열 딕셔너리를 받아 서열 개수, 총 길이, 평균, 최솟값, 최댓값을 담은 딕셔너리를 돌려준다.
ㄴ gc_content는 단일 염기서열 문자열을 인자로 받아 염기 G와 C의 비율을 돌려준다.
ㄴ reverse_complement는 단일 염기서열 문자열을 인자로 받아 각 염기의 상보 염기로 치환한뒤 순서를 뒤집어 돌려준다.
ㄴ wirte_fasta는 서열딕셔너리와 파일 경로를 받아 FASTA확장자의 형태로 파일을 저장한다.

각 함수를 쓰는 예 한 줄
ㄴread_fasta: seq_data= read_fasta("data/*.fasta")
ㄴlengths_stats: stats= lengths_stats(seq_data)
ㄴgc_content: gc_ratio= gc_content("ATGCGC")
ㄴreverse_complement: rev_seq= reverse_complement("ATGCGC")
ㄴwrite_fasta: write_fasta(seq_data, "output/result.fasta")

아직 부족하다고 느끼는 점이나 추가하고 싶은 함수
ㄴ존재하지 않는 파일 경로를 전달하거나 잘못된 파일을 읽었을 때에 대한 예외 처리가 부족한 것 같다. 
  따라서, bash에서 만들었듯이 사용자가 현재 오류를 실행하고 있는 경우 오류 출력이 아니라, 오류 내용을 표준 출력할 수 있는 함수가 있으면 좋겠다.