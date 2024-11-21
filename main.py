# main.py
from lecture import Lecture
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from selenium_scraper import get_lecture_data  # 데이터 가져오는 함수 임포트
from timetable import create_timetable
app = FastAPI()
templates = Jinja2Templates(directory='.')

@app.get("/", response_class=HTMLResponse)
async def read_lectures(request: Request):
    # Selenium 크롤링 데이터 호출
    lecture_datas = get_lecture_data()
    # HTML 파일을 RETURN 해줌
    return templates.TemplateResponse("index.html", {"request": request, "lectures": lecture_datas})
lectures = []

# POST 엔드포인트 정의
@app.post("/api/timetable")
async def receive_timetable(lecture: Lecture):
    if(lecture not in lectures):
        lectures.append(lecture)
    else:
        lectures.remove(lecture)
    timetable = create_timetable(lectures)
    return {"timetable": timetable}
# uvicorn main:app --reload