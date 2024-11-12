# selenium의 webdriver를 사용하기 위한 import
from selenium import webdriver
from selenium.webdriver.common.by import By
# selenium으로 키를 조작하기 위한 import
from selenium.webdriver.support.select import Select

# 크롬드라이버 실행
driver = webdriver.Chrome() 
#크롬 드라이버에 url 주소 넣고 실행
driver.get('https://for-s.seoultech.ac.kr/html/pub/schedule.jsp')
#select 태그를 id로 찾은 뒤, 컴퓨터 공학과를 선택
select = Select(driver.find_element(By.ID, 'cbo_Less'))
select.select_by_value("20030505")
#검색 버튼을 id로 찾아서 클릭하여 원하는 화면 띄우기
search_button = driver.find_element(By.ID,'btn_ReportSearch')
search_button.click()
list = driver.find_element(By.ID, "div_grid")
tbody = list.find_element(By.TAG_NAME,"tbody")
#테이블에서 일부 데이터들을 가져와서 test해봄
for tr in tbody.find_elements(By.TAG_NAME,"tr"):
    td=tr.find_elements(By.TAG_NAME,"td")
    lecture_name=td[2]
    lecture_number=td[5]
    lecture_time=td[9]
    print("name= "+lecture_name.text+" number= "+lecture_number.text+" time= "+lecture_time.text)
