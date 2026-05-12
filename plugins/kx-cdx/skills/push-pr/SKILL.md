---
name: push-pr
description: Git add, commit, push (-u origin), PR create를 한 번에 수행
argument-hint: [커밋 메시지]
allowed-tools: Bash(git *), Bash(gh *)
disable-model-invocation: true
---

# Push & PR 자동화

현재 브랜치의 변경사항을 커밋, 푸시하고 PR을 생성합니다.

인수: $ARGUMENTS

## 수행 절차

다음 순서대로 작업을 수행하세요:

### 0. recap 실행 (인수에 "recap"이 포함된 경우만)

`$ARGUMENTS`에 `recap` 키워드가 포함되어 있는지 확인한다.

- **포함됨**: `/recap` 스킬을 먼저 실행하고, recap이 생성한 파일을 이후 커밋에 포함
- **포함 안 됨**: 이 단계를 건너뛰고 바로 다음 단계로 진행

`$ARGUMENTS`에서 `recap` 키워드를 제거한 나머지를 커밋 메시지로 사용한다.

### 0-B. refetch 실행 (인수에 "refetch"가 포함된 경우만)

`$ARGUMENTS`에 `refetch` 키워드가 포함된 경우, 작업 시작 전 최신 기본 브랜치를 받아 현재 작업에 반영한다.

수행 절차:

1. 작업 디렉토리가 깨끗하지 않으면 `git stash push -u -m "push-pr-refetch"`로 임시 저장
2. 기본 브랜치명 확인 (`git remote show origin | grep 'HEAD branch'`, 실패 시 `main`)
3. `git fetch origin [기본 브랜치]` 실행
4. 현재 브랜치가 기본 브랜치면 `git pull --ff-only origin [기본 브랜치]`
5. 현재 브랜치가 기본 브랜치가 아니면 `git rebase origin/[기본 브랜치]` 시도
   - rebase 충돌 발생 시: 사용자에게 충돌 파일 목록을 보고하고 중단. 사용자가 직접 해결 후 다시 실행하도록 안내
6. stash가 있었다면 `git stash pop`으로 복원 (충돌 시 보고)

`$ARGUMENTS`에서 `refetch` 키워드를 제거한 나머지를 이후 단계에서 커밋 메시지로 사용한다.

### 1. 현재 상태 확인

병렬로 실행:
- `git status --short` → 변경 파일 목록 (**untracked 파일 포함**)
- `git branch --show-current` → 현재 브랜치명
- `git remote show origin | grep 'HEAD branch'` → 기본 브랜치명 (실패 시 `main`으로 간주)
- `git log --oneline -5` → 최근 커밋 스타일 참고
- `git diff --stat` → 변경 통계

**변경사항 판단 기준** (아래 중 하나라도 해당하면 변경사항 있음):
- `git diff --stat` 출력이 있음 (tracked 파일 수정)
- `git diff --cached --stat` 출력이 있음 (staged 변경)
- `git status --short` 출력에 `??`(untracked), `A`(added) 등이 있음

위 조건에 **모두 해당하지 않을 때만** "커밋할 변경사항이 없습니다"라고 알리고 중단합니다.

### 1-B. 서브모듈 변경 감지

`git submodule status` 출력이 있으면 서브모듈이 존재하는 저장소이다.
다음 명령으로 서브모듈 변경 여부를 판단한다:

- `git submodule status` → 라인 앞에 `+`(부모 ref와 다름) 또는 `-`(미초기화) 가 붙으면 변경
- `git diff --submodule=log` / `git diff --cached --submodule=log` → 서브모듈 커밋 변경 로그
- 각 서브모듈 디렉토리에서 `git status --short` → 서브모듈 내부 작업 디렉토리 변경

서브모듈에 변경이 있으면 **서브모듈 내부에서 먼저 commit + push**를 마친 뒤 부모 저장소의 gitlink를 커밋해야 한다. 부모만 커밋하면 PR이 푸시되지 않은 SHA를 가리켜 깨진 참조가 된다. 변경된 서브모듈 목록과 처리 방향을 사용자에게 보고하고 진행 여부를 확인한다.

### 2. 민감 파일 검사

변경 파일 중 다음 패턴이 있으면 **경고 후 해당 파일 제외**:
- `.env`, `.env.*`
- `credentials.*`, `secrets.*`
- `*.pem`, `*.key`

### 3. 작업 무관 변경사항 점검

`git diff --cached` 및 `git diff`를 분석하여 다음 항목을 점검합니다.
문제가 발견되면 **해당 내용을 사용자에게 보고하고 진행 여부를 확인**합니다.

#### 점검 항목

**로컬 환경 값 유출**
- `0.0.0.0`, `127.0.0.1`, `localhost` 등 로컬 도메인/IP가 코드에 하드코딩된 경우
- 예: `http://0.0.0.0:8000`, `http://localhost:3000`
- 설정 파일(`config`, `settings`, `.env.example`)이나 테스트 코드에서의 사용은 허용

**공통 코드 의도치 않은 변경**
- `APIRouter()` 파라미터 변경 (prefix, tags 등)
- 공통 미들웨어, 의존성 주입 함수 변경
- `__init__.py`의 export 변경
- 예: `APIRouter(prefix="/v1/subscriptions")` → `APIRouter(prefix="/v1/subs")` 같은 변경

**설정/인프라 파일 의도치 않은 변경**
- `alembic.ini`, `pyproject.toml`, `requirements.txt`, `Dockerfile` 등 설정 파일이 변경된 경우
- 현재 작업과 관련 없는 설정 변경이면 경고

**Vercel 호스트 리다이렉트 충돌**
- `next.config.mjs`에 호스트 기반 리다이렉트(예: `www → non-www`)가 추가/변경된 경우 경고
- Vercel은 도메인 설정에서 www 리다이렉트를 처리하므로 next.config에 넣으면 무한 리다이렉트 발생

**디버깅 코드 잔존**
- `print()`, `console.log()`, `breakpoint()`, `pdb.set_trace()` 등 디버깅 코드
- 주석 처리된 코드 블록 추가 (`# TODO`, `# FIXME`는 허용)

#### 점검 결과 보고 형식

문제 발견 시:
```
⚠️ 작업 무관 변경사항 감지

1. [파일명:라인] 로컬 도메인 사용 → 0.0.0.0:8000
2. [파일명:라인] APIRouter prefix 변경 → 다른 API에 영향 가능
3. [파일명:라인] print() 디버깅 코드 잔존

계속 진행하시겠습니까? (이 변경사항들이 의도된 것이라면 진행)
```

문제 없으면 다음 단계로 진행합니다.

### 4. 커밋 메시지 결정

- `$ARGUMENTS`에서 `recap`, `merge`, `refetch` 키워드를 제거한 나머지를 커밋 메시지로 사용
- 커밋 메시지가 비어있으면 변경 내용을 분석하여 한국어로 자동 생성
  - 변경 유형 파악 (feat/fix/refactor/docs/chore 등)
  - 변경 핵심을 1~2문장으로 요약

### 5. 기본 브랜치 작업 여부 확인

기본 브랜치와 현재 브랜치가 같으면 새 작업 브랜치를 만든 뒤 그 브랜치에서 계속 진행합니다.

- 브랜치명은 `codex/` 접두사를 사용하고, 커밋 메시지 또는 변경 내용을 기반으로 짧은 slug를 생성합니다.
- 예: `codex/nexus-answer-meta`, `codex/fix-login-copy`
- 이미 같은 이름의 브랜치가 있으면 뒤에 숫자를 붙여 충돌을 피합니다.

실행 예시:

```bash
git checkout -b [새 브랜치명]
```

기본 브랜치와 현재 브랜치가 다르면 이 단계는 건너뜁니다.

### 6. Git Add

```bash
git add -A
```

### 7. Git Commit

HEREDOC 형식으로 커밋:
```bash
git commit -m "$(cat <<'EOF'
[커밋 메시지]

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>
EOF
)"
```

커밋 실패(pre-commit hook 등) 시:
- 에러 내용을 사용자에게 보고
- 자동 수정 가능하면 수정 후 **새 커밋** 시도 (amend 금지)
- 자동 수정 불가하면 중단

### 8. Git Push

```bash
git push -u origin [현재 브랜치명]
```

### 9. PR 생성

기본 브랜치를 자동 감지합니다:
- `git remote show origin | grep 'HEAD branch'`로 확인
- 실패 시 `main` 사용

`gh pr create` 실행:
```bash
gh pr create --title "[커밋 메시지]" --body "$(cat <<'EOF'
## Summary
[변경 내용 요약 - 1~3개 bullet points]

## Changes
[변경된 파일 목록 - 최대 15개]

## Test plan
- [ ] 빌드 확인
- [ ] 기능 동작 확인

Generated with Codex
EOF
)"
```

이미 PR이 존재하면 기존 PR URL을 표시합니다.

### 10. PR 머지 (인수에 "merge"가 포함된 경우만)

`$ARGUMENTS`에 `merge` 키워드가 포함된 경우:

```bash
gh pr merge --squash --delete-branch
```

- squash merge로 진행
- 머지 후 원격 브랜치 자동 삭제
- 머지 실패 시 에러 보고 (CI 미통과, 리뷰 필요 등)

### 11. 결과 보고

```
━━━━━━━━━━━━━━━━━━━━━━━━━
Push & PR 완료

  브랜치: [브랜치명]
  커밋: [커밋 메시지]
  변경 파일: [N개]
  PR: [PR URL]
  머지: [완료 / 미실행]
━━━━━━━━━━━━━━━━━━━━━━━━━
```
