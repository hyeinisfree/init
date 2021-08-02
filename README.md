# init
> Django로 성신여자대학교 컴퓨터공학과 'init' 사이트 만들기! 

![](https://images.velog.io/images/hyeinisfree/post/8b68ce0c-804a-4570-bf84-4f5fb5d7a21e/%EC%8A%A4%ED%81%AC%EB%A6%B0%EC%83%B7%202021-04-17%20%EC%98%A4%ED%9B%84%2010.13.03.png)

## 회원가입, 로그인, 로그아웃

### User model

- AbstractUser model 사용
    - 사용자 한국 이름, email, 활동년도 필드를 추가해서 사용하려고 AbstratUser를 사용했다.

### 회원가입

![](https://images.velog.io/images/hyeinisfree/post/ec73d132-5bee-4803-ad18-57e697950fd0/%EC%8A%A4%ED%81%AC%EB%A6%B0%EC%83%B7%202021-04-17%20%EC%98%A4%ED%9B%84%2010.14.15.png)

- UserCreationForm 사용하여 구현하였다.
- 회원가입시 Profile model도 One-to-One으로 생성되게 하였다(models.py)에서 처리했다.

### 로그인, 로그아웃

![](https://images.velog.io/images/hyeinisfree/post/83e7426b-b38c-4eba-8c36-0ee064b18f96/%EC%8A%A4%ED%81%AC%EB%A6%B0%EC%83%B7%202021-04-17%20%EC%98%A4%ED%9B%84%2010.14.43.png)

- CBV를 사용해서 구현하였다.

### 회원정보수정

![](https://images.velog.io/images/hyeinisfree/post/dcc156ba-b95d-457e-87e7-d3f282cfdd19/%EC%8A%A4%ED%81%AC%EB%A6%B0%EC%83%B7%202021-04-17%20%EC%98%A4%ED%9B%84%2010.15.16.png)

- UserChangeForm을 사용하여 구현하였다.

### 비밀번호수정

![](https://images.velog.io/images/hyeinisfree/post/51fe7e3f-44ae-4be1-b5ab-6ecd2847fb5e/%EC%8A%A4%ED%81%AC%EB%A6%B0%EC%83%B7%202021-04-17%20%EC%98%A4%ED%9B%84%2010.15.23.png)

- PasswordChageForm을 사용하여 구현하였다.

## 프로필

사용자 프로필을 따로 만들고 싶어서 구현하였다. 

### Profile model

- User model과 OneToOne 관계 모델이다.
- nickname, bio, img, birthday, git 필드가 사용된다.
- img 필드는 ProcessedImageField로 서버에 이미지 파일로 저장된다.
    - profile_upload_to 함수를 구현하여 지정된 이름으로 서버에 저장되게 구현하였다. (upload_to 속성)
    - OverwriteStorage 클래스를 구현하여 overwrite 되게 구현하였다. (storage 속성)

### 프로필 확인

![](https://images.velog.io/images/hyeinisfree/post/408ebb78-6ed0-40ce-ae4f-3babc4e83a6e/%EC%8A%A4%ED%81%AC%EB%A6%B0%EC%83%B7%202021-04-17%20%EC%98%A4%ED%9B%84%2010.15.42.png)

- Profile model을 받아와서 쉽게 구현 가능하다.

### 프로필 수정

![](https://images.velog.io/images/hyeinisfree/post/53c22531-ce4b-4ccb-8a41-e00cf64235fc/%EC%8A%A4%ED%81%AC%EB%A6%B0%EC%83%B7%202021-04-17%20%EC%98%A4%ED%9B%84%2010.15.57.png)

- ProfileForm이라는 ModelForm을 구현하여 만들었다.
- form을 통해 쉽게 view와 template를 작성할 수 있다.

➕ 추가 예정

- 아이디 찾기
- 비밀번호 찾기

## 과제 제출

동아리 정기모임 과제를 사이트로 제출하면 좋을 거 같아서 구현해봤다.

### Homework model

- 활동년도, 제목, 내용, 작성자, 작성일시, 수정일시, 마감기한 필드로 구현하였다.

### Homework_submit model

- homework_id와 user_id 필드가 외래키로 사용된다.
- homework_id, user_id, 내용, 업로드파일, 제출일시 필드로 구성된다.
- Profile model의 img 필드와 같이 sfile 필드도 homework_upload_to 함수를 구현하여 지정된 이름으로 서버에 저장되게 하였다.

### 숙제 목록

![](https://images.velog.io/images/hyeinisfree/post/086dc504-3a4d-4e77-b7bd-79dbfcc67ce1/%EC%8A%A4%ED%81%AC%EB%A6%B0%EC%83%B7%202021-04-17%20%EC%98%A4%ED%9B%84%2010.16.26.png)

- 사용자가 로그인하고 homework 페이지에 접속하면 활동 년도 숙제 목록으로 redirect 된다.
- 숙제 목록이 보이고 숙제 제출 여부를 확인할 수 있다.

### 숙제 상세

![](https://images.velog.io/images/hyeinisfree/post/f0f797d8-3edc-4f10-80a7-ba13bc5eab50/%EC%8A%A4%ED%81%AC%EB%A6%B0%EC%83%B7%202021-04-17%20%EC%98%A4%ED%9B%84%2010.16.50.png)

- 숙제 목록 페이지에서 숙제를 선택하여 누르면 숙제 상세 페이지로 이동된다.
- 숙제 상세 페이지에서 숙제 제목, 내용, 마감기한 등을 확인할 수 있다.
- 사용자가 숙제를 제출했다면 수정 버튼, 제출하지 않았다면 제출 버튼이 보인다.

### 숙제 제출

![](https://images.velog.io/images/hyeinisfree/post/412c6445-9446-45ec-ade7-e838ef794c89/%EC%8A%A4%ED%81%AC%EB%A6%B0%EC%83%B7%202021-04-17%20%EC%98%A4%ED%9B%84%2010.16.55.png)

- 숙제 상세 페이지에서 수정 버튼을 누르면 숙제 수정 페이지로 이동된다.
    - 숙제 수정 페이지는 기존 제출한 내용을 불러온다.
    - 숙제를 제출하지 않은 사람이 수정 페이지에 접근하면 숙제 제출 페이지로 이동된다.
- 숙제 상세 페이지에서 제출 버튼을 누르면 숙제 제출 페이지로 이동된다.
    - 숙제를 제출한 사람이 수정 페이지에 접근하면 숙제 수정 페이지로 이동된다.
- 내용은 비워둘 수 없다. 파일 제출은 하나의 파일만 가능하다.
- 숙제 제출 버튼을 누르면 숙제 상세 페이지로 다시 이동된다.

➕ 추가 예정

- 마감 기한이 지났을 경우 설정  


_init 사이트는 시험기간이니 잠시 잠듭니다.._
