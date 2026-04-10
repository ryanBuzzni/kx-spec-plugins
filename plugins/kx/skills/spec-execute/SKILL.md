---
name: spec-execute
description: 스펙 문서 기반으로 개발→리뷰→테스트 전체 워크플로우 실행. "스펙 실행", "spec execute", "스펙 작성하고 개발", "스펙문서 갱신", "스펙 갱신", "spec 갱신" 등으로 트리거. /spec-execute로도 호출 가능.
---

# Spec Execute 워크플로우

스펙 문서(spec.md, plan.md, context.md)를 기반으로 개발 → 리뷰 → 테스트를 실행한다.
**질문 없이 즉시 실행한다.**

> **🔴 핵심 원칙: 이 워크플로우는 Phase 1 → 2 → 3 → 4 를 끝까지 실행해야 완료된다.**
> **개발(Phase 1) 완료는 중간 단계일 뿐이다. 서브에이전트가 반환되면 반드시 Phase 2(스펙 갱신) → Phase 3(코드 리뷰) → Phase 4(테스트)를 이어서 실행한다.**
> **어떤 Phase에서든 "여기서 끝"이라고 판단하지 않는다. 완료 보고가 출력될 때까지 멈추지 않는다.**

> **🔵 필수 참조: 실행 전에 반드시 아래 두 파일을 읽고 전체 워크플로우 흐름과 리뷰 기준을 숙지한다.**
> - `~/.claude/skills/spec/references/workflow.md` — 전체 워크플로우 흐름, 자가 평가 사이클, 완료 조건
> - `~/.claude/skills/spec/references/code-review-checklist.md` — 코드 리뷰 판정 기준

기능명: $ARGUMENTS

---

## Phase 0: 스펙 문서 확인

1. `$ARGUMENTS`에서 기능명 추출. 비어있으면 세션 컨텍스트에서 추론.
2. `specs/` 하위에서 기능명과 일치하는 폴더 탐색
3. **스펙 문서(spec.md, plan.md)가 존재하는지 확인**
   - **존재** → `spec.md`, `plan.md` 읽고 Phase 1로 진행
   - **미존재** → `/kx:spec-write` 스킬을 먼저 실행하여 스펙 문서 생성 (`--skip-confirm` 플래그 전달) 후 Phase 1로 진행

---

## Phase 1: 개발 실행

스펙 문서를 기반으로 즉시 개발 에이전트를 실행한다.

1. `spec.md`와 `plan.md`를 기반으로 작업 영역 자동 판별
   - 백엔드 → `backend-dev`
   - 웹 프론트 → `frontend-web-dev`
   - 앱 프론트 → `frontend-app-dev`
   - 복합 → 병렬 또는 순차 실행

2. `~/.claude/skills/use-agents/references/AGENT_SYSTEM.md`의 실행 방법을 따라 에이전트 실행

3. 에이전트에게 전달할 컨텍스트:
   - `specs/[폴더명]/spec.md` 전체 내용
   - `specs/[폴더명]/plan.md` 전체 내용
   - 작업 대상 파일 목록
   - 세션에서 논의된 기술적 결정사항

> **⚠️ CRITICAL: 개발 에이전트가 완료되면 여기서 멈추지 않는다. 반드시 Phase 2 → 3 → 4를 순서대로 이어서 실행한다. 개발 완료는 워크플로우의 중간 단계일 뿐이다.**

---

## Phase 2: 스펙 문서 갱신 (spec-write)

개발 에이전트 작업 완료 후, **즉시** 변경 내용을 스펙 문서에 반영한다.

1. 변경된 파일 목록, 완료된 작업 반영
2. context.md 상태 업데이트
3. **갱신 완료 후 멈추지 않고 Phase 3으로 즉시 이어진다**

---

## Phase 3: 코드 리뷰 (`/kx:spec-code-review`)

> **⚠️ Phase 2 완료 후 반드시 `/kx:spec-code-review` 스킬을 실행한다. 건너뛰지 않는다.**
> **다른 플러그인의 리뷰 스킬이 아닌, 반드시 `/kx:spec-code-review`를 사용한다.**

code-reviewer 에이전트를 spawn하여 변경된 코드를 리뷰한다.

1. `/kx:spec-code-review` 스킬을 실행한다
2. 스킬 내부에서 `~/.claude/agents/code-reviewer.md`와 체크리스트를 참조하여 리뷰 수행
4. 리뷰 결과 판정:
   - **blocker 0개** → **즉시 Phase 4로 진행**
   - **blocker 1개+** → **여기서 멈추지 않는다.** 즉시 Phase 5(개선 사이클)로 진입하여 blocker를 수정한다

---

## Phase 4: 테스트 실행 (`/kx:spec-testing`)

> **⚠️ Phase 3 완료 후 반드시 `/kx:spec-testing` 스킬을 실행한다. 건너뛰지 않는다.**
> **다른 플러그인의 테스트 스킬이 아닌, 반드시 `/kx:spec-testing`을 사용한다.**

1. `spec.md`의 Test Plan에서 테스트 시나리오 확인
2. 작업 영역에 맞게 `/kx:spec-testing` 스킬을 실행:
   - 백엔드 → `/kx:spec-testing back`
   - 웹 프론트 → `/kx:spec-testing web`
   - 앱 프론트 → `/kx:spec-testing app`
3. Test Plan의 테스트 시나리오를 기반으로 전달
4. 테스트 결과 판정:
   - **전체 통과** → 완료 보고
   - **실패 존재** → 개선 사이클 진입 (Phase 5)

---

## Phase 5: 자가 평가 및 개선 사이클

> **⚠️ blocker 또는 테스트 실패 발견 시 반드시 진입한다. "사용자에게 보고"만 하고 멈추지 않는다.**

코드 리뷰 또는 테스트에서 문제가 발견되면 자동으로 개선 사이클에 진입한다.
상세 규칙은 `~/.claude/skills/spec/references/workflow.md`를 따른다.

### 흐름

```
[문제 발견] → [원인 파악] → [수정 (개발 에이전트 재실행)]
     → [Phase 2: 스펙 갱신] → [Phase 3: 코드 리뷰] → [Phase 4: 테스트]
     → [통과?] → Yes → 완료 보고
        ↓ No
     [재진입] (최대 3회)
```

### 구체적 행동
1. blocker/실패 내용을 분석하여 원인 파악
2. 개발 에이전트를 재실행하여 수정
3. Phase 2(스펙 갱신) → Phase 3(코드 리뷰) → Phase 4(테스트) 순서로 재실행
4. **통과할 때까지 반복한다** (최대 3회)

### 규칙
- 최대 **3회** 반복
- 3회 후에도 미해결 시 사용자에게 보고하고 수동 판단 요청
- 각 사이클마다 개선 보고 출력

---

## 실행 흐름

```
/spec-execute [기능명]
     ↓
[Phase 0] 스펙 문서 존재 확인 → 없으면 /kx:spec-write 먼저 실행
     ↓
[Phase 1] 작업 영역 판별 → 개발 에이전트 실행
     ↓
[Phase 2] 스펙 문서 갱신
     ↓
[Phase 3] 코드 리뷰
     ↓
[Phase 4] 테스트 실행
     ↓
[통과?] → Yes → 완료 보고
   ↓ No
[Phase 5] 개선 사이클 → Phase 2로 재진입 (최대 3회)
```

## 완료 보고

```
━━━━━━━━━━━━━━━━━━━━━━━━━
Spec → Execute 완료
━━━━━━━━━━━━━━━━━━━━━━━━━

  기능: [기능명]
  모드: [신규 생성 | 갱신]
  스펙: specs/[폴더명]/
    - spec.md
    - plan.md
    - context.md
  에이전트: [사용된 에이전트]
  개선 사이클: [N]회 수행
  코드 리뷰: blocker 0 | issue N | suggestion N
  테스트: 전체 통과
  수정 파일: [파일 목록]
━━━━━━━━━━━━━━━━━━━━━━━━━
```
