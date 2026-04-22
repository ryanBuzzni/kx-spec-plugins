# KX Codex Workflow

## 기본 흐름

1. `spec-plan` 또는 `planner`로 계획을 확정한다.
2. `spec-write`로 `spec.md`, `plan.md`, `context.md`를 만든다.
3. `spec-execute`, `use-dev`, `use-agents`로 구현을 진행한다.
4. `spec-testing`과 `spec-code-review`로 검증한다.

## 명령 조합 예시

### 계획 수립

```text
Use planner to turn the current request into an implementation plan with approval checkpoints.
```

### 문서 생성

```text
Use spec-write to create spec.md, plan.md, and context.md from the approved plan.
```

### 개발 실행

```text
Use use-dev for a single-domain implementation.
Use use-agents when work should be split across multiple agents.
```

### 검증

```text
Use spec-testing back
Use spec-testing web
Use spec-code-review
```

## 운영 규칙

- `explorer`는 탐색 전용으로 사용한다.
- KX 커스텀 에이전트는 구현, 리뷰, 테스트 역할에 집중시킨다.
- `specs/` 문서가 있으면 항상 그 문서를 우선 컨텍스트로 사용한다.
- 변경 후에는 관련 테스트, 타입체크, 린트 순으로 검증한다.
