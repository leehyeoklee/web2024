# selenium_scraper.py
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
import time

def get_lecture_data():
    # 크롬드라이버 실행
    driver = webdriver.Chrome()
    driver.get('https://for-s.seoultech.ac.kr/html/pub/schedule.jsp')

    # Select 컴퓨터 공학과
    select = Select(driver.find_element(By.ID, 'cbo_Less'))
    select.select_by_value("20030505")
    
    # 검색 버튼 클릭
    search_button = driver.find_element(By.ID, 'btn_ReportSearch')
    search_button.click()
    time.sleep(2)  # 페이지 갱신 대기 시간 조정
    
    # 테이블 데이터 수집
    lecture_datas = []
    list_element = driver.find_element(By.ID, "div_grid")
    tbody = list_element.find_element(By.TAG_NAME, "tbody")
    for tr in tbody.find_elements(By.TAG_NAME, "tr"):
        td = tr.find_elements(By.TAG_NAME, "td")
        lecture_name = td[2].text
        lecture_number = td[5].text
        lecture_time = td[9].text
        if lecture_name:  # 빈 데이터는 제외
            lecture_datas.append({
                'lecture_name': lecture_name,
                'lecture_number': lecture_number,
                'lecture_time': lecture_time
            })
    
    driver.quit()
    return lecture_datas