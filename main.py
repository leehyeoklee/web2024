# main.py
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from selenium_scraper import get_lecture_data  # 데이터 가져오는 함수 임포트

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/test")
def test():
    lecture_datas = get_lecture_data()
    return lecture_datas

@app.get("/lectures", response_class=HTMLResponse)
async def read_lectures(request: Request):
    # Selenium 크롤링 데이터 호출
    lecture_datas = get_lecture_data()
    return templates.TemplateResponse("lectures.html", {"request": request, "lectures": lecture_datas})

# uvicorn main:app --reload