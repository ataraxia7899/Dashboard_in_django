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
cd mysite

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

### 4. 데이터베이스 설정

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

```
📦 mysite/
├── 📄 manage.py             # Django 프로젝트 관리 스크립트
├── 📂 config/               # 프로젝트 설정 디렉토리
│   ├── settings.py          # 프로젝트 설정
│   └── urls.py              # 최상위 URL 설정
├── 📂 pybo/                 # 'pybo' 애플리케이션
│   ├── migrations/          # 데이터베이스 마이그레이션 파일
│   ├── templates/           # HTML 템플릿 (추가 필요)
│   ├── admin.py             # 관리자 페이지 설정
│   ├── apps.py              # 앱 설정
│   ├── models.py            # 데이터베이스 모델
│   ├── tests.py             # 테스트 코드
│   ├── urls.py              # 앱 내부 URL 설정
│   └── views.py             # 뷰(로직)
└── 📄 requirements.txt       # 의존성 패키지 목록
```

## 📜 라이선스 및 연락처

- 본 프로젝트는 학습 및 포트폴리오 용도로 작성되었습니다.
- 문의: `ataraxia7899@gmail.com`