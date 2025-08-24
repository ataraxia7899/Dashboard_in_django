# 📄 Django 대시보드 웹사이트 프로젝트 (Pybo)

## 🖥️ 프로젝트 소개

이 프로젝트는 **Django** 프레임워크를 사용하여 개발된 간단한 **대시보드 웹사이트**입니다.

Django의 기본 개념을 익히고 웹 애플리케이션의 전체적인 흐름을 파악하는 것을 목표로 제작되었습니다.

## 🛠️ 기술 스택

- **Backend**: Django
- **Language**: Python
- **Database**: SQLite (기본 설정), mariaDB

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

# 2. 관리자(superuser) 계정을 생성합니다. (선택사항)
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
├──📄 .gitignore                                   # Git 추적 제외 파일 목록
├──📄 requirements.txt                             # pip 패키지 의존성 목록
├──📄 db.sqlite3                                   # SQLite 데이터베이스 파일
├──📄 manage.py                                    # Django 프로젝트 관리 스크립트 (명령행 도구)
├──📄 README.md                                    # 프로젝트 설명 및 가이드 문서
├──📂 config/                                      # Django 프로젝트 설정 디렉터리
│   ├──📄 __init__.py                              # Python 패키지 초기화 파일
│   ├──📄 asgi.py                                  # ASGI 서버 진입점
│   ├──📄 settings.py                              # Django 전체 설정 파일
│   ├──📄 urls.py                                  # 프로젝트 전체 URL 라우팅
│   ├──📄 wsgi.py                                  # WSGI 서버 진입점
│   └──📂 __pycache__/                             # Python 바이트코드 캐시 폴더
├──📂 mysite/                                      # 실제 앱 소스 및 의존성 파일 위치
│   └──📂 pybo/                                    # pybo Django 앱
│       ├──📄 __init__.py                          # Python 패키지 초기화 파일
│       ├──📄 admin.py                             # Django 관리자 페이지 설정
│       ├──📄 apps.py                              # 앱 설정 클래스
│       ├──📄 forms.py                             # Django 폼 정의
│       ├──📄 models.py                            # 데이터베이스 모델 정의
│       ├──📄 tests.py                             # 단위 테스트 코드
│       ├──📄 urls.py                              # 앱 내부 URL 라우팅
│       ├──📄 views.py                             # 뷰(로직) 함수/클래스
│       ├──📄 __pycache__/                         # Python 바이트코드 캐시 폴더
│       └──📂 migrations/                          # DB 마이그레이션 파일
│           ├──📄 __init__.py                      # 마이그레이션 패키지 초기화
│           └──📂 __pycache__/                     # 마이그레이션 바이트코드 캐시
├──📂 static/                                      # 정적 파일(CSS, JS, 이미지 등)
│   ├──📄 dashboard.css                            # 대시보드 전용 스타일
│   ├──📄 post_list.css                            # 게시글 목록 전용 스타일
│   └──📂 js/                                      # JavaScript 파일 폴더
│       └──📄 theme.js                             # 다크/라이트 테마 전환 스크립트
└──📂 templates/                                   # HTML 템플릿 폴더
    ├──📄 dashboard.html                           # 대시보드 페이지
    ├──📄 post_list.html                           # 게시글 목록 페이지
    ├──📄 post_detail.html                         # 게시글 상세 페이지
    ├──📄 post_form.html                           # 게시글 생성/수정 폼
    ├──📄 comment_form.html                        # 댓글 수정 폼
    ├──📄 login.html                               # 로그인 페이지
    ├──📄 signup.html                              # 회원가입 페이지
    └──📄 user_list.html                           # (관리자) 사용자 목록 페이지
```

## 💾 DB 구성 (Database Schema)

`migrations` 폴더의 마이그레이션 파일을 기반으로 생성된 데이터베이스 모델의 구조는 다음과 같습니다.

#### `User`
사용자 정보를 저장하는 모델입니다. Django의 기본 `auth.User` 모델 대신 커스텀 모델을 사용합니다.

| 필드명 | 타입 | 설명 |
| --- | --- | --- |
| `id` | AutoField | 기본 키 (PK) |
| `username` | CharField(50) | 사용자 이름 (고유) |
| `join_date` | DateTimeField | 가입일 (자동 생성) |

#### `Post`
게시글 정보를 저장하는 모델입니다.

| 필드명 | 타입 | 설명 |
| --- | --- | --- |
| `id` | BigAutoField | 기본 키 (PK) |
| `user` | ForeignKey(User) | 작성자 (User 모델과 관계, 작성자 삭제 시 `NULL`로 설정) |
| `title` | CharField(200) | 게시글 제목 |
| `content` | TextField | 게시글 내용 |
| `created_at` | DateTimeField | 작성일 (자동 생성) |
| `attachment` | FileField | 첨부 파일 (선택 사항) |

#### `Comment`
게시글에 대한 댓글 정보를 저장하는 모델입니다.

| 필드명 | 타입 | 설명 |
| --- | --- | --- |
| `id` | BigAutoField | 기본 키 (PK) |
| `user` | ForeignKey(User) | 작성자 (User 모델과 관계, 작성자 삭제 시 댓글도 삭제) |
| `post` | ForeignKey(Post) | 원본 게시글 (Post 모델과 관계, 게시글 삭제 시 댓글도 삭제) |
| `content` | TextField | 댓글 내용 |
| `created_at` | DateTimeField | 작성일 (자동 생성) |

#### `PostLike`
사용자가 '좋아요'를 누른 게시글 정보를 저장하는 중개 모델입니다.

| 필드명 | 타입 | 설명 |
| --- | --- | --- |
| `id` | BigAutoField | 기본 키 (PK) |
| `user` | ForeignKey(User) | 좋아요를 누른 사용자 |
| `post` | ForeignKey(Post) | 좋아요를 받은 게시글 |
| `created_at` | DateTimeField | 생성일 (자동 생성) |
| `(user, post)` | UniqueConstraint | 사용자는 하나의 게시글에 한 번만 '좋아요'를 누를 수 있습니다. |

#### `Bookmark`
사용자가 북마크한 게시글 정보를 저장하는 중개 모델입니다.

| 필드명 | 타입 | 설명 |
| --- | --- | --- |
| `id` | BigAutoField | 기본 키 (PK) |
| `user` | ForeignKey(User) | 북마크한 사용자 |
| `post` | ForeignKey(Post) | 북마크된 게시글 |
| `created_at` | DateTimeField | 생성일 (자동 생성) |
| `(user, post)` | UniqueConstraint | 사용자는 하나의 게시글을 한 번만 북마크할 수 있습니다. |

#### `DailyVisitor`
일일 방문자 수를 기록하는 모델입니다.

| 필드명 | 타입 | 설명 |
| --- | --- | --- |
| `id` | BigAutoField | 기본 키 (PK) |
| `date` | DateField | 날짜 (고유) |
| `count` | PositiveIntegerField | 해당 날짜의 방문자 수 |

#### `ActivityLog`
사용자의 주요 활동(가입, 글 작성 등)을 기록하는 모델입니다.

| 필드명 | 타입 | 설명 |
| --- | --- | --- |
| `id` | BigAutoField | 기본 키 (PK) |
| `user` | ForeignKey(User) | 활동을 수행한 사용자 |
| `activity_type` | CharField(10) | 활동 유형 (`signup`, `post`, `comment`, `like`) |
| `message` | CharField(255) | 활동 내용 메시지 |
| `created_at` | DateTimeField | 활동 시간 (자동 생성) |

## 실행 결과

### 대시보드 페이지
<img width="503" height="1495" alt="Image" src="https://github.com/user-attachments/assets/9b4df953-154f-454c-a572-35ccb28c79ed" />

### 대시보드 페이지 (다크모드)
<img width="503" height="1495" alt="Image" src="https://github.com/user-attachments/assets/0b8d5e84-9299-476a-8694-7755cb483aa3" />

### 최근 게시글 페이지
<img width="503" height="1113" alt="Image" src="https://github.com/user-attachments/assets/59af02aa-24be-4e30-9634-fb74bbaafd12" />

### 최근 게시글 페이지 (다크모드)
<img width="503" height="1113" alt="Image" src="https://github.com/user-attachments/assets/c7859727-e0b1-44f8-ae3c-bc6542b796b3" />

### 시연영상 : <a href="https://youtu.be/4pHxq73OK7s?si=FBBCOhemrYNmPGEX" target="_blank">프로젝트 시연영상</a>

## 📜 라이선스 및 연락처

- 본 프로젝트는 학습 및 포트폴리오 용도로 작성되었습니다.
- 문의: `ataraxia7899@gmail.com`
