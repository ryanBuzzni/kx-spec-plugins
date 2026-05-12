---
name: push-issue
description: 세션 내용을 정리해 브랜치를 만들어 push하고, 작업 내용을 GitHub Issue로 등록
argument-hint: [이슈 제목 또는 키워드]
allowed-tools: Bash(git *), Bash(gh *)
disable-model-invocation: true
---

# Push & Issue 자동화

현재 세션에서 진행한 작업을 요약하여 브랜치로 push하고, GitHub Issue로 등록합니다.

> **⚠️ CRITICAL: 모든 git/gh 명령은 반드시 현재 작업 디렉토리(pwd)에서 실행한다. 절대 `cd`로 다른 디렉토리로 이동하지 말 것.** worktree 환경에서 메인 repo로 이동하면 의도하지 않은 브랜치/경로에서 작업될 수 있음.

인수: $ARGUMENTS

## 수행 절차

### 0. refetch 실행 (인수에 "refetch"가 포함된 경우만)

`$ARGUMENTS`에 `refetch` 키워드가 포함된 경우, 작업 시작 전 최신 기본 브랜치를 받아 현재 작업에 반영한다.

수행 절차:

1. 작업 디렉토리가 깨끗하지 않으면 `git stash push -u -m "push-issue-refetch"`로 임시 저장
2. 기본 브랜치명 확인 (`git remote show origin | grep 'HEAD branch'`, 실패 시 `main`)
3. `git fetch origin [기본 브랜치]` 실행
4. 현재 브랜치가 기본 브랜치면 `git pull --ff-only origin [기본 브랜치]`
5. 현재 브랜치가 기본 브랜치가 아니면 `git rebase origin/[기본 브랜치]` 시도
   - rebase 충돌 발생 시: 사용자에게 충돌 파일 목록을 보고하고 중단. 사용자가 직접 해결 후 다시 실행하도록 안내
6. stash가 있었다면 `git stash pop`으로 복원 (충돌 시 보고)

`$ARGUMENTS`에서 `refetch` 키워드를 제거한 나머지를 이후 단계에서 이슈 제목으로 사용한다.

### 1. 세션 내용 정리

현재 세션에서 사용자와 진행한 작업/논의 내용을 다음 관점으로 정리한다:

- **무엇을 했는가** (What): 변경된 파일, 추가된 기능, 수정된 버그
- **왜 했는가** (Why): 작업 배경, 해결하려는 문제, 사용자 요청
- **어떻게 했는가** (How): 접근 방식, 주요 의사결정, 트레이드오프
- **남은 작업** (TODO): 후속 작업, 알려진 이슈, 검증 필요 항목

정리 결과는 이후 이슈 본문과 커밋 메시지에 사용한다.

### 2. 현재 상태 확인

병렬로 실행:
- `git status --short` → 변경 파일 목록 (untracked 포함)
- `git branch --show-current` → 현재 브랜치명
- `git remote show origin | grep 'HEAD branch'` → 기본 브랜치명 (실패 시 `main`)
- `git log --oneline -5` → 최근 커밋 스타일 참고
- `git diff --stat` → 변경 통계

변경사항이 전혀 없으면 사용자에게 알리고, 이슈만 등록할지 중단할지 확인한다.

### 3. 민감 파일 및 작업 무관 변경 점검

`push-pr` 스킬과 동일한 기준으로 점검:
- `.env`, `credentials.*`, `*.pem`, `*.key` 등 민감 파일은 제외
- 로컬 도메인 하드코딩, 공통 코드 의도치 않은 변경, 디버깅 코드 잔존 등 발견 시 보고 후 진행 여부 확인

### 4. 이슈 제목과 본문 결정

- **제목**: `$ARGUMENTS`에서 `refetch` 키워드를 제거한 나머지가 있으면 그것을 기반으로, 없으면 세션 정리 결과에서 한국어로 1줄 요약
  - 형식 예시: `feat(area): 짧은 요약`, `fix(area): 짧은 요약`
- **본문**: 1단계의 세션 정리 결과를 아래 템플릿에 채워 넣는다

```markdown
## 배경 (Why)
[작업 배경 및 해결하려는 문제]

## 작업 내용 (What / How)
- [주요 변경 1]
- [주요 변경 2]
- [주요 변경 3]

## 변경 파일
- `path/to/file1`
- `path/to/file2`
(최대 15개)

## 후속 작업 (TODO)
- [ ] [남은 작업 또는 검증 항목]

## 참고
- 브랜치: `[브랜치명]`
- 커밋: `[커밋 SHA]`
```

### 5. 작업 브랜치 생성

기본 브랜치와 현재 브랜치가 같으면 새 브랜치를 만든다.

- 변경 내용을 분석하여 적절한 브랜치명을 자동 생성 (예: `feat/add-login-api`, `fix/null-pointer-error`)
- 동일 이름 존재 시 숫자 suffix로 충돌 회피

```bash
git checkout -b [새 브랜치명]
```

기본 브랜치가 아니면 현재 브랜치를 그대로 사용한다.

### 6. Git Add & Commit

변경사항이 있을 때만 수행:

```bash
git add -A
git commit -m "$(cat <<'EOF'
[이슈 제목과 동일하거나 더 구체적인 커밋 메시지]

[본문 요약 1~3줄]

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>
EOF
)"
```

pre-commit hook 실패 시: 에러 보고 → 자동 수정 가능하면 새 커밋으로 재시도 (amend 금지).

### 7. Git Push

```bash
git push -u origin [현재 브랜치명]
```

### 8. GitHub Issue 등록

```bash
gh issue create --title "[이슈 제목]" --body "$(cat <<'EOF'
[4단계에서 작성한 본문]
EOF
)"
```

- 동일 제목의 열린 이슈가 이미 있으면 사용자에게 보고하고 새로 만들지/기존에 코멘트로 추가할지 확인
- 코멘트로 추가하는 경우: `gh issue comment [번호] --body ...`

라벨/담당자 지정이 필요하면 추가 옵션 사용:
- `--label "type:feature,area:backend"` 등 (저장소에 존재하는 라벨만)
- `--assignee @me`

### 9. 결과 보고

```
━━━━━━━━━━━━━━━━━━━━━━━━━
Push & Issue 완료

  브랜치: [브랜치명]
  커밋: [커밋 SHA] (변경 없으면 "없음")
  변경 파일: [N개]
  이슈: [이슈 URL]
━━━━━━━━━━━━━━━━━━━━━━━━━
```

## 주의 사항

- PR을 만들지 않는다. PR이 필요하면 `/push-pr`을 사용한다.
- 이슈 본문은 세션 맥락이 사라져도 이해 가능하도록 자기완결적으로 작성한다.
- 커밋 메시지와 이슈 본문은 한국어로 작성한다 (사용자 기본 언어).
