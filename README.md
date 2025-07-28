# PaceBook-backend 개발컨벤션

# 1. 프로젝트구조 및 폴더 구성

## 기본폴더 구조

```bash
pacebook-backend/
│
├── config/                
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py         
│   └── wsgi.py / asgi.py
│
├── common/
├── users/
├── community/
├── app/
│
├── manage.py
└── README.md
```

## 앱 디렉토리 내부구조

```bash
community/
├── __init__.py
├── models.py
├── admin.py
├── serializers.py
├── views.py
├── urls.py
├── tests/
│   ├── __init__.py
│   ├── test_models.py
│   ├── test_views.py
│   └── test_serializers.py
└── migrations/
        └── __init__.py
```

## 테스트 디렉토리 분리전략

- 각 앱 내부에 `tests/` 폴더를 만들고, 기능 단위로 테스트 파일을 나눈다.
- 공통 테스트 유틸리티는 최상위 `tests/` 또는 `common/tests/`에 둘 수 있다.
- 파일 명에 `test_`붙여야 실행됨

예:

```bash
users/
└── tests/
	├── test_models.py
	├── test_views.py
	└── factories.py
```

# 2. 코딩 스타일 가이드

## 파일별 구성 순서

```python
# 표준
import os
import datetime

#django
from django.urls import path

# 서드파티
from rest_framework import serializers

# 로컬
from users.models import User

```

## 네이밍 컨벤션

| 용도 | 네이밍 예시 | 규칙 |
| --- | --- | --- |
| 변수 | `user_name`, `is_active` | `snake_case` |
| 함수 | `get_user_profile()` | `snake_case` |
| 클래스 | `UserSerializer`, `RunLogViewSet` | `PascalCase` |
| 상수 | `MAX_LENGTH = 50` | `UPPER_SNAKE_CASE` |
| 파일 이름 | `serializers.py`, `test_views.py` | `snake_case` |

# 3. GIT 컨벤션

## Branch 전략

| 브랜치 | 역할 |
| --- | --- |
| `main` | 운영(배포) 브랜치 |
| `dev` | 통합 개발 브랜치 |
| `feature/*` | 기능 개발 브랜치 |
| `hotfix/*` | 운영 긴급 수정 |
| `release/*` | 배포 준비용 브랜치 (선택사항) |

### 흐름 요약

1. 모든 개발은 `feature/*` 브랜치에서 시작한다.
2. PR을 통해 `dev`으로 merge한다.
3. 운영 배포 시 `main`으로 merge → 태그 추가 및 릴리즈

예시: feature/community

## Commit 메세지 컨벤션

| Type | 설명 | 예시 |
| --- | --- | --- |
| `feat` | 새로운 기능 추가 | feat(user): 로그인 기능 구현 |
| `fix` | 버그 수정 | fix(post): 댓글 등록 시 오류 수정 |
| `docs` | 문서 수정 (코드 변화 없음) | docs(readme): 사용법 예시 추가 |
| `style` | 코드 스타일 변경 (공백, 세미콜론 등) | style: prettier 적용 및 세미콜론 정리 |
| `refactor` | 리팩토링 (기능 변화 없음) | refactor(auth): 중복 로직 함수화 |
| `perf` | 성능 개선 |  |
| `test` | 테스트 코드 추가/수정 | test(comment): 댓글 API 테스트 코드 추가 |
| `build` | 빌드 관련 수정 (의존성, 설정 등) | build: dotenv 패키지 추가 |
| `ci` | CI 설정 관련 변경 |  |
| `chore` | 기타 변경사항 (예: 패키지 수정, 주석 등) | chore: .gitignore 파일 업데이트 |
| `revert` | 이전 커밋 되돌림 | revert: feat(user): 로그인 기능 구현 |