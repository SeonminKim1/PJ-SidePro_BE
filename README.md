![image](https://user-images.githubusercontent.com/87006912/182738130-a7c87bdf-0522-4382-b6d4-8ec2e38ef6b3.png)

## :owl: SidePro (SideProject)
- 개발자를 위한 사이드 프로젝트 공유 플랫폼 서비스 (with. 커피챗을 곁들인) 

## :panda_face: Introduction
- **주제** : 사이드 프로젝트 공유 플랫폼 (with. 커피챗)
- **기간** : 2022.07.07 (목) ~ 2022.08.04 (목)
- **Team** : 김선민 ([Github](https://github.com/SeonminKim1)), 김민기 ([Github](https://github.com/kmingky)), 박재현 ([Github](https://github.com/Aeius)), 황신혜 ([Github](https://github.com/hwangshinhye)) 

<hr>

## 📚 Project Structure
![image](https://user-images.githubusercontent.com/87006912/182737967-eb7e3ae2-1e8d-46d0-8a9f-241f027cf656.png)

<hr>

## :handshake: Project-Rules
#### Scheduling & API 
- [Git Project Link](https://github.com/SeonminKim1/SMOPS-BE/projects/1) / [간트차트 Link](https://docs.google.com/spreadsheets/d/1_1Sx46dnKnI8_DLJQzAASMSr7u525RFjm2Iat0beU14/edit#gid=375979933) / [API Design Link](https://www.notion.so/12cc32feafcb4e81b2377f07b04a6824?v=5b05b526a18e434cb44d62f044b26bf7)
- [Git BE Issue Link](https://github.com/SeonminKim1/SMOPS-BE/issues) / [Git FE Issue Link](https://github.com/SeonminKim1/SMOPS-FE/issues)

#### Branch Info
- main : LocalHost 실행 branch
- publish : EC2 Hosting 실행 Branch

#### Repository Info
- [SMOPS-FE Project](https://github.com/SeonminKim1/SMOPS-FE)

#### Figma Mock-up
![ss](https://user-images.githubusercontent.com/87006912/182737861-0cbc69de-68a6-4257-8ff8-d9b1ce50d381.png)


#### DB Modeling   
![SIDEPRO_DB_FINAL](https://user-images.githubusercontent.com/87006912/182737490-554e9094-6439-4e14-8608-e60c4af2445c.png)

<hr>

## 👉 Getting-Started

``` Run
## FrontEnd Settings
$ git clone https://github.com/SeonminKim1/SMOPS-FE
$ cd SMOPS-FE/
- Install vscode extensions : Live Server 
- Run Live Server

## Backend Settings
$ git clone https://github.com/SeonminKim1/SMOPS-BE
$ cd SMOPS-BE/
$ pip install -r requirements.txt

- Make 'my_settings.py' from 'ex_my_settings.py
$ python manage.py makemigrations
$ python manage.py migrations
$ python manage.py runserver

# if you apply code convention by black & isort
$ python auto_cleancode.py
```

<hr>

## 👉 Structure
```
┌─SIDEPRO
├── sidepro             // project
│   ├── urls.py         // base url
│   ├── asgi.py         // chat route setting
│   ├── settings.py     // setting
│   └── ...
├── project             // app
│   ├── models.py       // DB Model - project, comment
│   ├── views.py        // View Functions
│   ├── serializers.py  // Serializers
│   ├── tests.py        // Test Code
│   ├── pagination.py   // pagination
│   └── ...
├── chat                // app
│   ├── models.py       // DB Model - status, room, chat
│   ├── views.py        // View Functions
│   ├── serializers.py  // Serializers
│   ├── tests.py        // Test Code
│   ├── constants.py    // Constants
│   ├── consumers.py    // Consumer
│   ├── routung.py      // Routing
│   └── ...
├── ai                  // app
│   ├── views.py        // View Functions
│   ├── serializers.py  // Serializers
│   ├── tests.py        // Test Code
│   ├── cron.py         // Crontab
│   └── ...
├── user                // app
│   ├── models.py       // DB Model - user, userprofile, ...
│   ├── views.py        // View Functions
│   ├── serializers.py  // Serializers
│   ├── tests.py        // Test Code
│   ├── constants.py    // Constants
│   └── ...
├── _utils 
│   ├── auto_clean_pyc_migrate.py    // Migrations
│   ├── auto_cleancode.py            // Run black, isort
│   ├── auto.runserver.py            // Run Server
│   ├── query_utils.py               // Query Debuger
│   └── set_basedb.sql               // Base DB Data
│
├── .github\workflow
│   └── be_cicd.yml     // CI/CD PIPE LINE    
│
├── log 
│   └── a.txt           // Save crontab log
│
├── nginx 
│   ├── nginx.conf      // nginx
│   └── Dokerfile       // nginx Dokerfile
│
├── Dockerfile          // Dokerfile
├── docker-compose.yaml // Doker-Compose
├── **manage.py**        
└── requirements.txt
```

<hr>


## :computer: Development

#### Login/Join Page
- 회원가입,로그인 vaildation
- 로그인 JWT Token 부여
- 소셜로그인(미구현)

#### 메인 페이지
- 배너 출력
1) github-repo 2)스파르타 3)event예시 4) 설문
- 프로젝트 리스트 출력(pagination)
- 프로젝트 북마크
- 프로젝트 작성한 유저와 커피챗하기
- 프로젝트 유저페이지로 이동
- 프로젝트 필터링 별 조회
   - 조회순, 최신순, 인기순(북마크)
- 프로젝트 기술스택으로 검색
- 추천 프로젝트 리스트 출력

#### 프로젝트 상세 페이지
- 프로젝트 정보 조회
- 프로젝트 북마크
- 프로젝트 수정, 삭제(작성자만)
- 댓글 작성
- 댓글 수정, 삭제(작성자만)

#### 프로필 페이지(마이/유저 페이지)
- 프로필 정보 조회
- 나/유저의 프로젝트 조회
- 나/유저의 북마크한 프로젝트 조회
- 해당 유저와 커피챗하기
- 프로젝트 작성한 유저와 커피챗하기
- 나의 프로필 정보 수정
    - 프로필 수정, 삭제(로그인 유저만)

#### 커피챗(aside)
- 채팅방 목록 조회
- 채팅방 삭제
- 유저 프로필 조회
- 실시간 채팅


#### AWS Infra
- AWS EC2 이용한 외부 Publish 배포
- AWS S3 FE 버켓 2개 이용하여 각각 정적 웹 호스팅, 업로드 파일 저장소
- AWS IAM 부여하여 Infra Team 공동 관리
- AWS RDS 이용하여 DataBase 속도와 안정성 확보 
- AWS ROUTER 53 도메인 등록하여 가독성 접근성 증가

#### Doker


#### nginx / gunicorn


<hr>

## 👉 시연 화면
#### 회원가입, 로그인 화면
![image](https://user-images.githubusercontent.com/33525798/173514356-84840d07-2425-4095-b9fa-07d50a19bc0d.png)

#### 유화 메인 페이지, 유화 상세 페이지
![image](https://user-images.githubusercontent.com/33525798/173514477-228b4897-bee0-491e-847c-5720d11a5eb4.png)

#### 마이 갤러리 페이지
![image](https://user-images.githubusercontent.com/33525798/173514527-8e456009-0dcb-4e5d-890a-e476ef4331fb.png)

#### 유화 만들기 페이지 (AI)
![image](https://user-images.githubusercontent.com/33525798/173514527-8e456009-0dcb-4e5d-890a-e476ef4331fb.png)



