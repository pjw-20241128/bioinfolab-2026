# gc_content.py 사용법 및 설명서

## 1. 개요

`src/gc_content.py` 는 FASTQ 파일의 각 read 에 대해 GC 비율과 평균 품질을 함께 계산하는 Python 스크립트이다. GC 비율이 극단적인 read 를 양쪽에서 열 개씩, 즉 **GC 비율이 가장 높은 read 10개**와 **가장 낮은 read 10개**를 골라, 각 그룹의 평균 품질이 전체 평균과 얼마나 차이 나는지 출력한다. 외부 라이브러리 없이 Python 표준 기능(`sys`)만 사용한다.

## 2. 실행 방법

`lab11` 폴더를 현재 위치로 두고 상대 경로로 실행한다.

```
$ cd lab11
$ python3 src/gc_content.py data/SRR1553607_1.fastq
```

| 인자 | 설명 |
|------|------|
| `sys.argv[1]` | 읽을 FASTQ 파일 경로 (필수) |

결과는 화면(표준 출력)에 나온다. 파일로 저장하려면 리다이렉션을 쓴다.

```
$ python3 src/gc_content.py data/SRR1553607_1.fastq > doc/gc_result_1.txt
```

고를 read 수는 스크립트 위쪽의 `N_PICK = 10` 을 바꾸면 조정할 수 있다.

## 3. 출력 형식

출력은 세 부분으로 되어 있다.

| 부분 | 내용 |
|------|------|
| 전체 요약 | 전체 read 수, 전체 평균 GC 비율, 전체 평균 품질 |
| GC 가 가장 높은 read 10개 | GC 비율이 높은 순서로 `이름<TAB>GC 비율<TAB>평균 품질`, 마지막 줄에 그룹 평균 품질과 전체 평균과의 차이 |
| GC 가 가장 낮은 read 10개 | GC 비율이 낮은 순서로 같은 형식 |

- GC 비율은 0~1 사이의 값으로 소수점 셋째 자리까지, 품질은 둘째 자리까지 표시한다.
- 차이는 `그룹 평균 - 전체 평균` 이며, 부호(`+`/`-`)를 항상 붙인다. `-` 이면 그 그룹의 품질이 전체보다 낮다는 뜻이다.
- read 이름은 헤더의 첫 단어만 쓴다 (예: `@SRR1553607.53820 53820 length=101` → `SRR1553607.53820`).

## 4. 실행 예시

`data/SRR1553607_1.fastq` 로 실행한 실제 결과이다.

```
$ python3 src/gc_content.py data/SRR1553607_1.fastq
전체 read 수: 203445
전체 평균 GC 비율: 0.588
전체 평균 품질: 33.45

## GC 비율이 가장 높은 read 10개
name	gc	mean_quality
SRR1553607.53820	0.980	11.10
SRR1553607.169331	0.950	19.73
SRR1553607.143780	0.941	9.25
SRR1553607.77585	0.941	9.06
SRR1553607.194620	0.931	17.33
SRR1553607.169682	0.931	32.28
SRR1553607.106561	0.931	24.01
SRR1553607.195126	0.921	34.17
SRR1553607.185657	0.921	10.21
SRR1553607.176568	0.921	5.75
그룹 평균 품질: 17.29 (전체 평균과 차이: -16.16)

## GC 비율이 가장 낮은 read 10개
name	gc	mean_quality
SRR1553607.166164	0.129	39.66
SRR1553607.165570	0.139	38.32
SRR1553607.179986	0.139	38.09
SRR1553607.59968	0.158	39.58
SRR1553607.61985	0.158	33.28
SRR1553607.70984	0.158	39.22
SRR1553607.117728	0.158	39.27
SRR1553607.117814	0.158	37.28
SRR1553607.166721	0.158	40.11
SRR1553607.172662	0.158	38.46
그룹 평균 품질: 38.33 (전체 평균과 차이: +4.88)
```

세 파일의 결과를 정리하면 다음과 같다.

| 파일 | 전체 평균 GC | 전체 평균 품질 | GC 높은 10개 평균 품질 (차이) | GC 낮은 10개 평균 품질 (차이) |
|------|------|------|------|------|
| SRR1553607_1 | 0.588 | 33.45 | 17.29 (-16.16) | 38.33 (+4.88) |
| SRR1553607_2 | 0.592 | 30.83 | 4.65 (-26.18) | 36.51 (+5.68) |
| trimmed | 0.589 | 34.95 | 32.02 (-2.93) | 38.46 (+3.51) |

## 5. 결과 해석

**GC 비율이 극단적으로 높은 read 는 품질이 크게 낮다.** `_1` 에서는 전체보다 약 16, `_2` 에서는 약 26 낮다. 이런 read 를 직접 열어 보면 원인을 알 수 있다.

```
@SRR1553607.199211 199211 length=101
GCCCCGGCCCCCCGCCCCCCCGGGGCCGGGGGCGGGGGACGCGCCCCGCCGCCGCCCCCCCCCCGCGCC...
+SRR1553607.199211 199211 length=101
#####################################################################...
```

- 품질 문자 `#` 은 Q2 로, Illumina 가 "이 부분부터는 믿을 수 없음" 을 표시할 때 쓰는 값이다. 이 read(`_2` 파일)는 101개 염기 전체가 Q2 이다.
- 시퀀싱이 실패한 구간에서는 G 나 C 가 연속으로 잘못 읽히는 경우가 많다. 그래서 "GC 비율이 비정상적으로 높다" 는 것 자체가 품질이 나쁜 read 의 신호가 된다.
- reverse read(`_2`)가 forward read(`_1`)보다 이런 read 가 많아 차이가 더 크다.

**GC 비율이 극단적으로 낮은 read 는 오히려 품질이 전체 평균보다 약간 높다.** 세 파일 모두 +3.5 ~ +5.7 정도이다.

**fastp 로 트리밍한 `trimmed.fastq` 에서는 차이가 크게 줄어든다** (-2.93). 품질이 낮은 끝부분과 read 가 제거되어, 남은 high-GC read 는 대부분 품질이 정상 범위이다.

## 6. 배경 지식

### 6.1 GC 비율

```
GC 비율 = (G 의 개수 + C 의 개수) / 서열 길이
```

예를 들어 `ATGCGC` 는 G 2개, C 2개이므로 4 / 6 = 0.667 이다. 이 데이터의 전체 평균 GC 비율은 약 0.59 이다.

### 6.2 Phred 품질 점수

FASTQ 의 4번째 줄은 염기마다 품질 점수를 문자 하나로 기록한다 (Phred+33).

```
품질 점수 Q = (문자의 ASCII 코드) - 33
```

| 문자 | ASCII | Q | 의미 |
|------|-------|---|------|
| `#` | 35 | 2 | 믿을 수 없는 염기 |
| `+` | 43 | 10 | 정확도 90% |
| `?` | 63 | 30 | 정확도 99.9% |
| `J` | 74 | 41 | 매우 높은 품질 |

## 7. 코드 설명

### 7.1 `read_fastq(filename)` 함수

`parse_fastq.py`, `qual_summary.py` 의 함수와 같다. 파일을 4줄씩 끊어 `(이름, 서열, 품질)` 튜플의 리스트를 돌려준다.

### 7.2 `gc_ratio(seq)` 함수

```python
def gc_ratio(seq):
    seq = seq.upper()
    gc = seq.count("G") + seq.count("C")
    return gc / len(seq)
```

서열을 대문자로 바꾼 뒤 `count()` 로 G 와 C 의 개수를 세고 서열 길이로 나눈다. N 도 분모(길이)에는 포함된다.

### 7.3 `mean_quality(qual)` 함수

```python
def mean_quality(qual):
    scores = []
    for ch in qual:
        scores.append(ord(ch) - 33)
    return sum(scores) / len(scores)
```

`qual_summary.py` 의 함수와 같다. 품질 문자를 `ord(ch) - 33` 으로 점수로 바꾼 뒤 평균을 낸다.

### 7.4 `group_mean(rows)`, `print_group(...)` 함수

```python
def group_mean(rows):
    total = 0
    for name, gc, q in rows:
        total = total + q
    return total / len(rows)
```

`(이름, GC 비율, 평균 품질)` 목록을 받아 평균 품질의 평균을 돌려준다. `print_group` 은 한 그룹의 read 목록과 그룹 평균, 전체 평균과의 차이(`{m - overall:+.2f}`, `+` 는 부호를 항상 표시)를 출력한다.

### 7.5 메인 부분

```python
reads = read_fastq(sys.argv[1])

rows = []
for name, seq, qual in reads:
    rows.append((name.split()[0], gc_ratio(seq), mean_quality(qual)))

overall_gc = sum(r[1] for r in rows) / len(rows)
overall_q = group_mean(rows)

rows_sorted = sorted(rows, key=lambda r: r[1])
low = rows_sorted[:N_PICK]
high = rows_sorted[-N_PICK:][::-1]
```

| 단계 | 내용 |
|------|------|
| `rows.append(...)` | read 마다 `(이름 첫 단어, GC 비율, 평균 품질)` 을 저장한다. |
| `overall_gc`, `overall_q` | 모든 read 의 GC 비율 평균과 평균 품질의 평균 |
| `sorted(rows, key=lambda r: r[1])` | GC 비율(`r[1]`)을 기준으로 오름차순 정렬한다. |
| `rows_sorted[:N_PICK]` | 앞에서 10개 = GC 비율이 가장 낮은 read |
| `rows_sorted[-N_PICK:][::-1]` | 뒤에서 10개를 뒤집어 GC 비율이 높은 순서로 만든다. |

메인 부분은 `if __name__ == "__main__":` 아래에 있으므로, 다른 스크립트에서 `from gc_content import gc_ratio` 처럼 함수만 가져다 쓸 수 있다.

## 8. 주의 사항 및 한계

| 상황 | 결과 |
|------|------|
| 인자 없이 실행 | `IndexError: list index out of range` (`sys.argv[1]` 없음) |
| 없는 파일 경로 | `FileNotFoundError` |
| 빈 파일 | `ZeroDivisionError` (read 가 0개) |
| 길이가 0인 read | `gc_ratio` 에서 `ZeroDivisionError` |
| 줄 수가 4의 배수가 아님 | 마지막 불완전한 read 에서 `IndexError` |
| `.fastq.gz` 압축 파일 | 그대로 읽을 수 없음 (먼저 `gunzip` 필요) |
| 큰 파일 | 파일 전체와 모든 read 의 결과를 메모리에 올림 |

- GC 비율이 같은 read 가 여럿이면 어느 read 가 10개 안에 들지는 파일 안의 순서에 따라 정해진다.
- 10개씩만 비교하므로 우연의 영향을 받는다. 차이가 통계적으로 의미 있는지는 이 스크립트로 판단할 수 없다. 더 확실히 보려면 `N_PICK` 을 늘리거나 GC 비율 구간별로 평균 품질을 구해 본다.
- `lab07/src/fasta.py` 의 `gc_content` 는 FASTA 용이므로 여기서는 쓰지 않고 FASTQ read 용 `gc_ratio` 를 따로 만들었다.

## 9. 요약

- 사용법: `python3 src/gc_content.py <FASTQ 파일>`
- read 마다 GC 비율과 평균 품질을 계산하고, GC 비율 양 극단의 read 10개씩을 전체 평균 품질과 비교한다.
- 예시 결과(`_1`): GC 높은 10개는 17.29 로 전체(33.45)보다 16.16 낮고, GC 낮은 10개는 38.33 으로 4.88 높다.
- GC 비율이 비정상적으로 높은 read 는 시퀀싱 오류로 생긴 저품질 read 일 가능성이 크다.
