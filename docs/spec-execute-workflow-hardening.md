# spec-execute 워크플로우 보강 메모

> 작성일: 2026-04-29
> 상태: 초안 (필요 시점에 검토 후 적용)

`/kx:spec-execute` 워크플로우(Phase 1 개발 → 2 스펙 갱신 → 3 코드 리뷰 → 4 테스트 → 5 개선 사이클)에서
**Phase 1(개발 에이전트) 리턴 직후 부모 세션이 Phase 2~4를 건너뛰고 멈추거나 곧장 테스트로 넘어가는 누락**이 관찰됨.
SKILL.md 안의 "멈추지 말 것" 경고문(L14-16, L54)만으로는 100% 막히지 않으므로 아래 보강안을 정리해 둠.

---

## 관찰된 실패 패턴

1. **Phase 1 → 그대로 종료**: backend-dev 리턴 후 부모가 "작업 끝"으로 오인, Phase 2/3/4 누락.
2. **Phase 1 → Phase 4 직행**: dev 에이전트가 스코프를 벗어나 테스트 파일까지 읽고/실행, Phase 2·3 스킵.
3. **사용자 지시로 인한 Phase 우회**: "테스팅은 이렇게 해줘" 같은 입력을 받으면 부모가 Phase 2·3을 생략하는 경향.
   → 사용자 지시는 *해당 Phase의 입력*에만 반영해야 하며, **Phase 순서/실행 여부는 불변**이어야 함.

---

## 보강안 (효과 작은 것 → 큰 것)

### A. 지침 강화 (SKILL.md / 에이전트 프롬프트)

**A-1. spec-execute SKILL.md 에 "불변 규칙" 명시**
> 사용자 지시는 각 Phase의 *입력*에만 반영한다.
> Phase 순서(1→2→3→4)와 실행 여부는 사용자 요청으로도 변경/생략 불가.
> 테스트 관련 지시 = Phase 4 입력으로 보관, Phase 1~3은 그대로 실행.

**A-2. 개발 에이전트 프롬프트(`backend-dev.md`, `frontend-web-dev.md`, `frontend-app-dev.md`) 에 스코프 명시**
> 스코프: 구현 코드만. 테스트 파일 작성/수정/실행 금지.
> 테스트는 Phase 4(`/kx:spec-testing`)의 영역.
> dev 에이전트는 구현 완료 시점에 즉시 리턴. 테스트로 넘어가면 워크플로우 위반.

**A-3. 개발 에이전트 출력 템플릿 끝에 트리거 문장 강제**
> "Phase 1 완료. 오케스트레이터는 즉시 Phase 2(spec-write 갱신) 호출 필요."

체감 누락률: 80~90% 커버.

---

### B. TaskCreate 강제 (구조적 보강)

Phase 0 마지막에 **Phase 1~4를 Task로 미리 등록**.
미완료 Task가 화면에 남아 있어 부모가 "끝났다" 오판할 확률을 줄임.

```
- [ ] Phase 1: 개발 에이전트 실행
- [ ] Phase 2: 스펙 문서 갱신
- [ ] Phase 3: 코드 리뷰
- [ ] Phase 4: 테스트 실행
```

체감 누락률: 90%+ 커버.

---

### C. SubagentStop hook (결정론적 봉쇄)

`~/.claude/settings.json` 에 SubagentStop hook 추가:

- 트리거: `subagent_type` 이 `kx:backend-dev` / `kx:frontend-web-dev` / `kx:frontend-app-dev` 일 때
- 동작: system-reminder 주입
  > "spec-execute Phase 1 종료. 즉시 Phase 2(spec-write 갱신) → 3(code-review) → 4(testing) 호출 필요. 텍스트 응답으로 종료 금지."
- 범위: 다른 워크플로우(단독 `use dev` 등)에는 영향 없도록 좁게 매칭

체감: 거의 100% 봉쇄. 단, settings.json 수정이라 영향 범위 검토 필요.

---

## Phase 5 (개선 사이클) Task 모델 — 하이브리드

코드 리뷰/테스트 실패로 Phase 5 진입 시, Task 리스트를 어떻게 다룰지에 대한 정리.

**선택안: 하이브리드**
- 초기엔 Phase 1~4 정적 등록 (B안 그대로)
- Phase 5 진입할 때만 **사이클 단위로 Task 묶음 추가**
- 최대 3회 한도가 시각적으로 강제됨

예시:
```
- [완료] Phase 1: 개발
- [완료] Phase 2: 스펙 갱신
- [완료] Phase 3: 코드 리뷰  ← blocker 2개 발견
- [진행중] 개선 사이클 1/3: blocker 수정
    - Phase 1 재실행
    - Phase 3 재리뷰
    - Phase 4 테스트
- [대기] Phase 4: 테스트  ← 사이클 통과 후 진행
```

3회 도달 시 Task 라벨에 "한도 도달 - 수동 판단 필요" 명시 → 자동 종료 트리거.

---

## 적용 권장 조합

| 옵션 | 구성 | 강도 |
|------|------|------|
| 가벼움 | A + B | 일상 케이스 대부분 커버 |
| 확실 | A + B + C | 누락 봉쇄 (권장) |

이전엔 지침만으로도 잘 돌았으나 그것은 모델/컨텍스트 운에 가까움.
컨텍스트가 길어질수록 지침은 약해지므로, 안정성을 원하면 C까지.

---

## 적용 시 수정 대상 파일

- `~/.claude/plugins/marketplaces/kx/plugins/kx/skills/spec-execute/SKILL.md`
  - Phase 0 마지막에 TaskCreate 단계 추가
  - "불변 규칙" 박스 삽입
  - Phase 5 섹션에 하이브리드 Task 모델 명시
- `~/.claude/agents/backend-dev.md`, `frontend-web-dev.md`, `frontend-app-dev.md`
  - 스코프 제한 (테스트 금지) + 즉시 리턴 + 출력 템플릿 트리거 문장
- (옵션 C) `~/.claude/settings.json`
  - SubagentStop hook 1개 추가
