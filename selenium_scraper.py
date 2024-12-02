# selenium_scraper.py
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select


def get_department_options():
    # Selenium 설정
    options = webdriver.ChromeOptions()
    options.add_argument("headless")
    driver = webdriver.Chrome(options=options)

    # 학과 목록을 크롤링할 웹사이트로 이동
    driver.get("https://for-s.seoultech.ac.kr/html/pub/schedule.jsp")  # 실제 웹사이트 URL로 변경
    
    # 학과 목록을 담고 있는 <select> 요소를 찾고 옵션들을 추출
    select_element = driver.find_element(By.ID, "cbo_Less")  # 실제 ID로 변경
    options = Select(select_element).options
    
    department_options = []
    for option in options:
        department_options.append(option.text)  # 옵션 텍스트만 배열로 추가

    driver.quit()
    return department_options

def get_lecture_data(department_name, semester):
    # 옵션 생성
    options = webdriver.ChromeOptions()
    options.add_argument("headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--log-level=3")
    prefs = {"profile.managed_default_content_settings.images": 2}
    options.add_experimental_option("prefs", prefs)

    driver = webdriver.Chrome(options=options)
    driver.get('https://for-s.seoultech.ac.kr/html/pub/schedule.jsp')
    
    # 학과 이름으로 선택
    select = Select(driver.find_element(By.ID, 'cbo_Less'))
    select.select_by_visible_text(department_name)  # 학과 이름으로 선택
    
    # 학기 선택
    semester_select = Select(driver.find_element(By.ID, 'cbo_Smst'))  # 'cbo_Smst' ID의 select 태그 선택
    semester_select.select_by_value(semester)  # semester 값에 해당하는 option 선택
    
    # 검색 버튼 클릭
    search_button = driver.find_element(By.ID, 'btn_ReportSearch')
    search_button.click()

    # 테이블 데이터 수집
    lecture_datas = []
    professors = []
    list_element = driver.find_element(By.ID, "div_grid")
    tbody = list_element.find_element(By.TAG_NAME, "tbody")
    for tr in tbody.find_elements(By.TAG_NAME, "tr"):
        td = tr.find_elements(By.TAG_NAME, "td")
        lecture_name = td[2].text
        lecture_number = td[5].text
        lecture_classification = td[6].text
        lecture_credit = td[8].text
        lecture_time = td[9].text
        lecture_students = td[11].text
        professor = td[16].text
        
        # 교수 이름을 ','로 분리하여 처리
        professor_list = professor.split(',')  # ','로 구분된 교수 이름을 분리
        for prof in professor_list:
            prof = prof.strip()  # 교수 이름에서 불필요한 공백 제거
            if prof and prof not in professors:  # 빈 문자열이거나 이미 리스트에 있으면 제외
                professors.append(prof)
            
        if lecture_name:  # 빈 데이터는 제외
            lecture_datas.append({
                'lecture_name': lecture_name,
                'lecture_number': lecture_number,
                'lecture_classification': lecture_classification,
                'lecture_credit': lecture_credit,
                'lecture_time': lecture_time,
                'lecture_students': lecture_students,
                'professor': professor
            })
    
    driver.quit()
    return lecture_datas, professors

