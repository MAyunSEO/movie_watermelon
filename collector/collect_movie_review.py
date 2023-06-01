import re
import math
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# anaconda prompt
# > conda activate cnu_python
# > pip install beautifulsoup
# > pip install selenium
# > pip install webdriver_manager

########################################
# 1. install ChromeDriver for selenium #
########################################
# selenium -> Webdriver(chrome)
# 1. 최신 버전 사용해서 code로 다운로드(최신버전)
# 2. chrome driver 다운로드 후 주입(구버전)
# 주소 : https://sites.google.com/chromium.org/driver/

driver = Service(executable_path="../driver/chromedriver.exe")
options = Options()
options.add_experimental_option("detach", True)  # ChromeDriver 자동 종료 X
driver = webdriver.Chrome(service=driver, options=options)

# selenium : 동적 페이지에서 웹 크롤링 가능!
#             -> 원래 용도 : 웹 브라우저 테스트용
# http: 웹
# ftp: 파일 전송
# ssh: 터미널 접속
# smtp: 메일 전송

##############################
# 2.Open URL in ChromeDriver #
##############################
movie_id = 160244
url = f"https://movie.daum.net/moviedb/grade?movieId={movie_id}"

# Selenium의 ChromeDriver를 통해서 해당 URL 접속
driver.get(url)
time.sleep(1)  # 1초 딜레이(웹 페이지 랜더링 완료까지 기다리기)
doc_html = driver.page_source  # 해당 URL 소스코드
print(doc_html)
doc = BeautifulSoup(doc_html, "html.parser")
title = doc.select("span.txt_tit")[1].text.strip()  # 영화 제목 수집

# 전체 리뷰 : 91개
# 기존 출력 : 10개
# 1클릭 추가 리뷰 : 30개 추가
# (전체 리뷰 - 기존 출력) / 30 = 3 (평점 더보기 클릭 횟수)

total_review_txt = doc.select("span.txt_netizen")[0].text
# 정규화 → 숫자만 추출
total_review = int(re.sub(r"[^~0-9]", "", total_review_txt))
click_cnt = math.ceil((total_review - 10) / 30)  # "평점 더보기" 버튼 클릭 횟수(모든 리뷰 출력을 위한)

for i in range(click_cnt):
    # "평점 더보기" 클릭 (리뷰 30개씩 증가)
    driver.find_element(By.CLASS_NAME, "link_fold").click()
    time.sleep(1)
time.sleep(5)

# >> 해당 페이지에 모든 리뷰 출력 완료
review_html = driver.page_source
doc = BeautifulSoup(review_html, "html.parser")
review_list = doc.select("ul.list_comment div.cmt_info")

for review_box in review_list:
    score = review_box.select("div.ratings")[0].text
    writer = review_box.select("a.link_nick")[0].text
    review_date = review_box.select("span.txt_date")[0].text
    review = review_box.select("p.desc_txt")[0].text
    if writer != '댓글작성자':
        print(list.remove(("댓글작성자")))
    if score != '댓글모아보기':
        list.remove("댓글모아보기")
    print(f" - 평점 : {score}")
    print(f" - 작성자 : {writer}")
    print(f" - 작성일자 : {review_date}")
    print(f" - 리뷰 : {review}")
    # 숙제:리뷰, 작성자, 작성일자 수집(평점은 해주심)
