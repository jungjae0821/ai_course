# 할 일 관리(Todo) 웹앱 스펙 명세서

## 1. 개요
사용자가 할 일을 등록하고, 완료 여부를 확인하며, 목록을 관리할 수 있는 심플한 웹 애플리케이션입니다. 복잡한 기능보다는 핵심적인 Todo 기능에 집중하여 빠르고 가볍게 동작하는 것을 목표로 합니다.

## 2. 기술
- **Language:** Python 3.x
- **Framework:** Flask
- **Database:** SQLite
- **Frontend:** HTML5, CSS3 (Vanilla CSS)

## 3. 파일 구성
- `app.py`: Flask 애플리케이션의 메인 엔트리 포인트 및 라우팅 로직
- `database.py`: SQLite 연결 관리 및 DB CRUD 함수 모음
- `models.py`: Todo 데이터 객체 모델 정의
- `static/css/style.css`: 앱의 디자인을 담당하는 순수 CSS 파일
- `templates/index.html`: 사용자 인터페이스를 위한 메인 HTML 템플릿

## 4. 동작 규칙 (Routing)

| Method | Endpoint | Input (Payload/Params) | Expected Result |
| :--- | :--- | :--- | :--- |
| GET | `/` | 없음 | 전체 Todo 목록 페이지 출력 |
| POST | `/add` | `title` (string) | 새로운 Todo 생성 후 `/`로 리다이렉트 |
| POST | `/toggle/<id>` | `id` (int) | 해당 ID의 `is_completed` 상태 반전 후 `/`로 리다이렉트 |
| POST | `/delete/<id>` | `id` (int) | 해당 ID의 Todo 삭제 후 `/`로 리다이렉트 |

## 5. 화면
- **메인 화면 (`/`)**:
  - 상단: 새로운 할 일을 입력할 수 있는 입력창과 '추가' 버튼
  - 중앙: 할 일 목록 (최신순 정렬)
    - 각 항목은 [완료 체크박스], [제목], [생성 시각], [삭제 버튼]으로 구성
    - 완료된 항목은 취소선(strikethrough)이 그어지고 글자 색이 흐릿하게 표시됨
  - 하단: 깔끔한 푸터 또는 여백

## 6. 테스트 (Flask `test_client` 기준)

| 요청 (Request) | 기대하는 결과 (Expected Result) |
| :--- | :--- |
| GET `/` | HTTP 200 및 빈 목록(또는 초기 데이터) 페이지 응답 |
| POST `/add` (title="Test Task") | HTTP 302 리다이렉트 및 DB에 데이터 1건 생성 확인 |
| POST `/add` (title="") | HTTP 302 혹은 에러 페이지 및 DB에 데이터 추가 실패 확인 |
| POST `/add` (title=" " - 공백만 입력) | HTTP 302 혹은 에러 페이지 및 DB에 데이터 추가 실패 확인 |
| POST `/add` (title=매우 긴 문자열) | HTTP 200 및 정상적인 길이로 잘리거나 저장 확인 |
| POST `/toggle/1` (존재하는 ID) | HTTP 302 및 해당 ID의 `is_completed` 값이 반전됨 |
| POST `/toggle/999` (없는 ID) | HTTP 404 혹은 에러 페이지 반환 |
| POST `/delete/1` (존재하는 ID) | HTTP 302 및 DB에서 해당 데이터 삭제 확인 |
| POST `/delete/999` (없는 ID) | HTTP 404 혹은 에러 페이지 반환 |
| GET `/non-existent-route` | HTTP 404 Not Found 반환 |

## 7. 완료 전 점검
- [ ] 모든 할 일은 최신 생성 순으로 정렬되어 나타나는가?
- [ ] 완료 체크 시 UI에 즉각적으로 취소선이 반영되는가?
- [ ] 삭제 시 `confirm()` 창이 나타나 사용자에게 확인을 받는가?
- [ ] SQLite 데이터베이스 파일(`todo.db`)이 정상적으로 생성되고 동작하는가?
- [ ] CSS 프레임워크 없이 순수 CSS로 레이아웃이 깨지지 않는가?

## 8. 하지 않는 것
- 사용자 인증 및 로그인 기능 (Login/Signup)
- 기존 항목의 내용 수정 기능 (Update Title)
- 외부 CSS 프레임워크 사용 (Bootstrap, Tailwind 등)
- 자바스크립트 프레임워크 사용 (React, Vue 등)
