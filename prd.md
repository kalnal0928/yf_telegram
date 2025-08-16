# Product Requirements Document (PRD)
## US Stock Monitor with Telegram Notification System

### 1. Project Overview

#### 1.1 Purpose
개발자가 관심 있는 미국 주식의 실시간 정보를 자동으로 조회하고, 정해진 시간에 텔레그램으로 알림을 받을 수 있는 자동화 시스템 개발

#### 1.2 Target User
- 미국 주식 투자자
- 주식 정보를 정기적으로 모니터링하고 싶은 개인 투자자
- 자동화된 주식 알림 시스템이 필요한 사용자

#### 1.3 Business Goals
- 주식 정보 모니터링의 자동화
- 실시간 주식 데이터에 대한 접근성 향상
- 투자 의사결정을 위한 정기적인 정보 제공

### 2. Functional Requirements

#### 2.1 Core Features

##### 2.1.1 주식 데이터 조회 기능
- **기능**: yfinance 라이브러리를 사용한 미국 주식 데이터 조회
- **대상 주식**: 사용자 정의 주식 티커 리스트
- **조회 데이터**:
  - 현재 주가
  - 전일 종가
  - 등락률 (%)
  - 등락액 ($)
  - 거래량
  - 52주 최고/최저가
  - 시가총액
  - P/E 비율

##### 2.1.2 데이터 포맷팅 기능
- **기능**: 조회된 데이터를 텔레그램 메시지 형태로 포맷팅
- **포맷 요구사항**:
  - 읽기 쉬운 텍스트 형태
  - 이모지를 활용한 시각적 표현 (📈📉💰)
  - 상승/하락에 따른 색상 구분 (텔레그램 마크다운)
  - 한국 시간 기준 타임스탬프

##### 2.1.3 텔레그램 전송 기능
- **기능**: 포맷된 주식 정보를 텔레그램 봇을 통해 전송
- **전송 대상**: 개인 또는 그룹 채팅
- **메시지 형태**: 텍스트 메시지 + 마크다운 포맷팅

#### 2.2 Automation Features

##### 2.2.1 스케줄링 기능
- **기능**: GitHub Actions를 사용한 자동 실행
- **실행 시간**: 
  - 평일 오전 9:30 AM EST (미국 장 시작 전)
  - 평일 오후 4:00 PM EST (미국 장 마감)
  - 토요일 오전 9:00 AM KST (주간 요약)
- **예외 처리**: 미국 공휴일 및 주말 제외

##### 2.2.2 에러 핸들링
- **네트워크 에러**: 재시도 로직 구현 (3회 시도)
- **API 한도 초과**: 적절한 딜레이 및 에러 로깅
- **텔레그램 전송 실패**: 대체 알림 방법

### 3. Technical Requirements

#### 3.1 Development Stack
- **언어**: Python 3.9+
- **주요 라이브러리**:
  - `yfinance`: 주식 데이터 조회
  - `python-telegram-bot`: 텔레그램 봇 API
  - `pandas`: 데이터 처리
  - `datetime`: 시간 처리
  - `requests`: HTTP 요청

#### 3.2 Infrastructure
- **CI/CD**: GitHub Actions
- **Repository**: GitHub Public/Private Repository
- **Secrets Management**: GitHub Secrets
  - `TELEGRAM_BOT_TOKEN`
  - `TELEGRAM_CHAT_ID`

#### 3.3 Configuration Management
- **설정 파일**: `config.yaml` 또는 환경변수
- **주식 티커 리스트**: 쉽게 수정 가능한 형태
- **알림 시간**: 설정 가능한 스케줄

### 4. Data Requirements

#### 4.1 Input Data
- **주식 티커 심볼**: ["AAPL", "GOOGL", "MSFT", "AMZN", "TSLA"] (예시)
- **텔레그램 봇 토큰**: Telegram BotFather에서 발급
- **채팅 ID**: 개인 또는 그룹 채팅 ID

#### 4.2 Output Data Format
```
📊 미국 주식 현황 (2024-01-15 09:30 EST)

🍎 AAPL (Apple Inc.)
💰 $185.25 (+2.15, +1.17%) 📈
📈 52W High: $199.62 | 📉 52W Low: $164.08
📊 Volume: 45.2M | P/E: 28.5

🔍 GOOGL (Alphabet Inc.)
💰 $142.80 (-1.05, -0.73%) 📉
📈 52W High: $151.55 | 📉 52W Low: $101.88
📊 Volume: 22.8M | P/E: 25.2
```

### 5. User Stories

#### 5.1 Primary User Stories
1. **개발자로서**, 내가 관심 있는 주식 목록을 설정하여 정기적으로 모니터링하고 싶다.
2. **투자자로서**, 미국 장 시작 전과 마감 후에 주식 정보를 자동으로 받고 싶다.
3. **사용자로서**, 텔레그램을 통해 간편하게 주식 정보를 확인하고 싶다.

#### 5.2 Secondary User Stories
1. **개발자로서**, 시스템이 안정적으로 동작하는지 모니터링하고 싶다.
2. **사용자로서**, 주말에 주간 주식 성과 요약을 받고 싶다.

### 6. System Architecture

#### 6.1 Component Diagram
```
GitHub Repository
├── src/
│   ├── stock_fetcher.py      # yfinance 주식 데이터 조회
│   ├── telegram_sender.py    # 텔레그램 메시지 전송
│   ├── data_formatter.py     # 데이터 포맷팅
│   └── main.py              # 메인 실행 스크립트
├── config/
│   ├── stocks.yaml          # 주식 티커 설정
│   └── schedule.yaml        # 스케줄 설정
├── .github/
│   └── workflows/
│       └── stock_alert.yml  # GitHub Actions 워크플로우
├── requirements.txt         # Python 의존성
└── README.md               # 프로젝트 문서
```

#### 6.2 Data Flow
1. GitHub Actions 스케줄러 트리거
2. Python 스크립트 실행
3. yfinance로 주식 데이터 조회
4. 데이터 포맷팅 및 가공
5. 텔레그램 봇을 통한 메시지 전송
6. 로그 기록 및 완료

### 7. Non-Functional Requirements

#### 7.1 Performance
- **응답 시간**: 전체 프로세스 5분 이내 완료
- **데이터 정확성**: yfinance API 데이터와 100% 일치
- **가용성**: 99% 이상 (GitHub Actions 가용성에 의존)

#### 7.2 Security
- **API 토큰 보안**: GitHub Secrets를 통한 안전한 저장
- **데이터 전송**: HTTPS를 통한 암호화된 통신
- **접근 제어**: 텔레그램 봇의 제한된 권한

#### 7.3 Maintainability
- **코드 구조**: 모듈화된 Python 코드
- **문서화**: 상세한 README 및 코드 주석
- **설정 관리**: YAML 기반 설정 파일

### 8. Testing Strategy

#### 8.1 Unit Testing
- 각 모듈별 단위 테스트
- Mock 데이터를 사용한 텔레그램 전송 테스트
- 데이터 포맷팅 검증

#### 8.2 Integration Testing
- yfinance API 연동 테스트
- 텔레그램 봇 API 연동 테스트
- 전체 워크플로우 통합 테스트

### 9. Deployment Plan

#### 9.1 Phase 1: MVP Development (1주)
- 기본 주식 조회 기능 개발
- 텔레그램 전송 기능 구현
- GitHub Actions 기본 스케줄링

#### 9.2 Phase 2: Enhancement (1주)
- 에러 핸들링 강화
- 데이터 포맷팅 개선
- 주간 요약 기능 추가

#### 9.3 Phase 3: Optimization (1주)
- 성능 최적화
- 모니터링 및 로깅 개선
- 문서화 완료

### 10. Risk Assessment

#### 10.1 Technical Risks
- **yfinance API 제한**: Rate limiting 대응 방안 필요
- **GitHub Actions 한계**: 무료 계정의 실행 시간 제한
- **텔레그램 API 변경**: API 버전 업데이트 대응

#### 10.2 Mitigation Strategies
- API 호출 간격 조절 및 재시도 로직 구현
- 효율적인 워크플로우 설계
- 정기적인 의존성 업데이트 및 테스트

### 11. Success Metrics

#### 11.1 Primary Metrics
- **시스템 가용성**: 95% 이상 성공적인 실행
- **데이터 정확성**: 100% 정확한 주식 데이터 전송
- **알림 적시성**: 설정된 시간에 정확한 전송

#### 11.2 Secondary Metrics
- **사용자 만족도**: 개인 피드백 기반
- **시스템 안정성**: 에러 발생률 5% 이하
- **유지보수성**: 기능 추가/수정 용이성