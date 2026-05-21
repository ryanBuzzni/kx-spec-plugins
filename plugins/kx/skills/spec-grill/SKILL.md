---
name: spec-grill
description: TDD 워크플로우 진입점. grill-me 스킬로 결정 트리를 끝까지 파고들어 의사결정을 정리한 뒤, 자동으로 `/kx:spec-write --skip-confirm --workflow=tdd`로 이어진다. "spec grill", "스펙 그릴", "그릴미 스펙", "tdd 시작", "/kx:spec-grill" 등으로 트리거.
---

# Spec Grill: TDD 워크플로우 진입점

기능 구현 전 사용자 의사결정을 인터뷰로 끌어내고, 곧바로 스펙 문서 작성 → TDD 구현 → 코드 리뷰로 자동 연결한다.

> **전체 흐름**: `kx:spec-grill → kx:spec-write → kx:spec-tdd → kx:spec-code-review`

---

## 1. 인터뷰 단계 — grill-me 적용

`~/.claude/skills/grill-me/SKILL.md`의 원칙을 그대로 적용한다:

- **한 번에 하나의 질문**
- 각 질문마다 **추천 답변**을 함께 제시 (사용자가 단순 승인만으로 진행 가능하도록)
- 코드베이스 탐색으로 답할 수 있는 질문은 **직접 탐색** (Serena MCP 우선)
- 결정 트리의 모든 분기가 해소될 때까지 반복

### 반드시 다루어야 할 분기

다음 항목이 결정되지 않았다면 질문한다:

| 카테고리 | 결정 항목 |
|---------|----------|
| **범위** | 기능명, User Story, 작업 영역(백/프론트/풀스택) |
| **데이터** | 입출력 형태, API 시그니처, 데이터 구조 |
| **시나리오** | 핵심 happy-path, 엣지 케이스, 에러 처리 |
| **기술** | 사용 라이브러리, 의존성, 제약 사항 |
| **테스트** | 검증 가능한 단위, Given/When/Then 시나리오 후보 |
| **비범위** | "이번 작업에 포함하지 않을 것" |

---

## 2. 인터뷰 결과 요약

해소된 결정 사항을 항목별로 정리하여 사용자에게 출력한다 (확인 질문은 다음 단계에서 따로 진행):

```
## 인터뷰 결과

**기능명**: [기능명]
**작업 영역**: [백엔드/프론트엔드/풀스택]
**User Story**:
  - As a [사용자 유형]
  - I want [원하는 기능]
  - So that [얻고자 하는 가치]
**주요 결정**:
  - [결정 1]
  - [결정 2]
**테스트 시나리오 후보**:
  - Scenario 1: Given ... / When ... / Then ...
  - Scenario 2: ...
**범위 외**:
  - [이번 작업에서 다루지 않을 것]
```

---

## 3. 다음 단계 결정 — AskUserQuestion

요약 출력 직후 **AskUserQuestion** 도구로 다음을 묻는다.

### 질문 형식

```
question: "다음 단계를 어떻게 진행할까요?"
header: "다음 단계"
multiSelect: false
options:
  - label: "전체 워크플로우 진행 (추천)"
    description: "스펙 문서 작성 후 즉시 spec-tdd → spec-code-review까지 자동 실행"
  - label: "스펙 문서만 작성"
    description: "spec.md / plan.md / context.md만 생성하고 종료. TDD/리뷰는 수동으로 따로 호출"
```

### 분기 — 사용자 응답 처리

| 사용자 선택 | 실행 명령 |
|------------|----------|
| **전체 워크플로우 진행** | `/kx:spec-write --skip-confirm --workflow=tdd` |
| **스펙 문서만 작성** | `/kx:spec-write --skip-confirm --workflow=tdd --no-chain` |

선택 직후 **즉시 해당 명령을 실행**한다. 추가 확인 없음.

### 이후 흐름

- **전체 진행 선택 시**: `spec-write → spec-tdd → spec-code-review`까지 자동
- **작성만 선택 시**: `spec-write`가 안내 출력 후 종료. 사용자가 원할 때 `/kx:spec-tdd` 직접 호출 가능

---

## 단독 실행 vs 체인 실행

- **단독 실행**: 사용자가 직접 `/kx:spec-grill` 호출 시 — 위 전체 흐름을 그대로 진행.
- **다른 스킬에서 호출**: 현재는 진입점 전용이므로 다른 스킬의 호출 대상이 아니다.
