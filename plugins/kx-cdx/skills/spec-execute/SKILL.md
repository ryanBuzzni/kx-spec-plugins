---
name: spec-execute
description: 스펙 문서 작성/갱신 후 개발 에이전트로 구현까지 자동 진행. "스펙 실행", "spec execute", "스펙 작성하고 개발", "스펙문서 갱신", "스펙 갱신", "spec 갱신" 등으로 트리거. /spec-execute로도 호출 가능.
---

# Spec → Execute 워크플로우

세션 컨텍스트를 기반으로 스펙 문서를 작성/갱신하고, 바로 개발 에이전트로 구현까지 진행한다.
**질문 없이 즉시 실행한다.**

기능명: $ARGUMENTS

---

## Phase 0: 분기 판단

1. `$ARGUMENTS`에서 기능명 추출. 비어있으면 세션 컨텍스트에서 추론.
2. `specs/` 하위에서 기능명과 일치하는 폴더 탐색
   - **폴더가 없는 경우** → Phase 1A (신규 생성)
   - **폴더가 있는 경우** → Phase 1B (갱신)
3. "갱신", "업데이트", "update" 키워드가 포함된 경우 → 기존 폴더를 찾아 Phase 1B 강제 진행

---

## Phase 1A: 스펙 신규 생성

1. 폴더명: `YYYYMMDD-기능명`
2. `specs/codebase/index.md`를 읽어 관련 feature 파악
3. 세션에서 논의된 내용(요구사항, 기술 결정, 제약사항, 변경 파일)을 수집
4. 다음 세 파일을 즉시 생성 (확인 없이):

### spec.md
```markdown
---
name: [기능명]
related_features: [관련 feature 목록]
status: planned
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

## Technical Constraints
- [사용 기술 스택]
- [제약사항]

## Data Structure / API
- [논의된 데이터 구조]
- [API 엔드포인트]

## Implementation Notes
- [세션에서 발견한 특이사항]
```

### plan.md
```markdown
# [기능명] Implementation Plan

## Overview
[한 줄 요약]

## Tasks
1. [ ] [작업 1] - [대상 파일/모듈]
2. [ ] [작업 2] - [대상 파일/모듈]
3. [ ] [작업 3] - [대상 파일/모듈]

## Technical Approach
- [선택된 방식과 이유]

## Dependencies
- [관련 feature/모듈]

## Estimated Impact
- [수정되는 파일/모듈]
- [주의할 점]
```

### context.md
```markdown
# [기능명] Context

## Current Status
- Phase: Planning
- Last Updated: YYYY-MM-DD

## Summary
- [세션에서 수행한 작업 요약]

## Files Changed
- (아직 없음)

## Session History
- YYYY-MM-DD: 스펙 문서 생성 via spec-execute
```

---

## Phase 1B: 스펙 갱신

기존 `specs/[폴더명]/` 내의 **spec.md, plan.md, context.md** 세 파일을 모두 읽고, 세션에서 새로 논의/변경된 내용을 반영하여 갱신한다.

1. `specs/[폴더명]/spec.md`, `plan.md`, `context.md` 순서대로 읽기
2. 세션에서 변경된 내용 수집:
   - 새로운 요구사항, 수정된 acceptance criteria
   - 변경된 기술 결정, 추가된 제약사항
   - 완료된 작업, 새로 발견된 작업
   - 변경된 파일 목록 (git diff 참조)
3. **세 파일 모두 갱신**:
   - `spec.md`: 요구사항, acceptance criteria, 기술 제약 업데이트. status 변경 (planned → in_progress → completed)
   - `plan.md`: 완료된 작업 체크, 새 작업 추가, 접근 방식 변경 반영
   - `context.md`: Current Status 업데이트, Files Changed 추가, Session History에 갱신 이력 추가

---

## Phase 2: 개발 실행

스펙 문서 생성/갱신 즉시 개발 에이전트를 실행한다.

1. `spec.md`와 `plan.md`를 기반으로 작업 영역 자동 판별
   - 백엔드 → `backend-dev`
   - 웹 프론트 → `frontend-web-dev`
   - 앱 프론트 → `frontend-app-dev`
   - 복합 → 병렬 또는 순차 실행

2. `~/plugins/kx-cdx/skills/use-agents/references/AGENT_SYSTEM.md`의 실행 방법을 따라 에이전트 실행

3. 에이전트에게 전달할 컨텍스트:
   - `specs/[폴더명]/spec.md` 전체 내용
   - `specs/[폴더명]/plan.md` 전체 내용
   - 작업 대상 파일 목록
   - 세션에서 논의된 기술적 결정사항

---

## 실행 흐름

```
/spec-execute [기능명]
     ↓
[폴더 존재 확인 → 신규 생성 or 갱신]
     ↓
[spec.md + plan.md + context.md 생성/갱신]
     ↓
[작업 영역 판별 → 에이전트 즉시 실행]
     ↓
[완료 보고]
```

## 완료 보고

```
━━━━━━━━━━━━━━━━━━━━━━━━━
Spec → Execute 완료

  기능: [기능명]
  모드: [신규 생성 | 갱신]
  스펙: specs/[폴더명]/
    - spec.md
    - plan.md
    - context.md
  에이전트: [사용된 에이전트]
  수정 파일: [파일 목록]
━━━━━━━━━━━━━━━━━━━━━━━━━
```
