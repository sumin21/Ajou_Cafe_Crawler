from selenium import webdriver
import time
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup as bs
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


def no_space(text):
    text1 = re.sub('&nbsp; | &nbsp;| \n|\t|\r', '', text)
    text2 = re.sub('\n\n', '', text1)
    text2.strip()
    return text2


def crawl(target_url):

    cafeArr = []
    driver.get(target_url)
    time.sleep(3)
    soup = bs(driver.page_source, 'html.parser')

    for page in range(4):
        time.sleep(8)
        print(
            len(soup.find_all("a", {"class": "a4gq8e-aVTXAb-haAclf-jRmmHf-hSRGPd"})))
        if(page == 1):
            for cafe in soup.find_all("a", {"class": "a4gq8e-aVTXAb-haAclf-jRmmHf-hSRGPd"}):
                cafeObj = {}
                url = cafe.get('href')
                driver.get(url)
                soup1 = bs(driver.page_source, 'html.parser')

                cafeName = driver.find_element_by_css_selector(
                    'h1.x3AX1-LfntMc-header-title-title > span').text
                cafeObj['카페이름'] = cafeName
                print(cafeName)

                # if(cafeName != '카페쿠츠'):
                #     continue
                # 카페사진
                try:
                    cafePhotoUrl = driver.find_element_by_css_selector(
                        'button.F8J9Nb-LfntMc-header-HiaYvf-LfntMc > img').get_attribute("src")
                    cafeObj['사진url'] = cafePhotoUrl
                except:
                    print('카페사진 없음')
                    cafeObj['사진url'] = 0

                # 별점
                try:
                    cafeStar = driver.find_element_by_css_selector(
                        'span.aMPvhf-fI6EEc-KVuj8d').text
                    cafeObj['별점'] = cafeStar
                except:
                    print('별점 없음')
                    cafeObj['별점'] = 0

                # 주소
                try:
                    cafeAddress = soup1.find(
                        "button", {"data-item-id": "address"})['aria-label']
                    cafeObj['주소'] = cafeAddress
                except:
                    print('주소 없음')
                    cafeObj['주소'] = 0

                # 연락처
                try:
                    cafePhoneNumber = soup1.find(
                        "button", {"data-tooltip": "전화번호 복사"})['aria-label']
                    cafeObj['연락처'] = cafePhoneNumber

                except:
                    print('연락처 없음')
                    cafeObj['연락처'] = 0

                cafeObj['서비스옵션'] = []
                # 옵션
                try:

                    for option in soup1.select('div.uxOu9-sTGRBb-p83tee-haAclf > div'):
                        print(option['aria-label'])
                        cafeObj['서비스옵션'].append(option['aria-label'])
                except:
                    print('옵션 없음')
                    cafeObj['서비스옵션'] = 0

                cafeObj['영업시간'] = {}
                # 영업시간
                try:
                    cafeTimeStr = soup1.find(
                        "div", {"class": "LJKBpe-open-R86cEd-haAclf"})['aria-label']
                    print(cafeTimeStr)
                    newCafeTimeStr = cafeTimeStr[:-15]
                    cafeTimeArr1 = newCafeTimeStr.split('; ')
                    for cafeTime in cafeTimeArr1:
                        cafeTimeArr2 = cafeTime.split(',')
                        cafeTimeArr3 = cafeTimeArr2[1].split('~')
                        cafeObj['영업시간'][cafeTimeArr2[0]] = [
                            cafeTimeArr3[0], cafeTimeArr3[1]]

                except:
                    print('영업시간 기재 없음')
                    cafeObj['영업시간'] = 0

                # 리뷰
                time.sleep(5)
                driver.execute_script("window.scrollTo(0, 1000)")
                cafeObj['리뷰'] = []
                # reviewArr = []
                errorArr = []
                try:
                    reviewBtn = driver.find_element_by_xpath(
                        "//div[@class='jANrlb']/button[@class='HHrUdb gm2-button-alt HHrUdb-v3pZbf']")

                    # reviewBtn.send_keys(Keys.ENTER)
                    reviewBtn.click()
                    time.sleep(2)

                    for k in range(0, len(driver.find_elements_by_css_selector(
                            'span.ODSEW-ShBeI-H1e3jb'))):
                        reviewObj = {}
                        reviewStar = driver.find_elements_by_css_selector(
                            'span.ODSEW-ShBeI-H1e3jb')[k].get_attribute("aria-label")
                        reviewDate = driver.find_elements_by_css_selector(
                            'span.ODSEW-ShBeI-RgZmSc-date')[k].text
                        reviewText = driver.find_elements_by_css_selector(
                            'span.ODSEW-ShBeI-text')[k].text

                        reviewObj['리뷰별점'] = reviewStar
                        reviewObj['리뷰날짜'] = reviewDate
                        reviewObj['리뷰글'] = reviewText

                        cafeObj['리뷰'].append(reviewObj)

                except ElementNotInteractableException:
                    print('조짐')
                    errorArr.append(cafeName)
                    cafeObj['리뷰'] = 'err'

                except:
                    print('리뷰 없음')
                    cafeObj['리뷰'] = 0

                cafeArr.append(cafeObj)
                # print(reviewArr)

        driver.get(target_url)
        soup = bs(driver.page_source, 'html.parser')
        for direction in range(1+(page+1)):
            time.sleep(3)
            driver.find_element_by_css_selector(
                '#ppdPk-Ej1Yeb-LgbsSe-tJiF1e').click()
            soup = bs(driver.page_source, 'html.parser')

        middleObj = {}
        middleObj['카페'] = cafeArr
        print(middleObj)
        with open('doit-cafe11' + str(page+1) + '.json', 'w') as f:
            json.dump(middleObj, f, ensure_ascii=False)

    finalObj = {}
    finalObj['카페'] = cafeArr

    with open('doit-cafe' + '.json', 'w') as f:
        json.dump(finalObj, f, ensure_ascii=False)


crawl(
    'https://www.google.co.kr/maps/search/%EC%95%84%EC%A3%BC%EB%8C%80%ED%95%99%EA%B5%90+%EC%A3%BC%EB%B3%80+%EC%B9%B4%ED%8E%98/@37.2797233,127.0425144,17z/data=!3m1!4b1?hl=ko')

# time.sleep(2)

# 'https://www.google.com/search?q=%EC%95%84%EC%A3%BC%EB%8C%80%ED%95%99%EA%B5%90+%EC%A3%BC%EB%B3%80+%EC%B9%B4%ED%8E%98&biw=1920&bih=969&tbm=lcl&ei=JLXrYaDiEYuLr7wPuYSx6A4&oq=%EC%95%84%EC%A3%BC%EB%8C%80%ED%95%99%EA%B5%90+%EC%A3%BC%EB%B3%80+%EC%B9%B4%ED%8E%98&gs_l=psy-ab.3...124069.125195.0.125389.11.8.0.0.0.0.224.755.0j2j2.4.0....0...1c.1j4.64.psy-ab..11.0.0....0.av4oARCfteM#rlfi=hd:;si:;mv:[[37.28794358525591,127.05224516912608],[37.274319099594315,127.0319676689735],null,[37.281131650722244,127.04210641904979],16]'
# 'https://www.google.com/search?q=%EC%95%84%EC%A3%BC%EB%8C%80%ED%95%99%EA%B5%90+%EC%A3%BC%EB%B3%80+%EC%B9%B4%ED%8E%98&biw=1920&bih=969&tbm=lcl&ei=JLXrYaDiEYuLr7wPuYSx6A4&oq=%EC%95%84%EC%A3%BC%EB%8C%80%ED%95%99%EA%B5%90+%EC%A3%BC%EB%B3%80+%EC%B9%B4%ED%8E%98&gs_l=psy-ab.3...124069.125195.0.125389.11.8.0.0.0.0.224.755.0j2j2.4.0....0...1c.1j4.64.psy-ab..11.0.0....0.av4oARCfteM#rlfi=hd:;si:;mv:[[37.28794358525591,127.05224516912608],[37.274319099594315,127.0319676689735],null,[37.281131650722244,127.04210641904979],16];start:20'
# 'https://www.google.com/search?q=%EC%95%84%EC%A3%BC%EB%8C%80%ED%95%99%EA%B5%90+%EC%A3%BC%EB%B3%80+%EC%B9%B4%ED%8E%98&biw=1920&bih=969&tbm=lcl&ei=JLXrYaDiEYuLr7wPuYSx6A4&oq=%EC%95%84%EC%A3%BC%EB%8C%80%ED%95%99%EA%B5%90+%EC%A3%BC%EB%B3%80+%EC%B9%B4%ED%8E%98&gs_l=psy-ab.3...124069.125195.0.125389.11.8.0.0.0.0.224.755.0j2j2.4.0....0...1c.1j4.64.psy-ab..11.0.0....0.av4oARCfteM#rlfi=hd:;si:;mv:[[37.28794358525591,127.05224516912608],[37.274319099594315,127.0319676689735],null,[37.281131650722244,127.04210641904979],16];start:40'
