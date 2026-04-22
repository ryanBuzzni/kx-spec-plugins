---
name: debugging
description: 에러 분석, 버그 추적, 문제 해결을 위한 전문 스킬
disable-model-invocation: true
---
name: debugging

# 디버깅 스킬

에러 분석, 버그 추적, 문제 해결을 위한 전문 스킬

## 디버깅 프로세스

### 1단계: 정보 수집
- 에러 메시지 전체 확인
- 스택 트레이스 분석
- 발생 조건/재현 방법 파악
- 관련 코드 탐색

### 2단계: 분석
- 에러 유형 분류
- 직접 원인 파악
- 근본 원인 분석 (Root Cause)
- 영향 범위 확인

### 3단계: 해결
- 수정 코드 제안
- 대안 제시
- 예방책 제안
- 검증 방법 안내

---
name: debugging

## 기술 스택별 에러 패턴

### NestJS
| 에러 | 원인 | 해결 |
|-----|------|------|
| Nest can't resolve dependencies | DI 설정 누락 | Module에 provider 등록 |
| Cannot read property of undefined | null 체크 누락 | Optional chaining 사용 |
| 401 Unauthorized | 토큰 만료/누락 | Guard, 토큰 갱신 확인 |

### FastAPI
| 에러 | 원인 | 해결 |
|-----|------|------|
| ValidationError | Pydantic 타입 불일치 | 요청 데이터 형식 확인 |
| IntegrityError | DB 제약조건 위반 | 유니크, FK 확인 |
| 422 Unprocessable Entity | 요청 body 형식 | 스키마 확인 |

### Next.js / React
| 에러 | 원인 | 해결 |
|-----|------|------|
| Hydration mismatch | SSR/CSR 불일치 | 'use client', 동적 import |
| Too many re-renders | 무한 루프 | useEffect 의존성 확인 |
| Cannot update unmounted | 비동기 처리 | cleanup 함수, AbortController |

### React Native
| 에러 | 원인 | 해결 |
|-----|------|------|
| Native module not found | 링킹 안됨 | pod install, rebuild |
| Network request failed | 네트워크 설정 | iOS ATS, Android cleartext |
| null is not an object | 초기 렌더링 | 조건부 렌더링, 로딩 상태 |

---
name: debugging

## HTTP 에러 빠른 진단

```
400 Bad Request     → 요청 데이터 형식 확인
401 Unauthorized    → 인증 토큰 확인
403 Forbidden       → 권한 확인
404 Not Found       → URL 경로 확인
500 Internal Server → 서버 로그 확인
502 Bad Gateway     → 프록시/서버 상태 확인
503 Service Unavailable → 서버 과부하/점검
```

---
name: debugging

## 디버깅 명령어

```bash
# 로그 확인
tail -f logs/app.log
grep -r "ERROR" ./logs/

# 포트 확인
lsof -i :3000
netstat -tlnp | grep 3000

# 프로세스 확인
ps aux | grep node
ps aux | grep python

# API 테스트
curl -v http://localhost:3000/api/health

# Git 최근 변경
git diff HEAD~1
git log --oneline -10
```

---
name: debugging

## 출력 형식

```markdown
## 🐛 디버깅 리포트

### 문제 요약
[한 줄 요약]

### 에러 분석
- **유형**: [에러 유형]
- **위치**: [파일:라인]
- **직접 원인**: [원인]
- **근본 원인**: [왜 발생했는지]

### 해결책
```[언어]
// 수정 코드
```

### 검증 방법
[해결됐는지 확인하는 방법]

### 예방책
[재발 방지를 위한 제안]
```

---
name: debugging

## 전문 에이전트 연계

복잡한 디버깅이 필요한 경우 로컬 Codex 에이전트 설정을 먼저 확인합니다.
- 위치: `~/.codex/agents/`
