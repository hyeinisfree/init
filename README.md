# init
Django로 성신여자대학교 컴퓨터공학과 'init' 사이트 만들기! 

![https://s3-us-west-2.amazonaws.com/secure.notion-static.com/c6b8ac2c-2ef4-41f4-a2ea-c1ba365f8edb/_2021-04-17__10.13.03.png](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/c6b8ac2c-2ef4-41f4-a2ea-c1ba365f8edb/_2021-04-17__10.13.03.png)

## 회원가입, 로그인, 로그아웃

---

### User model

- AbstractUser model 사용
    - 사용자 한국 이름, email, 활동년도 필드를 추가해서 사용하려고 AbstratUser를 사용했다.

### 회원가입

![https://s3-us-west-2.amazonaws.com/secure.notion-static.com/5774ffbe-1e6c-4522-a2c0-9838dd5f7567/_2021-04-17__10.14.15.png](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/5774ffbe-1e6c-4522-a2c0-9838dd5f7567/_2021-04-17__10.14.15.png)

- UserCreationForm 사용하여 구현하였다.
- 회원가입시 Profile model도 One-to-One으로 생성되게 하였다(models.py)에서 처리했다.

### 로그인, 로그아웃

![https://s3-us-west-2.amazonaws.com/secure.notion-static.com/5dcbb036-1d55-4dac-998e-df15bc96283b/_2021-04-17__10.14.43.png](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/5dcbb036-1d55-4dac-998e-df15bc96283b/_2021-04-17__10.14.43.png)

- CBV를 사용해서 구현하였다.

### 회원정보수정

![https://s3-us-west-2.amazonaws.com/secure.notion-static.com/bc067afe-c101-4871-bce5-36b3b3635c2a/_2021-04-17__10.15.16.png](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/bc067afe-c101-4871-bce5-36b3b3635c2a/_2021-04-17__10.15.16.png)

- UserChangeForm을 사용하여 구현하였다.

### 비밀번호수정

![https://s3-us-west-2.amazonaws.com/secure.notion-static.com/e4906463-bcaa-415d-98c2-f6aabe1f14b3/_2021-04-17__10.15.23.png](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/e4906463-bcaa-415d-98c2-f6aabe1f14b3/_2021-04-17__10.15.23.png)

- PasswordChageForm을 사용하여 구현하였다.

## 프로필

---

사용자 프로필을 따로 만들고 싶어서 구현하였다. 

### Profile model

- User model과 OneToOne 관계 모델이다.
- nickname, bio, img, birthday, git 필드가 사용된다.
- img 필드는 ProcessedImageField로 서버에 이미지 파일로 저장된다.
    - profile_upload_to 함수를 구현하여 지정된 이름으로 서버에 저장되게 구현하였다. (upload_to 속성)
    - OverwriteStorage 클래스를 구현하여 overwrite 되게 구현하였다. (storage 속성)

### 프로필 확인

![https://s3-us-west-2.amazonaws.com/secure.notion-static.com/5b34ffd8-6922-40d9-b4c0-a3af27eae21e/_2021-04-17__10.15.42.png](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/5b34ffd8-6922-40d9-b4c0-a3af27eae21e/_2021-04-17__10.15.42.png)

- Profile model을 받아와서 쉽게 구현 가능하다.

### 프로필 수정

![https://s3-us-west-2.amazonaws.com/secure.notion-static.com/f98610fc-701a-4823-ae43-ba70f81ad10c/_2021-04-17__10.15.57.png](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/f98610fc-701a-4823-ae43-ba70f81ad10c/_2021-04-17__10.15.57.png)

- ProfileForm이라는 ModelForm을 구현하여 만들었다.
- form을 통해 쉽게 view와 template를 작성할 수 있다.

➕ 추가 예정

- 아이디 찾기
- 비밀번호 찾기

## 과제 제출

---

동아리 정기모임 과제를 사이트로 제출하면 좋을 거 같아서 구현해봤다.

### Homework model

- 활동년도, 제목, 내용, 작성자, 작성일시, 수정일시, 마감기한 필드로 구현하였다.

### Homework_submit model

- homework_id와 user_id 필드가 외래키로 사용된다.
- homework_id, user_id, 내용, 업로드파일, 제출일시 필드로 구성된다.
- Profile model의 img 필드와 같이 sfile 필드도 homework_upload_to 함수를 구현하여 지정된 이름으로 서버에 저장되게 하였다.

### 숙제 목록

![https://s3-us-west-2.amazonaws.com/secure.notion-static.com/9b2fbb23-3aaa-461a-a990-d10780f750aa/_2021-04-17__10.16.26.png](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/9b2fbb23-3aaa-461a-a990-d10780f750aa/_2021-04-17__10.16.26.png)

- 사용자가 로그인하고 homework 페이지에 접속하면 활동 년도 숙제 목록으로 redirect 된다.
- 숙제 목록이 보이고 숙제 제출 여부를 확인할 수 있다.

### 숙제 상세

![https://s3-us-west-2.amazonaws.com/secure.notion-static.com/b3c6c2a2-420b-4463-aa3f-a1540f519434/_2021-04-17__10.16.50.png](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/b3c6c2a2-420b-4463-aa3f-a1540f519434/_2021-04-17__10.16.50.png)

- 숙제 목록 페이지에서 숙제를 선택하여 누르면 숙제 상세 페이지로 이동된다.
- 숙제 상세 페이지에서 숙제 제목, 내용, 마감기한 등을 확인할 수 있다.
- 사용자가 숙제를 제출했다면 수정 버튼, 제출하지 않았다면 제출 버튼이 보인다.

### 숙제 제출

![https://s3-us-west-2.amazonaws.com/secure.notion-static.com/b6d3d427-9713-48f4-b0a7-1acef9dfb5d1/_2021-04-17__10.16.55.png](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/b6d3d427-9713-48f4-b0a7-1acef9dfb5d1/_2021-04-17__10.16.55.png)

- 숙제 상세 페이지에서 수정 버튼을 누르면 숙제 수정 페이지로 이동된다.
    - 숙제 수정 페이지는 기존 제출한 내용을 불러온다.
    - 숙제를 제출하지 않은 사람이 수정 페이지에 접근하면 숙제 제출 페이지로 이동된다.
- 숙제 상세 페이지에서 제출 버튼을 누르면 숙제 제출 페이지로 이동된다.
    - 숙제를 제출한 사람이 수정 페이지에 접근하면 숙제 수정 페이지로 이동된다.
- 내용은 비워둘 수 없다. 파일 제출은 하나의 파일만 가능하다.
- 숙제 제출 버튼을 누르면 숙제 상세 페이지로 다시 이동된다.

➕ 추가 예정

- 마감 기한이 지났을 경우 설정

init 사이트는 시험기간이니 잠시 잠듭니다..
