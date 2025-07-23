# 📄 Django 대시보드 웹사이트 프로젝트 (Pybo)

## 🖥️ 프로젝트 소개

이 프로젝트는 **Django** 프레임워크를 사용하여 개발된 간단한 **대시보드 웹사이트**입니다.

Django의 기본 개념을 익히고 웹 애플리케이션의 전체적인 흐름을 파악하는 것을 목표로 제작되었습니다.

## 🛠️ 기술 스택

- **Backend**: Django
- **Language**: Python
- **Database**: SQLite (기본 설정)

## 🏃‍♂️ 로컬에서 프로젝트 실행하기

이 프로젝트를 로컬 컴퓨터에서 실행하려면 다음 단계를 따르세요.

### 1. 사전 준비

- **Python 3.x** 버전이 설치되어 있어야 합니다.
- Python 패키지 관리자인 **pip**가 설치되어 있어야 합니다.

### 2. 프로젝트 복제 및 설정

```bash
# 1. 프로젝트를 복제(clone)합니다.
git clone <저장소_URL>

# 2. 프로젝트 디렉터리로 이동합니다.
cd projects

# 3. 가상환경을 생성합니다.
python -m venv venv

# 4. 가상환경을 활성화합니다.
# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate
```

### 3. 의존성 패키지 설치

프로젝트 실행에 필요한 모든 패키지를 `requirements.txt` 파일을 통해 한 번에 설치합니다.

```bash
pip install -r requirements.txt
```

### 4. 데이터베이스 설정 (선택사항)

```bash
# 1. 데이터베이스 스키마를 생성(migrate)합니다.
python manage.py migrate

# 2. 관리자(superuser) 계정을 생성합니다.
python manage.py createsuperuser
```

### 5. 개발 서버 실행

```bash
python manage.py runserver
```

- 서버가 성공적으로 실행되면, 웹 브라우저에서 `http://127.0.0.1:8000/` 주소로 접속하여 확인할 수 있습니다.

## 📂 디렉토리 구조

```text
📦 projects/                                    # 프로젝트 루트
├── .gitignore                                   # Git 추적 제외 파일 목록
├── requirements.txt                             # pip 패키지 의존성 목록
├── db.sqlite3                                   # SQLite 데이터베이스 파일
├── manage.py                                    # Django 프로젝트 관리 스크립트 (명령행 도구)
├── README.md                                    # 프로젝트 설명 및 가이드 문서
├── config/                                      # Django 프로젝트 설정 디렉터리
│   ├── __init__.py                              # Python 패키지 초기화 파일
│   ├── asgi.py                                  # ASGI 서버 진입점
│   ├── settings.py                              # Django 전체 설정 파일
│   ├── urls.py                                  # 프로젝트 전체 URL 라우팅
│   ├── wsgi.py                                  # WSGI 서버 진입점
│   └── __pycache__/                             # Python 바이트코드 캐시 폴더
├── mysite/                                      # 실제 앱 소스 및 의존성 파일 위치
│   └── pybo/                                    # pybo Django 앱
│       ├── __init__.py                          # Python 패키지 초기화 파일
│       ├── admin.py                             # Django 관리자 페이지 설정
│       ├── apps.py                              # 앱 설정 클래스
│       ├── models.py                            # 데이터베이스 모델 정의
│       ├── tests.py                             # 단위 테스트 코드
│       ├── urls.py                              # 앱 내부 URL 라우팅
│       ├── views.py                             # 뷰(로직) 함수/클래스
│       ├── __pycache__/                         # Python 바이트코드 캐시 폴더
│       └── migrations/                          # DB 마이그레이션 파일
│           ├── __init__.py                      # 마이그레이션 패키지 초기화
│           └── __pycache__/                     # 마이그레이션 바이트코드 캐시
├── static/                                      # 정적 파일(CSS, JS 등)
│   ├── dashboard.css                            # 대시보드 스타일 CSS
│   ├── post_list.css                            # 게시글 목록 스타일 CSS
│   └── js/
│       └── theme.js                             # 다크/라이트 테마 JS
└── templates/                                   # HTML 템플릿 폴더
    ├── dashboard.html                           # 대시보드 페이지 템플릿
    └── post_list.html                           # 게시글 목록 페이지 템플릿
```

## 📜 라이선스 및 연락처

- 본 프로젝트는 학습 및 포트폴리오 용도로 작성되었습니다.
- 문의: `ataraxia7899@gmail.com`
