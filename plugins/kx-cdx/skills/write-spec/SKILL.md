---
name: write-spec
description: 현재 세션에서 조사/논의한 내용을 기반으로 스펙 문서(spec.md, plan.md, context.md)를 자동 작성. 사용자가 "스펙 작성", "스펙문서 작성", "스펙 작성해", "spec 작성", "스펙 문서 만들어" 등 스펙 문서 생성을 요청할 때 트리거.
---

# 스펙 문서 작성 스킬

현재 세션에서 조사하고 논의한 내용을 기반으로 스펙 문서를 작성한다.

## 1. 기능명 확인

- 사용자 메시지에서 기능명을 추출한다.
- 기능명이 불명확하면 물어본다.
- 폴더명 형식: `YYYYMMDD-기능명` (오늘 날짜 사용)

## 2. 세션 컨텍스트 수집

현재 대화에서 다음 정보를 추출한다:

- **논의된 기능/작업 내용**: 사용자가 요청하거나 논의한 기능
- **조사 결과**: 코드 탐색, 문서 조회 등으로 파악한 정보
- **기술적 결정사항**: 선택된 기술, 라이브러리, 패턴
- **제약사항**: 발견된 제한 사항이나 주의점
- **변경된 파일**: git diff나 작업 중 수정된 파일 (있다면)

## 3. 사용자 확인

추출한 내용을 요약하여 보여준다:

```
## 세션에서 수집한 내용

**기능**: [기능명]
**논의 내용**: [요약]
**기술 결정**: [결정사항]
**제약사항**: [제약사항]

이 내용으로 스펙 문서를 작성할까요?
빠진 내용이나 추가할 내용이 있으면 말씀해주세요.
```

→ **사용자 확인 후 진행**

## 4. 스펙 문서 생성

### 4.1 폴더 생성

`specs/[폴더명]/` 폴더를 생성한다.

### 4.2 spec.md 작성

```markdown
---
name: [기능명]
related_features: [관련 feature 목록]
status: planned | in_progress | completed
created: YYYY-MM-DD
---

# [기능명] Specification

## User Story
- As a [사용자 유형]
- I want [원하는 기능]
- So that [얻고자 하는 가치]

## Acceptance Criteria
- [ ] [세션에서 논의된 기준 1]
- [ ] [세션에서 논의된 기준 2]
- [ ] [세션에서 논의된 기준 3]

## Technical Constraints
- [사용 기술 스택]
- [제약사항]

## Data Structure / API
- [논의된 데이터 구조]
- [API 엔드포인트]

## Implementation Notes
- [세션에서 발견한 특이사항]
- [주의점]

## Test Plan

### 백엔드 테스트
- **Auth 필요 시**: 재사용가능한 access token 생성 헬퍼 메소드를 만들어 테스트에서 사용
- [ ] [단위 테스트 케이스]
- [ ] [통합 테스트 케이스]

### 프론트엔드 테스트
- **Auth 필요 시** (택 1):
  - 재사용가능한 테스터 로그인 헬퍼 함수 생성하여 사용
  - 필요하다면 `auth.spec.ts` 별도 작성 → 유저가 1회 로그인 후 테스트 진행
- [ ] [컴포넌트/페이지 테스트 케이스]

### UI 테스트 (Playwright CLI)
- Playwright CLI로 UI 검증 테스트 수행
- **Auth 로그인 불가 시**: `test/` 페이지를 별도 생성하여 Playwright CLI로 검증
- [ ] [UI 테스트 시나리오]
```

### 4.3 plan.md 작성

세션에서 논의된 내용을 기반으로 구현 계획을 3~5개의 Phase로 분리하여 작성한다.

```markdown
# [기능명] Implementation Plan

## Overview
- [기능의 전체적인 구현 방향 요약]

## Phase 1: [첫 번째 단계 이름]
- **목표**: [이 Phase에서 달성할 목표]
- [ ] 작업 1
- [ ] 작업 2
- **검증**: [완료 확인 방법]

## Phase 2: [두 번째 단계 이름]
- **목표**: [이 Phase에서 달성할 목표]
- [ ] 작업 3
- [ ] 작업 4
- **검증**: [완료 확인 방법]

## Phase 3: [세 번째 단계 이름]
- **목표**: [이 Phase에서 달성할 목표]
- [ ] 작업 5
- [ ] 작업 6
- **검증**: [완료 확인 방법]

## Dependencies
- [외부 의존성이나 선행 조건]

## Risks
- [예상되는 리스크와 대응 방안]
```

### 4.4 context.md 작성

```markdown
# [기능명] Context

## Current Status
- Phase: [Planning | In Progress | Completed]
- Last Updated: [날짜]

## Summary
- [세션에서 수행한 작업 요약]

## Files Changed
- [변경된 파일 목록 (있다면)]

## Session History
- [날짜]: 스펙 문서 작성 via write-spec
```

## 5. 결과 출력

```
스펙 문서 생성 완료:
  - specs/[폴더명]/spec.md (요구사항)
  - specs/[폴더명]/plan.md (구현 계획)
  - specs/[폴더명]/context.md (상태 추적)

다음 단계:
  - plan.md 검토 후 승인 → 구현 시작
  - use dev → 개발 시작
```
