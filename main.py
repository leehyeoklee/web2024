# main.py
from lecture import Lecture
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from selenium_scraper import get_lecture_data  # 데이터 가져오는 함수 임포트
from timetable import create_timetable
from fastapi.staticfiles import StaticFiles
from selenium_scraper import get_department_options
from timetable import Preference

app = FastAPI()

app.mount("/images", StaticFiles(directory="images"), name="images")
templates = Jinja2Templates(directory='.')
department_options = []
lectures = []   # 선택할 과목들의 배열
lecture_datas = []  # 크롤링해올 과목 데이터들의 배열
professors = []
preference = [] # 선호도
semester=""

@app.get("/", response_class=HTMLResponse)
async def main_page(request: Request):
    return templates.TemplateResponse("templates/index.html", {
        "request": request,
    })    
    

@app.post("/api/submit-semester")
async def submit_semester(request: Request):
    # 클라이언트에서 전송한 JSON 데이터를 파싱
    global semester
    data = await request.json()
    semester = data.get('semester')

@app.get("/select", response_class=HTMLResponse)
async def selection_page(request: Request):
    # 학과 목록 데이터 가져오기
    global department_options
    if(not department_options):
        department_options = get_department_options()  # 동기 함수 호출
    return templates.TemplateResponse("templates/selection.html", {
        "request": request,
        "departments": department_options  # 학과 목록 데이터 추가
    })
    
@app.post("/api/submit-department")
async def submit_department(request: Request):
    # 클라이언트에서 전송한 JSON 데이터를 파싱
    global lecture_datas, professors
    data = await request.json()
    department_value = data.get('departmentValue')
    # get_lecture_data 함수에 department_value를 전달
    lecture_datas, professors = get_lecture_data(department_value,semester)
    return {'professors': professors}

@app.post("/api/submit-selection")
async def submit_selection(request: Request):
    # 클라이언트에서 전송한 JSON 데이터를 파싱
    global preference
    data = await request.json()
    preference = Preference(**data)
    print(preference)
@app.get("/api/timetable", response_class=HTMLResponse)
async def read_lectures(request: Request):
    global lectures, lecture_datas
    lectures = []
    # HTML 파일을 RETURN 해줌
    return templates.TemplateResponse("templates/timetable.html", {"request": request, "lectures": lecture_datas})

# POST 엔드포인트 정의
@app.post("/api/timetable")
async def receive_timetable(lecture: Lecture):
    if(lecture not in lectures):
        lectures.append(lecture)
    else:
        lectures.remove(lecture)
    if(len(lectures)):
        return {"timetable": create_timetable(lectures,preference=preference)}


# uvicorn main:app --reload