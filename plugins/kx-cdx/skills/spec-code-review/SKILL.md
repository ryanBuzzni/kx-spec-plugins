---
name: spec-code-review
description: 코드 리뷰 스킬. "코드 리뷰", "코드리뷰", "리뷰해줘", "review", "/spec-code-review" 등으로 트리거. code-reviewer 에이전트를 spawn하여 변경된 코드를 정확성/보안/성능/품질 관점에서 체계적으로 점검한다.
---

# 코드 리뷰 스킬

code-reviewer 에이전트를 spawn하여 변경된 코드를 체계적으로 리뷰한다.

> **🔵 필수 참조: 실행 전에 반드시 아래 두 파일을 읽고 숙지한다.**
> - `~/plugins/kx-cdx/references/workflow.md` — 전체 워크플로우 흐름, 자가 평가 사이클, 완료 조건
> - `~/plugins/kx-cdx/references/code-review-checklist.md` — 코드 리뷰 판정 기준

---

## 실행 절차

1. `~/.codex/agents/code-reviewer.toml` 에이전트가 설치되어 있는지 확인한다.
2. `~/plugins/kx-cdx/references/code-review-checklist.md` 파일을 읽는다.
3. Codex 서브에이전트 기능으로 `code-reviewer` 에이전트를 실행한다.

```
서브에이전트 프롬프트:
- agent: `code-reviewer`
- prompt: |
    현재 작업 디렉토리의 변경된 코드를 리뷰해주세요.

    ---
    ## 리뷰 체크리스트
    [code-review-checklist.md 내용]

    ---
    ## 추가 컨텍스트
    [사용자가 제공한 추가 정보가 있으면 포함]
```

4. 에이전트의 리뷰 결과를 사용자에게 그대로 전달한다.

## 결과 판정

리뷰 결과를 판정한다:

- **blocker 0개** → "리뷰 통과. 커밋/푸시 가능합니다." + issue/suggestion 목록
- **blocker 1개+** → 개선 사이클 진입 필요 (workflow.md 참조)
