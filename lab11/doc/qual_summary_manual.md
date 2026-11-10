# qual_summary.py 사용법 및 설명서

## 1. 개요

`src/qual_summary.py` 는 FASTQ 파일을 읽어 read 마다 평균 품질 점수(Phred score)를 구한 뒤, 모든 read 의 평균 품질을 다시 평균 내어 하나의 값으로 출력하는 Python 스크립트이다. 외부 라이브러리 없이 Python 표준 기능(`sys`)만 사용한다.

## 2. 실행 방법

`lab11` 폴더를 현재 위치로 두고 상대 경로로 실행한다.

```
$ cd lab11
$ python3 src/qual_summary.py data/SRR1553607_1.fastq
```

| 인자 | 설명 |
|------|------|
| `sys.argv[1]` | 읽을 FASTQ 파일 경로 (필수) |

결과는 화면(표준 출력)에만 나온다. 파일로 저장하려면 리다이렉션을 쓴다.

```
$ python3 src/qual_summary.py data/SRR1553607_1.fastq > doc/qual_result.txt
```

## 3. 실행 예시

`data/` 의 paired-end 파일 두 개로 실행한 실제 결과이다.

```
$ python3 src/qual_summary.py data/SRR1553607_1.fastq
전체 read 평균 품질: 33.4497222958299

$ python3 src/qual_summary.py data/SRR1553607_2.fastq
전체 read 평균 품질: 30.830840894308746
```

| 파일 | read 수 | 전체 read 평균 품질 |
|------|---------|---------------------|
| SRR1553607_1.fastq (forward) | 203,445 | 약 33.45 |
| SRR1553607_2.fastq (reverse) | 203,445 | 약 30.83 |

일반적으로 Illumina 의 두 번째 read(_2)는 첫 번째 read(_1)보다 품질이 조금 낮게 나오며, 이 결과도 그 경향과 일치한다. 두 값 모두 Q30 이상이다.

## 4. 배경 지식: Phred 품질 점수

FASTQ 의 4번째 줄은 염기마다 품질 점수를 문자 하나로 기록한다. 현재 쓰이는 Phred+33 방식에서는 다음과 같이 계산한다.

```
품질 점수 Q = (문자의 ASCII 코드) - 33
오류 확률 P = 10 ^ (-Q / 10)
```

| 문자 | ASCII | Q | 오류 확률 |
|------|-------|---|-----------|
| `+` | 43 | 10 | 1/10 (90% 정확) |
| `5` | 53 | 20 | 1/100 (99% 정확) |
| `?` | 63 | 30 | 1/1,000 (99.9% 정확) |
| `J` | 74 | 41 | 약 1/12,600 |

예를 들어 첫 번째 read 의 품질 줄 `BB@FFFFFHHHHHJJJ...` 에서 `B` 는 33, `@` 는 31, `F` 는 37, `H` 는 39, `J` 는 41 이다. 이 read(길이 101)의 평균 품질은 약 37.44 이다.

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

`parse_fastq.py` 의 함수와 같다. 파일 전체를 읽어 4줄씩 끊고, `(이름, 서열, 품질)` 튜플의 리스트를 돌려준다.

| 단계 | 내용 |
|------|------|
| `f.readlines()` | 파일 전체를 줄 단위 리스트로 읽는다. |
| `range(0, len(lines), 4)` | 4줄씩 건너뛰며 각 read 의 첫 줄 위치를 얻는다. |
| `lines[i].rstrip()[1:]` | 맨 앞 `@` 를 뺀 헤더를 이름으로 쓴다. |
| `lines[i + 1]` / `lines[i + 3]` | 서열 줄 / 품질 줄 (`+` 줄은 건너뛴다) |

### 5.2 `mean_quality(qual)` 함수

```python
def mean_quality(qual):
    scores = []
    for ch in qual:
        scores.append(ord(ch) - 33)
    return sum(scores) / len(scores)
```

| 단계 | 내용 |
|------|------|
| `for ch in qual` | 품질 문자열의 문자를 하나씩 꺼낸다. |
| `ord(ch) - 33` | 문자를 ASCII 코드로 바꾼 뒤 33 을 빼서 Phred 점수로 만든다. |
| `sum(scores) / len(scores)` | 그 read 의 염기별 점수 평균을 돌려준다. |

### 5.3 메인 부분

```python
reads = read_fastq(sys.argv[1])

total = 0
for name, seq, qual in reads:
    q = mean_quality(qual)
    total = total + q

print("전체 read 평균 품질:", total / len(reads))
```

- 모든 read 에 대해 `mean_quality` 로 read 평균 품질을 구하고 `total` 에 더한다.
- 마지막에 `total` 을 read 개수로 나누어 "read 평균 품질들의 평균" 을 출력한다.
- `name`, `seq` 는 꺼내기만 하고 사용하지 않는다.

## 6. 결과 해석 시 주의점

출력값은 "read 별 평균의 평균" 이다. 모든 염기를 한꺼번에 평균 낸 값과는 read 길이가 서로 다를 때 달라진다. 짧은 read 와 긴 read 가 같은 비중으로 계산되기 때문이다. 이번 데이터는 모든 read 의 길이가 101 로 같으므로 두 값이 같다.

또한 평균 하나만으로는 read 끝부분의 품질 저하나 품질이 낮은 일부 read 를 알 수 없다. 위치별 품질 분포는 FastQC 같은 도구로 확인하는 것이 좋다.

## 7. 주의 사항 및 한계

| 상황 | 결과 |
|------|------|
| 인자 없이 실행 | `IndexError: list index out of range` (`sys.argv[1]` 없음) |
| 없는 파일 경로 | `FileNotFoundError` |
| 빈 파일 | `total / len(reads)` 에서 `ZeroDivisionError` |
| 품질 줄이 빈 read | `mean_quality` 에서 `ZeroDivisionError` |
| 줄 수가 4의 배수가 아님 | 마지막 불완전한 read 에서 `IndexError` |
| Phred+64 인코딩(오래된 Illumina) | 점수가 31 만큼 높게 계산됨 |
| `.fastq.gz` 압축 파일 | 그대로 읽을 수 없음 (먼저 `gunzip` 필요) |
| 큰 파일 | `readlines()` 와 records 리스트가 파일 전체를 메모리에 올림 |

- 메인 부분이 `if __name__ == "__main__":` 아래에 있지 않으므로, 다른 스크립트에서 이 파일의 함수를 import 하면 메인 코드도 함께 실행된다.

## 8. 요약

- 사용법: `python3 src/qual_summary.py <FASTQ 파일>`
- 품질 문자를 `ord(문자) - 33` 으로 Phred 점수로 바꾼다.
- read 별 평균 품질을 구한 뒤, 그 평균을 다시 평균 내어 출력한다.
- 예시 결과: _1 파일 약 33.45, _2 파일 약 30.83
