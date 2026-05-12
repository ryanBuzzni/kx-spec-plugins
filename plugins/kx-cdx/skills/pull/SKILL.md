---
name: pull
description: 원격 브랜치 pull. 키워드(base/submodules)로 동작 분기
argument-hint: [base | submodules]
allowed-tools: Bash(git *)
disable-model-invocation: true
---

# Pull 자동화

원격 브랜치를 pull 합니다. `$ARGUMENTS` 키워드에 따라 동작이 달라집니다.

인수: $ARGUMENTS

## 동작 분기

| 인수 | 동작 |
|------|------|
| (없음) | 현재 브랜치의 최신을 원격에서 pull |
| `base` | 기본 브랜치 최신을 현재 브랜치에 병합 |
| `submodules` | `git pull --recurse-submodules` 실행 |

여러 키워드가 함께 오면 보고 후 첫 번째 매칭 모드만 수행한다.

## 수행 절차

### 0. 현재 상태 확인

병렬로 실행:
- `git status --short` → 변경 파일 (untracked 포함)
- `git branch --show-current` → 현재 브랜치명
- `git remote show origin | grep 'HEAD branch'` → 기본 브랜치명 (실패 시 `main`)

작업 디렉토리가 깨끗하지 않으면 `git stash push -u -m "pull-skill"`로 임시 저장하고, 모드 실행 후 `git stash pop`으로 복원한다.

### 1. 모드별 실행

#### 모드 A: 인수 없음 — 현재 브랜치 pull

```bash
git pull --ff-only origin [현재 브랜치명]
```

- ff-only 실패 시(로컬 커밋이 분기됨) 사용자에게 보고하고 rebase/merge 중 어느 쪽을 원하는지 확인 후 진행
- 현재 브랜치가 원격에 없으면 그 사실을 알리고 중단

#### 모드 B: `base` — 기본 브랜치 최신을 현재 브랜치에 반영

```bash
git fetch origin [기본 브랜치]
```

현재 브랜치가 기본 브랜치인 경우:

```bash
git pull --ff-only origin [기본 브랜치]
```

현재 브랜치가 기본 브랜치가 아닌 경우 (rebase 우선):

```bash
git rebase origin/[기본 브랜치]
```

- rebase 충돌 시 충돌 파일 목록을 사용자에게 보고하고 중단 (`git rebase --abort` 여부는 사용자에게 확인)

#### 모드 C: `submodules` — 서브모듈 포함 pull

```bash
git pull --recurse-submodules
```

서브모듈이 없는 저장소이면 그 사실을 알리고 일반 pull(모드 A)로 진행할지 확인한다.

### 2. stash 복원

0단계에서 stash 했다면 `git stash pop`. 충돌 시 충돌 파일 목록 보고.

### 3. 결과 보고

```
━━━━━━━━━━━━━━━━━━━━━━━━━
Pull 완료

  모드: [current | base | submodules]
  브랜치: [현재 브랜치명]
  기준: [원격 브랜치명]
  새 커밋: [N개]
  stash: [복원됨 / 없음 / 충돌]
━━━━━━━━━━━━━━━━━━━━━━━━━
```

## 주의 사항

- 강제 reset(`--hard`)은 절대 자동 수행하지 않는다.
- 충돌 발생 시 사용자의 명시적 지시 없이는 abort/skip 하지 않는다.
