---
name: spec-tdd
description: TDD tracer-bullet 사이클로 스펙을 구현. spec.md의 Acceptance Criteria를 한 번에 하나씩 RED→GREEN→REFACTOR로 처리하고 완료 후 자동으로 `/kx:spec-code-review` 호출. "spec tdd", "스펙 tdd", "tdd 실행", "tracer bullet", "/kx:spec-tdd" 등으로 트리거.
---

# Spec TDD: tracer-bullet 구현 스킬

스펙 문서(`specs/[feature]/spec.md`, `plan.md`)를 진실의 원천으로 삼아 Kent Beck TDD 사이클로 구현한다.

> **전체 흐름**: `kx:spec-grill → kx:spec-write → kx:spec-tdd → kx:spec-code-review`

> **🔵 필수 참조: 실행 전에 반드시 읽고 원칙을 숙지한다.**
> - `~/.claude/skills/tdd/SKILL.md` — TDD 코어 원칙, tracer bullet, horizontal slice 안티패턴
> - `~/.claude/skills/tdd/tests.md` — 좋은 테스트 vs 나쁜 테스트
> - `~/.claude/skills/tdd/mocking.md` — 모킹 가이드라인

---

## 0. 사전 조건

- `specs/[feature-name]/spec.md`, `plan.md`, `context.md`가 존재해야 한다.
- 없으면 다음을 안내하고 종료:
  ```
  스펙 문서가 없습니다. 먼저 다음 중 하나를 실행하세요:
    - /kx:spec-grill → 인터뷰 후 자동 진행
    - /kx:spec-write → 스펙 문서만 작성
  ```

---

## 1. 컨텍스트 로드

다음 순서로 파일을 읽어 컨텍스트를 확보한다. **전역 컨텍스트 제한** — 지정된 spec 폴더 외 파일은 필요한 만큼만 읽는다.

| 순서 | 파일 | 추출할 정보 |
|------|------|------------|
| 1 | `specs/[feature]/spec.md` | Acceptance Criteria (BDD 시나리오), Test Plan |
| 2 | `specs/[feature]/plan.md` | Phase 목록, 작업 항목 |
| 3 | `specs/[feature]/context.md` | 현재 진행 상태, 이미 완료된 작업 |

기존 코드 탐색은 **Serena MCP 우선** (`find_symbol`, `find_referencing_symbols`, `get_symbols_overview`). Grep/Glob은 비코드 파일에만.

---

## 2. Tracer Bullet — 첫 사이클

가장 단순한 happy-path 시나리오 하나를 골라 **end-to-end로 통과**시킨다. 이 사이클이 인터페이스/구조/호출 경로를 실전 검증하는 뼈대가 된다.

```
🔴 RED   → spec.md의 첫 시나리오에 대한 실패 테스트 작성 → 실행하여 실패 확인
🟢 GREEN → 통과시키는 최소 코드 작성 → 실행하여 통과 확인
```

### 핵심 규칙

- 테스트는 **공개 인터페이스만 사용**, 내부 구현 디테일 검증 금지
- 테스트 이름은 **동작(behavior) 중심** — 예: `shouldRejectEmptyCart`, `사용자는_빈_장바구니로_체크아웃할_수_없다`
- 통과를 위한 **최소 코드만** — 추측성 코드/조기 추상화 금지
- 발생 불가능한 시나리오에 대한 에러 처리 금지

---

## 3. 증분 사이클 — 한 번에 하나의 동작

남은 시나리오를 `plan.md`의 Phase 순서대로 처리한다.

```
RED → GREEN → (필요 시) REFACTOR → 다음 시나리오
```

### 매 사이클 규칙

- **테스트 1개 → 구현 1개 → 테스트 실행** (vertical slice)
- ❌ **여러 테스트를 한꺼번에 쓰지 말 것** (horizontal slice 안티패턴 — `~/.claude/skills/tdd/SKILL.md` 참조)
- REFACTOR는 **GREEN 상태에서만**. RED 중에는 절대 금지.
- 매 사이클 후 **모든 관련 테스트 실행** (성능 위해 전체 테스트는 필요 시에만)

### 결함 발견 시 (TDD 사이클 중 버그 노출)

1. 먼저 **API 수준의 실패 테스트** 작성
2. **재현하는 가장 작은 테스트** 추가
3. 두 테스트 모두 통과시키기

---

## 4. 리팩토링 (Tidy First)

모든 시나리오가 GREEN 상태가 된 후에만 리팩토링한다. Kent Beck의 **Tidy First** 원칙:

- **구조적 변경** (이름 변경, 추출, 이동) ↔ **동작 변경** 은 별도 커밋
- 구조적 변경 전후로 테스트 실행하여 동작 변경 없음 검증
- 한 번에 하나의 리팩토링, 각 단계 후 테스트 실행

리팩토링 후보 (`~/.claude/skills/tdd/refactoring.md` 참조):
- 중복 제거
- 깊은 모듈로 추출 (작은 인터페이스 + 깊은 구현)
- 매직넘버 → 명명 상수
- SOLID 원칙은 자연스러운 곳에만 적용

---

## 5. Surgical Changes 원칙

`~/CLAUDE.md`의 수술적 변경 원칙을 적용:

- 인접 코드/주석/포맷팅을 "개선"하지 말 것
- 고장나지 않은 것을 리팩토링하지 말 것
- 본인의 변경으로 사용 안 되게 된 import/변수/함수만 제거
- 기존에 있던 데드 코드는 요청받지 않는 한 제거하지 말 것

---

## 6. context.md 업데이트

구현 완료 후 `specs/[feature]/context.md`를 갱신한다. 갱신이므로 `## 갱신 이력`에 오늘 날짜로 한 줄을 추가한다:

```markdown
## 마지막 업데이트
- 세션 상태: Implementation Complete

## 현재 진행 상태
- 모든 Phase 완료, 코드 리뷰 대기

## 완료된 작업
- [x] Phase 1: [단계명]
- [x] Phase 2: [단계명]
- ...

## 작성된 테스트
- [테스트 파일 경로 및 시나리오 수]

## 변경된 파일
- [구현 파일 목록]
- [테스트 파일 목록]

## 갱신 이력
- YYYY-MM-DD: TDD 구현 완료 (오늘 날짜)
```

---

## 7. 다음 단계 자동 연결

context.md 업데이트 직후 **즉시** 다음 명령을 실행한다. 멈추지 않는다.

```
/kx:spec-code-review
```

### 리뷰 결과 처리

- **blocker 0개** → 완료 보고
- **blocker 1개+** → 자가 개선 사이클 진입 (최대 3회, `references/workflow.md` 참조)
- `[needs-judgment]` 발견은 **사용자에게 묻지 않고** `spec.md`의 `## 리뷰 이슈 참고` 섹션에 기록 (`references/auto-fix-criteria.md` 참조)

---

## 체크리스트 — 매 사이클 자가 점검

```
[ ] 테스트는 동작(behavior)을 설명한다, 구현이 아니다
[ ] 테스트는 공개 인터페이스만 사용한다
[ ] 테스트는 내부 리팩토링에도 살아남는다
[ ] 코드는 이번 테스트에 필요한 최소량이다
[ ] 추측성 기능을 추가하지 않았다
```
