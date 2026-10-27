# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 저장소 성격

생물정보학실험 수업의 학생 실습 저장소이다. 빌드, 린트, 테스트 체계는 없다. 코드는 주차별 실습 과제로 작성한 짧은 bash/Python 스크립트이며, 주석과 출력 메시지는 한국어로 쓴다. 커밋 메시지도 한국어로 짧게 쓴다 (예: `lab07 함수와 파일 저장`).

## 폴더 구조와 규칙

- `labNN/` — 주차별 작업 폴더. `lab-template/` 을 복사해서 만든다 (`cp -r lab-template lab10`).
  - `data/` 입력/생성 데이터, `doc/` 보고서·결과 요약(`.md`, `.tsv`), `src/` 직접 작성한 스크립트.
- `resources/` — 강의자가 제공한 예제 데이터(`data/`)와 스크립트(`src/`). 수정하지 않는다.
- `.devcontainer/` — Codespaces 환경 4종 (`1-basic`, `2-conda`, `3-seq`, `4-genome`). 주차에 따라 다른 이미지를 쓰며, `check.sh` 가 생성 시 설치된 도구를 보여 준다.
  - 서열 분석 도구(seqkit, blastn, mafft, iqtree, fastqc, fastp)는 `3-seq` 이상, shovill/prokka 는 `4-genome` 에만 있다. 도구가 없으면 직접 설치하지 않는다 (conda 실습 주차만 예외).
- `.gitignore` 가 FASTQ/SRA, 조립·주석 결과 폴더(`shovill_out/`, `prokka_out/` 등), FastQC 보고서를 제외한다. 대용량 시퀀싱 데이터는 커밋하지 말고 필요할 때 wget 으로 다시 받는다.

## 스크립트 실행 방식

스크립트는 해당 lab 폴더를 현재 위치로 두고 상대 경로로 실행한다.

```
$ cd lab07
$ python3 src/summary.py data/seqs.fasta doc/summary.tsv
$ bash src/check_codespace.sh      # 결과를 doc/check_result.txt 에 저장
```

- 입력/출력 파일은 `sys.argv` (bash 는 `$1`, `$2`) 로 받는 것이 관례이다.
- `src/check_codespace.sh` 는 제출용 확인 스크립트로, 경로가 `lab02` 로 고정되어 있다. 내용을 고치지 않는다.

## Python 공용 모듈 (lab07 이후)

`lab07/src/fasta.py` 가 FASTA 처리 함수(`read_fasta`, `lengths_stats`, `gc_content`, `reverse_complement`, `write_fasta`)를 모아 둔 모듈이고, 같은 폴더의 다른 스크립트가 `from fasta import ...` 로 가져다 쓴다. Python 은 스크립트가 있는 폴더를 import 경로에 넣으므로 `python3 src/xxx.py` 형태로 실행하면 된다. 새 lab 에서 재사용하려면 `fasta.py` 를 그 lab 의 `src/` 로 복사한다.

- `read_fasta` 는 헤더의 첫 단어를 이름으로, 서열은 대문자로 바꿔 `{이름: 서열}` 딕셔너리로 돌려준다.
- 알려진 문제: `lengths_stats` 는 빈 입력일 때 `min_len`/`max_len` 키를, 정상일 때 `min`/`max` 키를 돌려준다. `reverse_complement` 는 A/T/G/C 외 문자(N 등)에서 KeyError 가 난다.

각 lab 의 학습 내용 요약은 `labNN/doc/` 의 markdown 에 정리한다 (예: `lab09/doc/lab07.md`).

## 추가 규칙

- FASTA 파일은 'lab07/src/fasta.py'의 'read_fasta' 로 읽는다.
- 새 라이브러리(Biopython 등)를 쓰기 전에 먼저 물어본다.
- rm 으로 파일을 지우지 않는다.
- pip install 로 무언가를 설치하지 않는다.
- git 명령어를 실행하지 않는다.