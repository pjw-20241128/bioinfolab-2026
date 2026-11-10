# qual_by_position.py 사용법 및 설명서

## 1. 개요

`src/qual_by_position.py` 는 FASTQ 파일의 모든 read 에서 같은 위치(1번째 염기, 2번째 염기, …)의 품질 점수를 모아 위치별 평균을 계산하고, 위치와 평균 품질을 탭으로 구분하여 출력하는 Python 스크립트이다. 이것은 FastQC 의 **Per base sequence quality** 그래프가 계산하는 평균값(그래프의 파란 선)과 같은 값이다. 외부 라이브러리 없이 Python 표준 기능(`sys`)만 사용한다.

## 2. 실행 방법

`lab11` 폴더를 현재 위치로 두고 상대 경로로 실행한다.

```
$ cd lab11
$ python3 src/qual_by_position.py data/SRR1553607_1.fastq
```

| 인자 | 설명 |
|------|------|
| `sys.argv[1]` | 읽을 FASTQ 파일 경로 (필수) |

결과는 화면(표준 출력)에 나온다. 탭으로 구분되어 있으므로 리다이렉션으로 `.tsv` 파일에 저장하면 엑셀이나 다른 스크립트에서 바로 쓸 수 있다.

```
$ python3 src/qual_by_position.py data/SRR1553607_1.fastq > doc/qual_by_position_1.tsv
```

## 3. 출력 형식

첫 줄은 열 이름이고, 그 다음 줄부터 위치마다 한 줄씩 출력한다. 위치는 1부터 세고, 평균 품질은 소수점 둘째 자리까지 표시한다.

```
position	mean_quality
1	32.04
2	32.17
3	32.28
...
101	28.25
```

| 열 | 내용 |
|----|------|
| `position` | read 안에서의 염기 위치 (1부터 시작) |
| `mean_quality` | 그 위치에 있는 모든 염기의 Phred 품질 점수 평균 |

## 4. 실행 예시

`data/` 의 세 파일로 실행한 실제 결과 중 일부이다 (모두 read 길이 최대 101, 출력 101줄 + 열 이름 1줄).

| 위치 | SRR1553607_1 | SRR1553607_2 | trimmed |
|------|--------------|--------------|---------|
| 1 | 32.04 | 30.03 | 32.28 |
| 2 | 32.17 | 30.02 | 32.41 |
| 3 | 32.28 | 30.25 | 32.52 |
| 4 | 35.85 | 33.72 | 36.07 |
| 9 | 37.27 | 35.07 | 37.63 |
| 14 (최고) | 38.47 | 36.12 | 38.93 |
| 99 | 29.03 | 26.46 | 31.03 |
| 100 | 28.93 | 26.34 | 30.92 |
| 101 | 28.25 | 25.78 | 30.17 |
| 평균이 30 미만인 위치 수 | 15 | 48 | 0 |

- 세 파일 모두 처음 몇 염기는 품질이 약간 낮고, 10~20번째 부근에서 가장 높으며, read 끝으로 갈수록 품질이 떨어진다. 이것이 Illumina 데이터의 전형적인 모양이다.
- reverse read(`_2`)는 forward read(`_1`)보다 전 구간에서 약 2 정도 낮고, 평균이 30 미만인 위치가 48개로 훨씬 많다.
- fastp 로 품질 트리밍한 `trimmed.fastq` 는 마지막 위치까지 평균이 30 이상으로 유지된다.

## 5. FastQC 결과와 비교

`doc/SRR1553607_1_fastqc.zip` 안의 `fastqc_data.txt` 에서 Per base sequence quality 모듈의 `Mean` 열을 보면 아래와 같다.

```
$ unzip -p doc/SRR1553607_1_fastqc.zip '*/fastqc_data.txt' \
    | sed -n '/Per base sequence quality/,/END_MODULE/p' | cut -f1,2 | head -6
>>Per base sequence quality	pass
#Base	Mean
1	32.04065963773993
2	32.170788173707884
3	32.2813094448131
4	35.849885718498854
```

이 스크립트의 출력(32.04, 32.17, 32.28, 35.85)과 같다. 단, FastQC 는 read 가 길면 10번째 위치부터 `10-11`, `12-13` 처럼 위치를 묶어서 그 구간의 평균을 보여 준다. 이 스크립트는 묶지 않고 모든 위치를 하나씩 출력하므로, 10번째 이후는 이 스크립트의 두 위치 값을 평균 내야 FastQC 의 값과 같아진다.

## 6. 배경 지식: Phred 품질 점수

FASTQ 의 4번째 줄은 염기마다 품질 점수를 문자 하나로 기록한다. Phred+33 방식에서는 다음과 같이 계산한다.

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

## 7. 코드 설명

### 7.1 `read_fastq(filename)` 함수

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

`parse_fastq.py`, `qual_summary.py` 의 함수와 같다. 파일을 4줄씩 끊어 `(이름, 서열, 품질)` 튜플의 리스트를 돌려준다.

### 7.2 `quality_by_position(reads)` 함수

```python
def quality_by_position(reads):
    totals = []
    counts = []
    for name, seq, qual in reads:
        for i, ch in enumerate(qual):
            q = ord(ch) - 33
            if i == len(totals):
                totals.append(0)
                counts.append(0)
            totals[i] = totals[i] + q
            counts[i] = counts[i] + 1
    means = []
    for i in range(len(totals)):
        means.append(totals[i] / counts[i])
    return means
```

| 단계 | 내용 |
|------|------|
| `totals`, `counts` | 위치별 품질 점수의 합과, 그 위치에 염기가 있는 read 의 수를 담는 리스트 |
| `enumerate(qual)` | 품질 문자열에서 위치 `i`(0부터)와 문자 `ch` 를 함께 꺼낸다. |
| `ord(ch) - 33` | 문자를 Phred 점수로 바꾼다. |
| `if i == len(totals)` | 지금까지 본 read 보다 긴 위치가 나오면 리스트에 칸을 하나 늘린다. |
| `totals[i] / counts[i]` | 위치마다 합을 개수로 나누어 평균을 구한다. |

`counts` 를 위치마다 따로 세기 때문에 read 길이가 서로 달라도 정확하게 계산된다. 예를 들어 `trimmed.fastq` 는 read 길이가 50~101 로 다양한데, 80번째 위치의 평균은 길이가 80 이상인 read 만으로 계산된다. FastQC 도 같은 방식이다.

### 7.3 메인 부분

```python
if __name__ == "__main__":
    reads = read_fastq(sys.argv[1])
    means = quality_by_position(reads)

    print("position\tmean_quality")
    for i, m in enumerate(means):
        print(f"{i + 1}\t{m:.2f}")
```

- 열 이름을 먼저 출력하고, 위치마다 `위치<TAB>평균` 을 출력한다. `\t` 가 탭 문자이다.
- 리스트 인덱스는 0부터 시작하므로 `i + 1` 로 바꾸어 위치를 1부터 표시한다.
- `{m:.2f}` 는 소수점 둘째 자리까지 반올림하여 표시한다.
- `if __name__ == "__main__":` 아래에 두었으므로, 다른 스크립트에서 `from qual_by_position import quality_by_position` 으로 함수만 가져다 쓸 수 있다.

## 8. 주의 사항 및 한계

| 상황 | 결과 |
|------|------|
| 인자 없이 실행 | `IndexError: list index out of range` (`sys.argv[1]` 없음) |
| 없는 파일 경로 | `FileNotFoundError` |
| 빈 파일 | 열 이름 한 줄만 출력된다. |
| 줄 수가 4의 배수가 아님 | 마지막 불완전한 read 에서 `IndexError` |
| Phred+64 인코딩(오래된 Illumina) | 점수가 31 만큼 높게 계산됨 |
| `.fastq.gz` 압축 파일 | 그대로 읽을 수 없음 (먼저 `gunzip` 필요) |
| 큰 파일 | `readlines()` 와 records 리스트가 파일 전체를 메모리에 올림 |

- 평균만 계산하므로 FastQC 그래프의 상자(사분위수)나 수염(10%/90%)은 알 수 없다. 평균이 높아도 일부 read 의 품질이 매우 낮을 수 있다.
- read 길이가 다를 때 끝부분 위치는 소수의 긴 read 로만 계산되므로, 그 값은 신뢰도가 낮다.

## 9. 요약

- 사용법: `python3 src/qual_by_position.py <FASTQ 파일> > 결과.tsv`
- 위치별로 품질 점수의 합과 개수를 모아 평균을 낸다.
- 출력은 `position<TAB>mean_quality` 형식이며, FastQC Per base sequence quality 의 `Mean` 값과 같다.
- 예시 결과: `_1` 파일은 14번째에서 최고 38.47, 101번째에서 28.25 로 끝부분 품질이 떨어진다.
