# 프론트엔드 테스트 전략

테스트가 **production 코드의 회귀를 실제로 잡도록** 만들기 위한 공통 원칙. 모든 프론트엔드 dev/tester/reviewer 에이전트가 이 문서를 따른다.

---

## 핵심 원칙 (CRITICAL)

### 1. 사본 검증 금지
테스트 파일 안에 production 로직을 **복사·재정의**하지 않는다. 사본을 검증하면 production이 깨져도 테스트는 통과 — **회귀 방지력 0** (false negative).

```ts
// ❌ 사본 검증 — 의미 없음
test('toast variant', () => {
  function resolveToastVariant(r) { /* hooks.ts의 로직을 다시 적음 */ }
  expect(resolveToastVariant({...})).toBe('success');
});

// ✅ 실제 함수 import
import { resolveToastVariant } from '@/services/foo/_utils';
test('toast variant', () => expect(resolveToastVariant({...})).toBe('success'));
```

### 2. Functional Core, Imperative Shell (Bernhardt, 2012)
도메인 의사결정 로직은 **순수 함수**(pure)로, 외부 의존(API, store, 시간, native module)은 **shell**로 분리. 외부 의존은 함수 인자로 주입받게 설계 → 자연스럽게 테스트 가능해짐. 테스트 가능성은 부산물이고, **관심사 분리(SoC) 자체가 목적**.

### 3. Implementation detail이 아닌 observable behavior 검증
변수명·내부 호출 순서·private 상태 검증 X. **입력 → 출력**, **사용자 행위 → 렌더 결과**만 검증. (Kent C. Dodds — Testing Trophy)

---

## 두 layer로 분담

각 로직 종류에 가장 싼 layer로 매칭. 한 layer로 다 덮으려 하지 않는다.

### L1 — 순수 함수 unit test
**대상**: derivation, 가드, 폼 검증, 분기 매핑, 시퀀스 함수, 타입 가드.

**시그니처 예시**:
| 유형 | 시그니처 |
|---|---|
| `useMemo` 본체 | `deriveX(input): T` |
| 입력/Select 가드 | `parseValue(val: string): T \| null` |
| 폼 검증 | `validateForm(input): { valid; errors }` |
| 분기 매핑 | `resolveVariant(...): 'success'\|'warning'\|'error'` |
| 시퀀스/루프 | `runSeq(items, apiCall)` (의존성 인자 주입) |
| 타입 가드 | `isValid(d): d is T` |

**위치**:
- 추출 코드: `services/[domain]/_utils.ts` 또는 `[Component].utils.ts` (소스 colocate)
- 테스트: `[domain]/__tests__/*.test.ts`

### L2 — 훅/컴포넌트 통합 test
**대상**: React Query 훅, `useEffect` 체인, 캐시 invalidate 배선, 사용자 행위 시나리오.

**표준 패턴** (TanStack 공식 + TkDodo):
- 매 테스트마다 새 `QueryClient` (격리)
- `defaultOptions: { queries: { retry: false } }` (timeout 방지)
- API mock은 **MSW** (Mock Service Worker) — single source of truth
- React 18+: `renderHook`/`render` from `@testing-library/react` (web) 또는 `@testing-library/react-native` (mobile)
- `renderWithProviders(ui, { queryClient, i18n, store })` fixture 1회 작성 후 재사용

**도입 범위**: 모든 훅 X. **자주 깨지는 도메인 / mutation invalidate 검증이 critical한 곳**부터 점진. (Testing Trophy — integration 우선)

---

## 추출 패턴 — 외부 의존은 인자 주입

```ts
// ❌ before — 테스트 불가
useMutation({ mutationFn: async (p) => {
  for (const email of p.emails) { await request.post('/invite', { email }); }
}});

// ✅ after — 인자 주입으로 추출
export async function runInviteLoop(emails, apiCall) {
  for (const email of emails) await apiCall({ email });
}
useMutation({ mutationFn: (p) => runInviteLoop(p.emails, api.invite) });
```

native module / AsyncStorage / 시간 / 랜덤 — 모두 인자로 받게 설계.

---

## Coverage는 보조 지표

- 100% 추구 X — line coverage 100%여도 회귀 못 잡음 (Google Testing Blog)
- 도메인별 60~85% threshold가 합리적
- code review에서 weak zone 식별용으로만 사용

---

## 출처

- [Kent C. Dodds — Testing Trophy](https://kentcdodds.com/blog/the-testing-trophy-and-testing-classifications)
- [Kent C. Dodds — Testing Implementation Details](https://kentcdodds.com/blog/testing-implementation-details)
- [TanStack Query Testing (공식)](https://tanstack.com/query/v5/docs/react/guides/testing)
- [TkDodo — Testing React Query](https://tkdodo.eu/blog/testing-react-query)
- [Gary Bernhardt — Functional Core, Imperative Shell (2012)](https://www.destroyallsoftware.com/screencasts/catalog/functional-core-imperative-shell)
- [Google Testing Blog — Code Coverage Best Practices](https://testing.googleblog.com/2020/08/code-coverage-best-practices.html)
- [Sentry — Mutation-testing our JS SDKs](https://sentry.engineering/blog/js-mutation-testing-our-sdks) (95% coverage여도 mutant 다수 생존 사례)
