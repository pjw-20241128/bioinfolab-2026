# lab07 요약 — 함수와 파일 저장

## 1. 핵심 개념

| 개념 | 내용 | 실습 파일 |
|---|---|---|
| 함수 정의 | `def 이름(인자):` 로 반복되는 작업을 묶는다 | `fgc.py` |
| `print` vs `return` | `print`는 화면에 보여주기만 하고 `None`을 돌려줌. `return`은 값을 돌려주어 변수에 저장 가능 | `fseqlen.py` |
| 모듈과 `import` | 함수를 `fasta.py`에 모아두고 `from fasta import read_fasta` 로 다른 스크립트에서 재사용 | `countseq2.py`, `seqlen2.py` |
| `if __name__ == "__main__":` | 파일을 직접 실행할 때만 동작하고, `import` 될 때는 실행되지 않는 테스트 코드 블록 | `fasta.py`, `tool.py` |
| 명령행 인자 | `sys.argv[1]`, `sys.argv[2]` … 로 입력/출력 파일 경로를 받음 | 대부분의 스크립트 |
| 파일 쓰기 | `with open(파일, "w") as out:` + `out.write(...)` (줄바꿈 `\n` 직접 추가) | `summary.py`, `write_fasta` |
| 여러 파일 처리 | `glob.glob(폴더 + "/*.fasta")` 로 파일 목록을 얻어 반복 | `batchinfo2.py` |

## 2. 함수 모듈 `src/fasta.py`

| 함수 | 입력 | 출력 |
|---|---|---|
| `read_fasta(filename)` | FASTA 파일 경로 | `{이름: 서열}` 딕셔너리 (헤더의 첫 단어를 이름으로, 서열은 대문자로 변환) |
| `lengths_stats(seqs)` | 서열 딕셔너리 | `count`, `total`, `avrg`, `min`, `max` 를 담은 딕셔너리 |
| `gc_content(seq)` | 서열 문자열 | GC 비율 (0~1, 빈 서열이면 0.0) |
| `reverse_complement(seq)` | 서열 문자열 | 상보 염기로 바꾼 뒤 뒤집은 서열 |
| `write_fasta(seqs, filename)` | 서열 딕셔너리, 저장 경로 | FASTA 파일로 저장 (반환값 없음) |

사용 예:

```python
from fasta import read_fasta, lengths_stats, gc_content, reverse_complement, write_fasta

seqs = read_fasta("data/seqs.fasta")
stats = lengths_stats(seqs)
gc = gc_content("ATGCGC")
rc = reverse_complement("ATGCGC")
write_fasta(seqs, "doc/out.fasta")
```

## 3. 스크립트 정리

| 스크립트 | 사용법 | 하는 일 |
|---|---|---|
| `fgc.py` | `python fgc.py` | GC 비율 함수 정의·호출 연습 |
| `fseqlen.py` | `python fseqlen.py` | `print` 함수와 `return` 함수의 차이 확인 (`a = None`, `b = 4`) |
| `countseq2.py` | `python countseq2.py 입력.fasta` | 서열 개수 출력 |
| `seqlen2.py` | `python seqlen2.py 입력.fasta` | 서열별 길이 출력 |
| `stats.py` | `python stats.py 입력.fasta` | 개수·총 길이·평균·최소·최대 길이 출력 |
| `summary.py` | `python summary.py 입력.fasta 출력.tsv` | 서열별 `name / length / gc` 표를 TSV로 저장 |
| `filter_fasta.py` | `python filter_fasta.py 입력.fasta 최소길이 출력.fasta` | 최소 길이 이상 서열만 골라 FASTA로 저장 |
| `batchinfo2.py` | `python batchinfo2.py 폴더 출력.tsv` | 폴더 안 모든 FASTA 파일의 서열 수·총 길이·평균 GC를 한 표로 저장 |

### lab06 `seqlen.py` → lab07 `seqlen2.py` 비교

lab06에서는 FASTA 읽기 코드를 스크립트 안에 직접 썼고, lab07에서는 그 부분을 `read_fasta` 함수로 빼서 `import` 해 쓴다.

```python
# lab06/src/seqlen.py — 파일 읽기와 길이 계산을 한 스크립트에서 모두 처리
import sys

filename = sys.argv[1]
lengths = {}

with open(filename) as f:
    for line in f:
        line = line.rstrip()
        if line.startswith(">"):
            name = line[1:].split()[0]
            lengths[name] = 0
        else:
            lengths[name] = lengths[name] + len(line)

for name in lengths:
    print(name, lengths[name])
```

```python
# lab07/src/seqlen2.py — 읽기는 fasta.py의 함수에 맡김
import sys
from fasta import read_fasta

seqs = read_fasta(sys.argv[1])

for name in seqs:
    print(len(seqs[name]))
```

| 항목 | `seqlen.py` (lab06) | `seqlen2.py` (lab07) |
|---|---|---|
| FASTA 읽기 | 스크립트 안에 직접 작성 | `read_fasta` 함수 재사용 |
| 저장하는 값 | `{이름: 길이}` (숫자만 누적) | `{이름: 서열}` (서열 전체 보관) |
| 출력 | `이름 길이` | `길이` 만 (이름 없음) |
| 재사용성 | 다른 스크립트에서 쓰려면 코드 복사 필요 | GC 계산·필터 등에 같은 함수 사용 가능 |

`seqlen2.py` 에서 `print(name, len(seqs[name]))` 로 바꾸면 lab06과 같은 출력이 된다.

## 4. 결과물

- `doc/summary.tsv` — `data/seqs.fasta` 의 서열별 요약

  | name | length | gc |
  |---|---|---|
  | gene1 | 30 | 0.5 |
  | gene2 | 15 | 0.4667 |
  | gene3 | 22 | 0.5455 |

- `doc/long.fasta` — 길이 필터를 통과한 서열 (gene1, gene3)
- `final.tsv` — `data/` 폴더 전체 일괄 요약

  | 파일 | 서열 수 | 총 길이 | 평균 GC |
  |---|---|---|---|
  | data/lower.fasta | 2 | 20 | 0.650 |
  | data/seqs.fasta | 3 | 67 | 0.504 |
  | data/seqs2.fasta | 2 | 16 | 0.250 |

  `lower.fasta` 는 소문자가 섞인 서열인데, `read_fasta` 에서 `.upper()` 로 변환했기 때문에 GC가 올바르게 계산된다.

## 5. 주의할 점 / 개선할 점

- `filter_fasta.py`: `sys.argv[2]` 는 문자열이므로 `int(sys.argv[2])` 로 바꿔야 길이와 비교할 수 있다.
- `batchinfo2.py`: 마지막 줄 `f"{'outfilename'}"` 은 변수 값이 아니라 글자 `outfilename` 이 출력된다 → `{outfilename}` 으로 수정.
- `fasta.py`의 `lengths_stats`: 빈 딕셔너리일 때 키가 `min_len`/`max_len` 이라 정상일 때의 `min`/`max` 와 다르다.
- `fasta.py`의 `reverse_complement`: `N` 같은 다른 문자가 있으면 `KeyError` 가 난다.
- `fasta.py`: `if __name__ == "__main__":` 블록이 두 개이고 중간에 함수 정의가 끼어 있음 → 파일 맨 끝에 하나로 합치는 것이 좋다.
- `tool.py`: `if __name__ == "__main__":` 이 함수 안(`return` 뒤)에 들여쓰기 되어 있어 실행되지 않는다.
- 없는 파일 경로를 넣었을 때의 예외 처리가 없다 (README에서 스스로 지적한 부분).
