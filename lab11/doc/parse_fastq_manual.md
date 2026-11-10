# parse_fastq.py 사용법 및 설명서

## 1. 개요

`src/parse_fastq.py` 는 FASTQ 파일을 읽어 read 개수와 첫 번째 read 의 이름, 서열, 길이를 출력하는 짧은 Python 스크립트이다. 외부 라이브러리 없이 Python 표준 기능(`sys`)만 사용한다.

## 2. 실행 방법

`lab11` 폴더를 현재 위치로 두고 상대 경로로 실행한다.

```
$ cd lab11
$ python3 src/parse_fastq.py data/SRR1553607_1.fastq
```

| 인자 | 설명 |
|------|------|
| `sys.argv[1]` | 읽을 FASTQ 파일 경로 (필수) |

결과는 화면(표준 출력)에만 나온다. 파일로 저장하려면 리다이렉션을 쓴다.

```
$ python3 src/parse_fastq.py data/SRR1553607_1.fastq > doc/parse_result.txt
```

## 3. 실행 예시

`data/SRR1553607_1.fastq` 로 실행한 실제 결과이다.

```
read 개수: 203445
첫 read 이름: SRR1553607.1 1 length=101
첫 read 서열: GTTAGCGTTGTTGATCGCGACGCAACAACTGGTAAAGAATCTGGAAGAAGGATATCAGTTCAAACGCTCAAGCGAGATGATGGATATTTTTGAACGACTCA
첫 read 길이: 101
```

파일은 813,780 줄이고, 4줄이 read 1개이므로 813,780 / 4 = 203,445 개와 일치한다.

## 4. FASTQ 형식

FASTQ 는 read 하나를 4줄로 기록한다.

```
@SRR1553607.1 1 length=101          <- 1줄: '@' + read 이름
GTTAGCGTTGTTGATCGCGACG...            <- 2줄: 염기 서열
+SRR1553607.1 1 length=101          <- 3줄: '+' (이름 반복은 선택)
BB@FFFFFHHHHHJJJJJJJJJ...            <- 4줄: 품질 점수 (서열과 길이 같음)
```

## 5. 코드 설명

### 5.1 `read_fastq(filename)` 함수

```python
def read_fastq(filename):
    records = []
    with open(filename) as f:
        lines = f.readlines()

    for i in range(0, len(lines), 4):
        name = lines[i].rstrip()[1:]
        seq = lines[i + 1].rstrip()
        qual = lines[i + 3].rstrip()
        records.append((name, seq, qual))

    return records
```

| 단계 | 내용 |
|------|------|
| `f.readlines()` | 파일 전체를 한 번에 읽어 줄 단위 리스트로 만든다. |
| `range(0, len(lines), 4)` | 0, 4, 8, ... 처럼 4줄씩 건너뛰며 각 read 의 첫 줄 위치를 얻는다. |
| `lines[i].rstrip()[1:]` | 줄 끝 개행을 지우고 맨 앞 `@` 를 뺀 나머지를 이름으로 쓴다. |
| `lines[i + 1]` | 서열 줄 |
| `lines[i + 3]` | 품질 점수 줄 (`lines[i + 2]` 인 `+` 줄은 건너뛴다) |
| 반환값 | `(이름, 서열, 품질)` 튜플의 리스트 |

### 5.2 메인 부분

```python
reads = read_fastq(sys.argv[1])
print("read 개수:", len(reads))
print("첫 read 이름:", reads[0][0])
print("첫 read 서열:", reads[0][1])
print("첫 read 길이:", len(reads[0][1]))
```

- `reads[0]` 은 첫 번째 read 튜플이고, `[0]` 은 이름, `[1]` 은 서열, `[2]` 는 품질이다.
- 이름은 헤더 줄 전체(공백 뒤 설명 포함)이다. 예: `SRR1553607.1 1 length=101`

## 6. 다른 스크립트에서 재사용하기

`read_fastq` 함수만 가져다 쓰려면 주의가 필요하다. 현재 메인 부분이 `if __name__ == "__main__":` 아래에 있지 않으므로, `from parse_fastq import read_fastq` 를 하면 import 하는 순간 메인 코드도 실행된다.

## 7. 주의 사항 및 한계

| 상황 | 결과 |
|------|------|
| 인자 없이 실행 | `IndexError: list index out of range` (`sys.argv[1]` 없음) |
| 없는 파일 경로 | `FileNotFoundError` |
| 빈 파일 | `read 개수: 0` 출력 후 `reads[0]` 에서 `IndexError` |
| 줄 수가 4의 배수가 아님 | 마지막 불완전한 read 에서 `IndexError` |
| `.fastq.gz` 압축 파일 | 그대로 읽을 수 없음 (먼저 `gunzip` 필요) |
| 서열이 여러 줄로 나뉜 FASTQ | 4줄 형식을 가정하므로 잘못 읽음 |
| 큰 파일 | `readlines()` 가 파일 전체를 메모리에 올리므로 메모리 사용량이 큼 |

- 품질 점수(`qual`)는 저장만 하고 출력이나 계산에는 쓰지 않는다.
- 헤더가 `@` 로 시작하는지, 서열과 품질의 길이가 같은지 검사하지 않는다.

## 8. 요약

- 사용법: `python3 src/parse_fastq.py <FASTQ 파일>`
- FASTQ 를 4줄 단위로 끊어 `(이름, 서열, 품질)` 리스트로 읽는다.
- read 개수와 첫 read 의 이름·서열·길이를 출력한다.
