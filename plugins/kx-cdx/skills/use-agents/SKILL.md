---
name: use-agents
description: 다중 에이전트 시스템으로 작업 실행. "use agents", "use agents 실행해줘", "use agents로 진행해", "에이전트 사용해서 실행" 등의 키워드로 트리거.
---

# use agents - 다중 에이전트 실행

## CRITICAL: 에이전트 Spawn 규칙
**서브에이전트를 호출하기 전 반드시 `~/plugins/kx-cdx/agents-src/_spawn-rules.md`를 읽고 따를 것.** (`subagent_type` 명시, `description` 3~5단어, `run_in_background: false`, spawn 직후 결과 검증)

플랜을 기반으로 여러 서브에이전트를 조합하여 작업을 수행한다.

## 실행 절차

### 1. 플랜 확인

- 현재 세션에 계획 문서나 승인된 작업 계획이 있는지 확인
- **플랜 있음** → 바로 에이전트 실행 (Step 3으로)
- **플랜 없음** → planner 에이전트로 계획 수립 (Step 2로)

### 2. 계획 수립 (플랜 없을 때)

로컬 Codex planner 에이전트 또는 동등한 planning workflow를 사용해 계획을 수립한다.
planner가 사용자와 소통하며 계획을 수립하고 승인을 받는다.

### 3. 에이전트 매핑

플랜의 각 작업을 담당 에이전트로 매핑:

| 작업 내용 | 에이전트 |
|----------|---------|
| 코드 구조 파악, 기존 패턴 분석 | explorer |
| 라이브러리/프레임워크 문서 확인 | explorer 또는 웹 검색 |
| API, DB, 서버 로직 개발 | backend-dev |
| 웹 페이지/컴포넌트 개발 | frontend-web-dev |
| 앱 스크린/컴포넌트 개발 | frontend-app-dev |

### 4. 의존성 분석 및 실행

`~/plugins/kx-cdx/skills/use-agents/references/AGENT_SYSTEM.md`의 실행 방법을 따른다.

**Phase 1: 탐색 (병렬 가능)**
- `explorer` + 문서 조사 동시 진행 가능

**Phase 2: 개발 (의존성 판단)**
- 독립적 작업 → 병렬 실행
- 의존적 작업 → 순차 실행

**Phase 3: 보고**
- 각 에이전트 완료 시 진행 상황 보고
- 병렬 실행 시 모든 결과 수집 후 통합 보고

### 5. 완료 보고

```markdown
## 작업 완료

### 수행된 작업
- [에이전트명]: [작업 내용]

### 생성/수정된 파일
- [파일 목록]

### 추가 작업 제안 (있다면)
- [후속 작업]
```
