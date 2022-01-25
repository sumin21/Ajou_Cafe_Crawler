from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from bs4 import BeautifulSoup as bs
from selenium import webdriver
import time
from selenium.webdriver.support.ui import WebDriverWait as wait
import json
import re
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.options import Options
import datetime
from selenium.common.exceptions import ElementNotInteractableException

options = Options()
options.binary_location = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe'

driver = webdriver.Chrome(
    'C:\\Users\이수민\Desktop\chromedriver_win32\chromedriver.exe', chrome_options=options)
# driver.maximize_window()
# driver.get("https://map.naver.com/v5/search")
driver.get('https://map.naver.com/v5/search/%EC%95%84%EC%A3%BC%EB%8C%80%ED%95%99%EA%B5%90%20%EC%A3%BC%EB%B3%80%20%EC%8B%9D%EB%8B%B9?c=14142449.9333239,4477832.8971836,16,0,0,0,dh')
# 검색창에 검색어 입력하기
# time.sleep(2)
# search_box = driver.find_element_by_css_selector("div.input_box>input")
# search_box.send_keys("아주대학교 주변 피시방")


# 검색버튼 누르기
# search_box.send_keys(Keys.ENTER)

# 크롤링
for p in range(1):
    # 5초 delay
    time.sleep(2)
    html = bs(driver.page_source, 'html.parser')
    driver.switch_to.frame("searchIframe")
    html = bs(driver.page_source, 'html.parser')

    time.sleep(4)

    print(len(driver.find_elements_by_css_selector('div._3hn9q')))
    k = driver.find_elements_by_css_selector('div._3hn9q > a')

    # 가게 obj
    eleObj = {}
    # 가게들 array
    eleArr = []

    for i in range(50):
        # 한 가게 정보
        oneEleObj = {}

        print(str(i+1) + '번째')
        # if(i == 60):
        #     break

        time.sleep(8)
        k = driver.find_elements_by_css_selector('div._3hn9q > a')
        k[i].click()
        time.sleep(2)
        driver.switch_to.default_content()
        frameName = driver.find_element_by_id("entryIframe")
        driver.switch_to.frame(frameName)
        html = bs(driver.page_source, 'html.parser')
        name = driver.find_element_by_css_selector('span._3XamX').text
        print(name)
        oneEleObj['이름'] = name

        # 사진 url
        try:
            photoUrl = driver.find_elements_by_css_selector(
                'div.cb7hz._div')[0].get_attribute("style")
            url = photoUrl.split('background-image: url("')[1][:-3]
            print(url)
            oneEleObj['사진url'] = url

        except:
            print('사진url 없음')
            oneEleObj['사진url'] = 0

        # 별점
        try:
            star = driver.find_element_by_css_selector(
                'span._1Y6hi._1A8_M > em').text
            print(star)
            oneEleObj['별점'] = star

        except:
            print('별점 없음')
            oneEleObj['별점'] = 0

        # 주소
        try:
            address = driver.find_element_by_css_selector(
                'a._1Gmk4 > span._2yqUQ').text
            print(address)
            oneEleObj['주소'] = address
        except:
            print('주소 없음')
            oneEleObj['주소'] = 0
        # 전화번호
        try:
            phoneNumber = driver.find_element_by_css_selector(
                'span._3ZA0S').text
            print(phoneNumber)
            oneEleObj['연락처'] = phoneNumber

        except:
            print('전화번호 없음')
            oneEleObj['연락처'] = 0
        # 이용시간
        try:
            driver.find_element_by_css_selector('a._318hN').click()
            time.sleep(2)
            dates = driver.find_elements_by_css_selector('span.j9L2O')
            dateArr = []
            for j in range(len(dates)):
                print(driver.find_elements_by_css_selector(
                    'span.j9L2O')[j].text)
                print(driver.find_elements_by_css_selector(
                    'div._2WoIY')[j].text)
                date1 = driver.find_elements_by_css_selector(
                    'span.j9L2O')[j].text
                date2 = driver.find_elements_by_css_selector(
                    'div._2WoIY')[j].text
                date3 = date1 + ' ' + date2
                dateArr.append(date3)
            oneEleObj['영업시간'] = dateArr
        except:
            print('이용시간 없음')
            oneEleObj['영업시간'] = 0

        # 리뷰
        try:
            reviewArr = 0
            for tlqkf in range(len(driver.find_elements_by_css_selector('div._2MDmw > a'))):
                print(driver.find_elements_by_css_selector(
                    'div._2MDmw > a > span')[tlqkf].text)
                if(driver.find_elements_by_css_selector('div._2MDmw > a > span')[tlqkf].text == "리뷰"):
                    reviewElement = driver.find_elements_by_css_selector('div._2MDmw > a')[
                        tlqkf]
                    print(reviewElement)
                    time.sleep(2)
                    reviewElement.click()
                    time.sleep(2)

                    try:
                        print(len(driver.find_elements_by_css_selector('li._3FaRE')))
                        reviewArr = []
                        for reviewNum in range(len(driver.find_elements_by_css_selector('ul._1jVSG > li._3FaRE'))):
                            reviewObj = {}
                            try:
                                reviewText = driver.find_elements_by_css_selector('span.WoYOw')[
                                    reviewNum].text
                                print(reviewText)
                                reviewObj['리뷰글'] = reviewText
                            except:
                                reviewText = ""
                                print(reviewText)
                                reviewObj['리뷰글'] = reviewText
                            try:
                                reviewStar = driver.find_elements_by_css_selector('span.Sv1wj > em')[
                                    reviewNum].text
                                print(reviewStar)
                                reviewObj['리뷰별점'] = reviewStar
                            except:
                                reviewStar = 0
                                print(reviewStar)
                                reviewObj['리뷰별점'] = reviewStar
                            try:
                                reviewDate = driver.find_elements_by_css_selector(
                                    'div._3-LAD > span._1fvo3 > time')[reviewNum].text
                                print(reviewDate)
                                reviewObj['리뷰날짜'] = reviewStar
                            except:
                                reviewDate = 0
                                print(reviewDate)
                                reviewObj['리뷰날짜'] = reviewStar
                            reviewArr.append(reviewObj)
                        oneEleObj['리뷰'] = reviewArr

                    except:
                        print('리뷰 리스트 없음')
                        reviewArr = 0
                        oneEleObj['리뷰'] = reviewArr
                    break
        except:
            print('리뷰 항목 없음')
            reviewArr = 0
            oneEleObj['리뷰'] = reviewArr

        eleArr.append(oneEleObj)

        driver.get('https://map.naver.com/v5/search/%EC%95%84%EC%A3%BC%EB%8C%80%ED%95%99%EA%B5%90%20%EC%A3%BC%EB%B3%80%20%EC%8B%9D%EB%8B%B9?c=14142449.9333239,4477832.8971836,16,0,0,0,dh')
        time.sleep(3)
        driver.switch_to.frame("searchIframe")
        html = bs(driver.page_source, 'html.parser')
        time.sleep(2)

    eleObj['음식점'] = eleArr
    with open('doit-food' + '.json', 'w') as f:
        json.dump(eleObj, f, ensure_ascii=False)

driver.close()
