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


# 크롤링
def naverCrawler(url):
    driver.get(url)
    # 2초 delay
    time.sleep(2)

    # searchIframe으로 frame 이동
    driver.switch_to.frame("searchIframe")
    bs(driver.page_source, 'html.parser')

    # 4초 delay
    time.sleep(4)

    # 가게 list
    k = driver.find_elements_by_css_selector('div._3hn9q > a')

    # 가게 obj
    eleObj = {}
    # 가게들 array
    eleArr = []

    # 50개 가게 크롤링 (스크롤 구현 x)
    for i in range(50):
        # 한 가게 정보
        oneEleObj = {}

        # 몇번째 가게
        print(str(i+1) + '번째')

        # 8초 delay
        time.sleep(8)

        # 가게 list (index ++)
        k = driver.find_elements_by_css_selector('div._3hn9q > a')
        # 가게 click
        k[i].click()
        # 2초 delay
        time.sleep(2)
        # 이전 frame으로 돌아가기
        driver.switch_to.default_content()
        # entryIframe으로 frame 이동
        frameName = driver.find_element_by_id("entryIframe")
        driver.switch_to.frame(frameName)
        bs(driver.page_source, 'html.parser')

        # 가게명
        name = driver.find_element_by_css_selector('span._3XamX').text
        print(name)
        oneEleObj['이름'] = name

        # 사진 url
        try:
            photoUrl = driver.find_elements_by_css_selector(
                'div.cb7hz._div')[0].get_attribute("style")
            photoUrlText = photoUrl.split('background-image: url("')[1][:-3]
            print(photoUrlText)
            oneEleObj['사진url'] = photoUrlText

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
            # 리뷰 창 클릭
            for optionEle in range(len(driver.find_elements_by_css_selector('div._2MDmw > a'))):
                print(driver.find_elements_by_css_selector(
                    'div._2MDmw > a > span')[optionEle].text)
                if(driver.find_elements_by_css_selector('div._2MDmw > a > span')[optionEle].text == "리뷰"):
                    reviewElement = driver.find_elements_by_css_selector('div._2MDmw > a')[
                        optionEle]
                    print(reviewElement)
                    time.sleep(2)
                    reviewElement.click()
                    time.sleep(2)

                    # 리뷰 list
                    try:
                        print(len(driver.find_elements_by_css_selector('li._3FaRE')))
                        reviewArr = []
                        for reviewNum in range(len(driver.find_elements_by_css_selector('ul._1jVSG > li._3FaRE'))):
                            reviewObj = {}

                            # 리뷰글
                            try:
                                reviewText = driver.find_elements_by_css_selector('span.WoYOw')[
                                    reviewNum].text
                                print(reviewText)
                                reviewObj['리뷰글'] = reviewText
                            except:
                                reviewText = ""
                                print(reviewText)
                                reviewObj['리뷰글'] = reviewText

                            # 리뷰별점
                            try:
                                reviewStar = driver.find_elements_by_css_selector('span.Sv1wj > em')[
                                    reviewNum].text
                                print(reviewStar)
                                reviewObj['리뷰별점'] = reviewStar
                            except:
                                reviewStar = 0
                                print(reviewStar)
                                reviewObj['리뷰별점'] = reviewStar

                            # 리뷰날짜
                            try:
                                reviewDate = driver.find_elements_by_css_selector(
                                    'div._3-LAD > span._1fvo3 > time')[reviewNum].text
                                print(reviewDate)
                                reviewObj['리뷰날짜'] = reviewStar
                            except:
                                reviewDate = 0
                                print(reviewDate)
                                reviewObj['리뷰날짜'] = reviewStar

                            # reviewArr list에 리뷰 한개씩 저장
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

        # eleArr list에 가게 한개씩 저장
        eleArr.append(oneEleObj)

        # 이전 frame으로 돌아가지 못해서 driver 초기화
        driver.get(url)
        time.sleep(3)

        # searchIframe frame으로 이동
        driver.switch_to.frame("searchIframe")
        bs(driver.page_source, 'html.parser')
        time.sleep(2)

    # 최종
    # {'음식점' : [....]}
    eleObj['음식점'] = eleArr

    # json 형태로 저장 (argument에는 object형태로 들어가야 함) / file 명 : 'doit-food.json'
    with open('doit-food' + '.json', 'w') as f:
        json.dump(eleObj, f, ensure_ascii=False)

    # driver close
    driver.close()


# crawler 호출
# 네이버 맵 (식당)
naverCrawler('https://map.naver.com/v5/search/%EC%95%84%EC%A3%BC%EB%8C%80%ED%95%99%EA%B5%90%20%EC%A3%BC%EB%B3%80%20%EC%8B%9D%EB%8B%B9?c=14142449.9333239,4477832.8971836,16,0,0,0,dh')
