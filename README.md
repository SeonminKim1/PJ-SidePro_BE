![image](https://user-images.githubusercontent.com/33525798/177453882-a8d55a06-1556-4a63-b1f8-244fca57b0a4.png)

## :owl: SidePro (SideProject)
- 개발자를 위한 사이드 프로젝트 공유 플랫폼 서비스 (with. 커피챗을 곁들인) 

## :panda_face: Introduction
- **주제** : 사이드 프로젝트 공유 플랫폼 (with. 커피챗)
- **기간** : 2022.07.07 (목) ~ 2022.08.04 (목)
- **Team** : 김선민 ([Github](https://github.com/SeonminKim1)), 김민기 ([Github](https://github.com/kmingky)), 박재현 ([Github](https://github.com/Aeius)), 황신혜 ([Github](https://github.com/hwangshinhye)) 

<hr>

## 📚 Project Structure
![image](https://user-images.githubusercontent.com/33525798/177453424-fbabf1d3-6109-4e68-a9cd-83c265fc4637.png)
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
![image](https://user-images.githubusercontent.com/33525798/177453735-59c483e0-a638-42fd-bccb-47b1795641a3.png)

#### DB Modeling   
![image](https://user-images.githubusercontent.com/33525798/177455609-da9e00a8-560e-45d2-a174-b300e86b18c6.png)

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
┌─smops
├── smops               // project
│   ├── urls.py       
│   ├── settings.py     // setting
│   └── ...
├── art                 // app
│   ├── models.py       // DB Model - User
│   ├── views.py        // View Functions
│   ├── serializers.py  // Serializers
│   └── ...
├── mygallery           // app
│   ├── models.py       // DB Model - Restaurant, Category
│   ├── views.py        // View Functions
│   ├── serializers.py  // Serializers
│   └── ...
├── ai                  // app + ai GAN
│   ├── service/        // AI Style Transfer 
│   ├── models.py       // DB Model - Star 
│   ├── views.py        // View Functions
│   ├── upload.py       // AWS S3 Upload Code 
│   ├── serializers.py  // Serializers
│   └── ...
├── user                // app
│   ├── models.py       // DB Model - Diary
│   ├── views.py        // View Functions
│   ├── serializers.py  // Serializers
│   └── ...
├── media 
│   └── test_img/       // test img    
│
├── **manage.py**           // 메인
└── requirements.txt
```

<hr>


## :computer: Development

#### Login/Join Page
- 회원가입 vaildation
- 로그인 JWT Token 부여

#### 유화 메인 페이지
- 유화 카테고리 별 조회 : 인물화, 풍경화, 정물화, 동물화
- 유화 필터링 별 조회
   - (1) 정렬 : 등록일, 가격 등
   - (2) 가격 범위 : ~10만원, ~30만원
   - (3) 그림형태
- 유화 아티스트 검색

#### 유화 상세 페이지
- 유화 정보 조회
- 유화 로그 조회 (히스토리)
- 유화 구매 하기

#### 마이 갤러리 페이지
- 보유 중인 내 유화 조회
- 유화 판매 상태로 업데이트 / 삭제
- 유화 로그 조회 (히스토리)

#### 유화 만들기 페이지 (AI)
- Base 이미지, Style 이미지 업로드
- StyleGAN 모델 학습 (RUN 버튼)
- 학습 결과 내 유화로 등록

#### AWS Infra
- AWS EC2 이용한 외부 Publish 배포
- AWS S3 User 이미지 업로드 및 정적 파일 관리 
- AWS IAM 부여하여 Infra Team 공동 관리

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



