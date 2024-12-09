from typing import List
from pulp import LpProblem, LpVariable, LpMaximize, lpSum
from pydantic import BaseModel
from lecture import Lecture

# Preference 모델 정의
class Preference(BaseModel):
    selectedTables: List[str]  # 예: ['concentrated', 'pm']
    selectedProfessors: List[str]  # 예: ['최성록', '이길흥']

def create_timetable(lectures: List[Lecture], preference: Preference) -> List[Lecture]:
    # 선호도 파싱
    time_preference = preference.selectedTables  # 오전/오후, 집중형/분산형
    preferred_professors = preference.selectedProfessors  # 선호 교수 목록

    n_lectures = len(lectures)  # 강의 수

    # 가중치 설정
    weights = []
    for i, lecture in enumerate(lectures):
        weight = 0
        # 필수 과목 가중치
        if "필" in lecture.classification:
            weight += 6

        # 선호 교수 가중치
        if lecture.professor in preferred_professors:
            weight += 2

        # 오전/오후 선호도에 따른 가중치
        if time_preference[0] == "am":  # 오전 선호
            if any(8 <= hour <= 12 for _, hours in lecture.time for hour in hours):
                weight += 2  # 오전 강의에 높은 가중치
        elif time_preference[0] == "pm":  # 오후 선호
            if any(13 <= hour <= 24 for _, hours in lecture.time for hour in hours):
                weight += 2  # 오후 강의에 높은 가중치

        # 집중형/분산형 선호도에 따른 가중치
        days_used = len(lecture.time)
        if time_preference[1] == "concentrated":  # 하루 집중형 선호
            if days_used == 1:
                weight += 2
        elif time_preference[1] == "distributed":  # 분산형 선호
            if days_used > 1:
                weight += 2

        # 인덱스 기반 가중치 (강의 선택 순서에 따른 가중치)
        weight += (n_lectures - i) / 5
        weights.append(weight)

    # 문제 정의
    prob = LpProblem("Timetable_Optimization", LpMaximize)

    # 변수 정의
    x = [LpVariable(f"x_{i}", cat="Binary") for i in range(n_lectures)]

    # 목적 함수 설정
    prob += lpSum([weights[i] * x[i] for i in range(n_lectures)])

    # 시간대 중복을 방지하기 위해 선택된 강의의 시간대를 저장
    time_slots = {}
    for i, lecture in enumerate(lectures):
        for day, hours in lecture.time:
            for hour in range(hours[0], hours[1] + 1):
                slot = (day, hour)
                if slot not in time_slots:
                    time_slots[slot] = []
                time_slots[slot].append(i)

    # 같은 시간대에 두 개 이상의 강의를 선택하지 않도록(1의 값을 여러 강의가 가지지 않도록) 제약 추가
    for slot, lecture_indices in time_slots.items():
        prob += lpSum([x[i] for i in lecture_indices]) <= 1

    # 같은 교수, 같은 이름의 수업은 하나만 선택하도록 제약 추가
    for professor in set(lecture.professor for lecture in lectures):
        for name in set(lecture.name for lecture in lectures):
            lecture_indices = [
                i for i, lecture in enumerate(lectures)
                if lecture.professor == professor and lecture.name == name
            ]
            if len(lecture_indices) > 1:
                prob += lpSum([x[i] for i in lecture_indices]) <= 1

    # 최적화 실행
    prob.solve()

    # 최적화 결과 추출
    selected_lectures = [lectures[i] for i in range(n_lectures) if x[i].varValue == 1]

    return selected_lectures
