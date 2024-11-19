# main.py
from lecture import Lecture
from typing import List
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from selenium_scraper import get_lecture_data  # 데이터 가져오는 함수 임포트

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def read_lectures(request: Request):
    # Selenium 크롤링 데이터 호출
    lecture_datas = get_lecture_data()
    # HTML 파일을 RETURN 해줌
    return templates.TemplateResponse("lectures.html", {"request": request, "lectures": lecture_datas})


# POST 엔드포인트 정의
@app.post("/api/timetable")
async def receive_timetable(lectures: List[Lecture]):
    # 받은 데이터를 로그에 출력
    print("Received lectures:", lectures)

    # 예시 응답 반환
    return {"message": "Timetable received successfully"}

# uvicorn main:app --reload