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
    time_preference = preference.selectedTables if preference.selectedTables else []  # 오전/오후, 집중형/분산형
    preferred_professors = preference.selectedProfessors if preference.selectedProfessors else []  # 선호 교수 목록

    n_lectures = len(lectures)  # 강의 수

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

    # 문제 정의
    prob = LpProblem("Timetable_Optimization", LpMaximize)

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

    # 최적화 결과 추출
    selected_lectures = [lectures[i] for i in range(n_lectures) if x[i].varValue == 1]

    return selected_lectures
