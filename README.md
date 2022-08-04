![image](https://user-images.githubusercontent.com/33525798/182744743-535b6add-39db-494e-9bf6-cfbff10750df.png)

## :owl: SidePro (SideProject)
- 개발자를 위한 사이드 프로젝트 공유 플랫폼 서비스 (with. 커피챗을 곁들인) 


## :panda_face: Introduction
- **주제** : 사이드 프로젝트 공유 플랫폼 (with. 커피챗)
- **기간** : 2022.07.07 (목) ~ 2022.08.04 (목)
- **Team** : 김선민 ([Github](https://github.com/SeonminKim1)), 김민기 ([Github](https://github.com/kmingky)), 박재현 ([Github](https://github.com/Aeius)), 황신혜 ([Github](https://github.com/hwangshinhye)) 
- **FE Repo** : [Sidepro-FE](https://github.com/SeonminKim1/SidePro-FE)
- **시연 영상** : [링크](https://drive.google.com/file/d/1WMoeDu8JlXTZY_Iiehs2pSy-rCM_wPzb/view?usp=sharing)

<hr>


## 📚 Project Structure
![image](https://user-images.githubusercontent.com/33525798/182751102-b3ed9cf4-8f62-458c-b251-cf77179a5e90.png)

<hr>

## :handshake: Project-Rules
#### Scheduling & API 
- [간트차트 Link](https://docs.google.com/spreadsheets/d/1_1Sx46dnKnI8_DLJQzAASMSr7u525RFjm2Iat0beU14/edit#gid=375979933)
- [API Design Link](https://docs.google.com/spreadsheets/d/1_1Sx46dnKnI8_DLJQzAASMSr7u525RFjm2Iat0beU14/edit#gid=1977470109)
- [QuerySet Optimize Experiments](https://www.notion.so/8635a07654204f84886081270cd301a8?v=d31ed66cc67843ada777bcca4238f1f9)

#### Branch Info
- main : LocalHost 실행 branch
- publish : EC2 Hosting 실행 Branch

#### Figma Mock-up & DB Modeling
![image](https://user-images.githubusercontent.com/33525798/182744857-d3dc1e10-806f-4fe8-a459-1ece66ffe173.png)


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

#### 🎉 로그인/회원가입
- 기본 vaildation & 로그인 JWT Token 사용

#### 🎉 프로젝트 게시판
- 프로젝트 목록 조회 (Django-Pagination)
- 프로젝트 등록 (Toast UI Editor / Image Preview)
- 프로젝트 검색, 정렬 (기술 스택 기반 검색 / 조회순, 최신순, 인기순 정렬)
- 프로젝트 상세 조회 / 수정 / 삭제 (댓글 CRUD, 북마크 ON/OFF)

#### 🎉 커피챗 기능
- 채팅 Room 목록 (조회, 생성, 삭제)
- 채팅 소켓 연결에 따른 Room Status 관리 (Running, Pending, Stop)
- 채팅 유저 프로필 조회
- 실시간 채팅
   - Websocket & Django Channels 이용
   - Daphne ASGI 서버 => WS 프로토콜 요청 처리
   - Redis를 이용한 실시간 메시지 전송

#### 🎉 추천 시스템 기능
- User-Based 추천 시스템 ("나와 비슷한 기술 스택을 보유한 유저의 프로젝트" 추천)
- Django-CronTab을 이용한 유사도 계산 부하 방지 (1분마다 Query & 유사도 계산)
- 스토리
   - 1) CronTab이 1분마다 나와 유사한 기술 스택 보유한 유저간의 유사도 계산
   - 2) 유사도 계산 파일 csv 저장
   - 3) 사용자 요청시 해당 파일 읽어서 추천 프로젝트 결과 출력
   
#### 🎉 프로필 페이지(마이/유저 페이지)
- 마이(유저) 프로젝트 모아보기
- 북마크한 프로젝트 모아보기
- 유저 프로필 정보 조회
- 내 프로필 정보 조회 수정, 삭제

#### 🎉 AWS Infra & CI-CD
- AWS EC2 내 container 기반 Publish 배포
- AWS S3 FE 버켓 2개 이용하여 각각 정적 웹 호스팅, 업로드 파일 저장소
- AWS IAM 부여하여 Infra Team 공동 관리
- AWS RDS 이용하여 DataBase 속도와 안정성 확보 
- AWS ROUTER 53 도메인 등록하여 가독성, 접근성 증가
- GitActions 이용한 CI-CD 자동화 구축

#### 🎉 Nginx / Gunicorn / Daphne
- Nginx : Proxy 역할 
- Gunicorn : Django 배포용 WSGI서버 http protocol 요청 처리 (worker : 2)
- Daphne : Django 배포용 ASGI서버 WebSocket portocol 요청 처리

<hr>

## 👉 시연 화면
#### 🎉 첫 화면, 회원가입, 로그인 화면
![image](https://user-images.githubusercontent.com/33525798/182766448-b277aebb-2bf3-45ac-ba2e-4394131d7621.png)

#### 🎉 메인 페이지 (게시판)
![image](https://user-images.githubusercontent.com/33525798/182766477-2e087332-be7c-416d-9a4a-d29265667322.png)

#### 🎉 상세 페이지 (글 조회, 글 쓰기)
![image](https://user-images.githubusercontent.com/33525798/182768500-30e352b8-f443-422b-a4c0-50f51645b53e.png)

#### 🎉 마이(유저) 페이지
![image](https://user-images.githubusercontent.com/33525798/182767190-ec31f7ff-7d90-49b1-9c8e-0bd513d8526b.png)

#### 🎉 채팅
![image](https://user-images.githubusercontent.com/33525798/182768639-acd8910e-d91b-4ff3-8e5b-635d7fcd7c37.png)
