## 🏫 서울 과기대 시간표 생성 웹 STS (SeoulTech Scheduler)

##  프로젝트 소개    
- STS는 학생들이 자신의 선호도에 따라 최적화된 시간표를 손쉽게 생성할 수 있도록 설계된 웹 애플리케이션입니다.
- 이 프로젝트는 사용자의 요구를 반영하여, 가장 최적의 시간표를 자동으로 생성하여 시각화합니다.
- 복잡한 시간 관리 문제를 해결하고, 학업 성취와 효율성을 동시에 추구할 수 있는 도구를 제공합니다. 

## 개발 동기
대학생이라면, 매 학기마다 시간표를 만들 때에 제한사항 때문에 골치 아팠던 경험이 한 번씩은 있을 것입니다. 듣고 싶은 수업은 여러 개, 겹치는 아르바이트 시간 등 고려해야하는 사항이 너무 많아 가능한 경우의 수를 따지는 데에 많은 시간이 걸려 어려움을 겪었습니다. 그래서 나만을 위한 시간표를 빠른 시간내에 구성할 수있는 웹이 있으면 좋겠다고 생각하여 제작하게 되었습니다.

## 기술 스택
1. 백엔드: FastAPI, uvicorn
2. 프론트엔드: HTML, CSS, JavaScript (fastapi의 Jinja2 템플릿 엔진 사용)
3. 데이터 처리: Python PuLP 라이브러리를 사용한 최적화 알고리즘
4. 크롤링: Selenium 라이브러리를 사용해 강의 데이터를 실시간으로 가져옴
## 라이브러리

```
pip install fastapi
pip install "uvicorn[standard]"
pip install pydantic
pip install selenium
```
* Fast api : 비동기 방식의 웹 서버 프레임워크
* uvicorn : 비동기 방식의 http 서버
* pydantic : JSON 데이터를 자동으로 Python 객체로 변환
* selenium : 서울과기대 수강신청 사이트에서 정보를 크롤링
## 실행 영상

## 페이지 별 기능
### 메인 페이지
* 학기를 선택할 수 있습니다.

![화면1](https://github.com/user-attachments/assets/24ad2399-ac06-4851-9eb8-6dd478acde7f)

<br>

### 학과 선택 페이지
![화면2](https://github.com/user-attachments/assets/b3319fdf-10fc-414a-8ca9-d63a927c2b37)


* 웹 크롤링을 통해 추출한 학과 이름들 중 하나를 선택할 수 있습니다.

![화면3](https://github.com/user-attachments/assets/e3c903e3-dd5d-439b-9860-a30f08acc995)

<br>

### 선호도 선택
데이터를 불러오는 동안에 선호도를 조사합니다. 선호하는 것이 없을 시에 선택하지 않을 수도 있습니다.
* 하루에 집중된 시간표와, 여러 날에 분산된 시간표 중 하나를 선택할 수 있습니다. 

![화면4](https://github.com/user-attachments/assets/58507bf4-585e-49e4-83f3-4ab35b285da0)

* 오전에 치중된 시간표와, 오후에 치중된 시간표 중 하나를 선택할 수 있습니다.

![화면5](https://github.com/user-attachments/assets/5bb45947-0515-4fd6-886a-f1ebaf955a6b)

* 웹 크롤링을 통해 추출한 교수 이름 중 선호하는 교수를 선택할 수 있습니다.

![화면6](https://github.com/user-attachments/assets/6c97a7ea-df8a-4743-b9db-5c048824e954)

<br>

### 로딩화면
* 데이터를 불러오는 동안 로딩화면을 제공합니다.

![로딩화면](https://github.com/user-attachments/assets/27c3a398-2246-4b75-9c7a-0944b2a29542)

<br>

### 시간표 생성 화면
* 이용 설명을 제공합니다.

![화면7](https://github.com/user-attachments/assets/fce8dbd5-9b6c-4921-be2b-06e26b566701)
* 듣고 싶은 과목을 선택하여 시간표를 생성하고, 시각화합니다.

![화면8](https://github.com/user-attachments/assets/461b5867-a8f4-485f-9219-1877751b2ed2)

## 주요 기능 구현 로직
### 최적의 시간표 생성 (python)
PuLP 라이브러리를 사용하여 선형 프로그래밍(Linear Programming)을 기반으로 구현되었습니다.

scipy.optimize.linprog는 정수 제약 조건을 지원하지 않기 때문에, 이를 지원하는 PuLP 라이브러리를 사용하여 각 과목의 선택 여부를 나타내는 변수(0 또는 1)를 binary하게 모델링했습니다.

이용자의 선택(예: 선호 교수, 강의 시간대 등)를 기반으로 각 강의에 선호도를 부여합니다. 그 후, 선호도의 합이 최대가 되는 강의 조합을 최적화 알고리즘으로 계산하여 반환합니다.
```python
 # 선호도 설정
    prfs = []
    for i, lecture in enumerate(lectures):
        prf = 0
        # 필수 과목 선호도
        if "필" in lecture.classification:
            prf += 6
        # 교수 선호도
        if preferred_professors and lecture.professor in preferred_professors:
            prf += 2
        # 오전/오후에 따른 선호도
        if time_preference:
            if time_preference[0] == "am":  
                if any(8 <= hour <= 12 for _, hours in lecture.time for hour in hours):
                    prf += 2  
            elif time_preference[0] == "pm":  
                if any(13 <= hour <= 24 for _, hours in lecture.time for hour in hours):
                    prf += 2  
            # 집중형/분산형에 따른 선호도
            days_used = len(lecture.time)
            if time_preference[1] == "concentrated": 
                if days_used == 1:
                    prf += 2
            elif time_preference[1] == "distributed": 
                if days_used > 1:
                    prf += 2
        # 인덱스 기반 선호도 (선택 순서)
        prf += (n_lectures - i) / 5
        prfs.append(prf)
```
같은 시간대에 여러개의 강의가 존재할 수 없고, 같은 이름의 강의를 여러 개 수강할 수 없도록 제약조건을 설정 후 최적화 문제를 해결하여 최적의 시간표를 생성하였습니다.
```python
 # 변수 정의
    x = [LpVariable(f"x_{i}", cat="Binary") for i in range(n_lectures)]

    # 목적 함수 설정
    prob += lpSum([prfs[i] * x[i] for i in range(n_lectures)])

    # 시간대 중복을 방지하기 위해 선택된 강의의 시간대를 저장
    time_slots = {}
    for i, lecture in enumerate(lectures):
        for day, hours in lecture.time:
            for hour in range(hours[0], hours[1] + 1):
                slot = (day, hour)
                if slot not in time_slots:
                    time_slots[slot] = []
                time_slots[slot].append(i)

    # 같은 시간대에 두 개 이상의 강의를 선택하지 않도록 제약 추가
    for slot, lecture_indices in time_slots.items():
        prob += lpSum([x[i] for i in lecture_indices]) <= 1

    # 같은 이름의 수업은 하나만 선택하도록 제약 추가
    for name in set(lecture.name for lecture in lectures):
        lecture_indices = [
            i for i, lecture in enumerate(lectures) if lecture.name == name
        ]
        if len(lecture_indices) > 1:
            prob += lpSum([x[i] for i in lecture_indices]) <= 1


    # 최적화 실행
    prob.solve()
```

### 시간표 색깔 구분 (javascript)
'교수이름-강의명' 문자열을 해시값으로 변환하고, 그 값을 RGB 색상 값으로 바꾸는 방식으로, 강의에 대해 고유한 색상을 생성하여 시간표가 어떤 강의로 구성되어있는지 인지할 수 있도록 했습니다.
```js
function generateColorFromString(input) {
    let hash = 0;
    for (let i = 0; i < input.length; i++) {
        hash = input.charCodeAt(i) + ((hash << 5) - hash);
    }

    // 해시값에서 RGB 추출
    let r = (hash >> 16) & 0xFF;
    let g = (hash >> 8) & 0xFF;
    let b = hash & 0xFF;

    // 밝기 계산 (YIQ 방식을 활용)
    const brightness = (r * 0.299 + g * 0.587 + b * 0.114);

    // 밝기가 너무 어두우면 밝기 조정
    if (brightness < 128) {
        r = Math.min(r + 70, 255); // 밝기 조정
        g = Math.min(g + 70, 255);
        b = Math.min(b + 70, 255);
    }

    return `rgb(${r}, ${g}, ${b})`;
}
```
## API
![image](https://github.com/user-attachments/assets/3cbf02bc-b677-47b6-aaf8-3b0e9e60d218)

## Refernce
* https://doyu-l.tistory.com/360 -  디자인 패턴 참고
* https://wikidocs.net/137914 - 셀레니엄 사용
* https://fastapi.tiangolo.com/ko/tutorial/first-steps/ - fast api 사용 
* https://for-s.seoultech.ac.kr/html/pub/schedule.jsp - 강의 정보
* https://www.seoultech.ac.kr/index.jsp - 서울과기대 이미지
* 에브리타임 모바일 앱 - 시간표 이미지



