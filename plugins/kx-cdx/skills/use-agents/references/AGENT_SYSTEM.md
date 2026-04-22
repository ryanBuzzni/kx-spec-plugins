# KX Codex Agent System

KX Codex 워크플로우는 두 종류의 에이전트를 함께 사용한다.

- **Codex 기본 에이전트**: `explorer`, `worker`, `default`
- **KX 커스텀 에이전트**: `planner`, `backend-dev`, `frontend-web-dev`, `frontend-app-dev`, `debugger`, `code-reviewer`, `back-tester`, `web-tester`, `app-tester`

## 설치 위치

- 커스텀 에이전트 source: `~/plugins/kx-cdx/agents-src/*.toml`
- 로컬 설치 위치: `~/.codex/agents/*.toml`
- 동기화 명령:

```bash
python3 ~/plugins/kx-cdx/scripts/sync_agents.py
```

## 사용 원칙

1. 코드베이스 탐색은 기본 `explorer` 에이전트를 우선 사용한다.
2. 실제 구현/리뷰/테스트는 KX 커스텀 에이전트를 사용한다.
3. 독립 작업은 병렬로, 의존 작업은 순차로 실행한다.
4. 스킬 문서에서 언급하는 에이전트 이름은 아래 이름과 정확히 일치해야 한다.

## 권장 매핑

| 작업 | 사용할 에이전트 |
|------|----------------|
| 코드 구조 탐색 | `explorer` |
| 계획 수립 | `planner` |
| 백엔드 개발 | `backend-dev` |
| 웹 프론트 개발 | `frontend-web-dev` |
| 앱 프론트 개발 | `frontend-app-dev` |
| 디버깅 | `debugger` |
| 코드 리뷰 | `code-reviewer` |
| 백엔드 테스트 | `back-tester` |
| 웹 E2E 테스트 | `web-tester` |
| 앱 UI 테스트 | `app-tester` |

## 실행 예시

### 단일 작업

```text
Have backend-dev implement the API changes from specs/20260422-foo/spec.md and plan.md.
```

### 탐색 후 구현

```text
Have explorer map the affected code paths first, then have frontend-web-dev implement the approved UI changes.
```

### 병렬 작업

```text
Have backend-dev implement the API updates and frontend-web-dev prepare the dependent UI work in parallel if they are independent.
```

## 설치 확인

다음 파일이 모두 존재하면 설치가 완료된 상태로 본다.

- `~/.codex/agents/planner.toml`
- `~/.codex/agents/backend-dev.toml`
- `~/.codex/agents/frontend-web-dev.toml`
- `~/.codex/agents/frontend-app-dev.toml`
- `~/.codex/agents/debugger.toml`
- `~/.codex/agents/code-reviewer.toml`
- `~/.codex/agents/back-tester.toml`
- `~/.codex/agents/web-tester.toml`
- `~/.codex/agents/app-tester.toml`
