import datetime
import os
import urllib.request
import selenium
import time
import random
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait

URL = 'https://www.ssfshop.com/8seconds/main?dspCtgryNo=&brandShopNo=BDMA07A01&brndShopId=8SBSS&leftBrandNM='
driver = webdriver.Chrome(executable_path='./chromedriver')
driver.get(url=URL)
driver.implicitly_wait(time_to_wait=5)

#폴더 생성
TOP_DIR_PATH='./WOMEN_TOP'
try : 
    if not(os.path.isdir(TOP_DIR_PATH)):
        os.makedirs(os.path.join(TOP_DIR_PATH))
except OSError as e:
    if e.errno != errno.EEXIST:
        print("failed to create directory")
        raise

#카테고리 (index 1~5까지 women-top)
for categories in range(1, 6):
    big = driver.find_elements_by_class_name('big')[0]
    big.find_elements_by_xpath('./li')[0].find_elements_by_xpath('./ul')[0].find_elements_by_xpath('./li')[categories].find_elements_by_xpath('./a')[0].click()
    driver.implicitly_wait(time_to_wait=3)

    pages = driver.find_elements_by_css_selector('#pagingArea')[0].find_elements_by_xpath('./a')
    #한 카테고리 내 페이지
    for page in range(1, len(pages)):
        #한 페이지 내 상품
        dspGood_li = driver.find_element_by_id('dspGood').find_elements_by_xpath('./li')
        for goods in range(0, len(dspGood_li)):
            dspGood_li = driver.find_element_by_id('dspGood').find_elements_by_xpath('./li')
            dspGood_li[goods].find_elements_by_xpath('./a')[0].click()
            driver.implicitly_wait(time_to_wait=3)

            #한 상품 내 상세 이미지
            image_other_li = driver.find_elements_by_class_name('lSGallery')[0].find_elements_by_xpath('./ul')[0].find_elements_by_xpath('./li')
            
            #상세 이미지 확대
            driver.find_elements_by_css_selector('.zoom-in.active>a')[0].click()
            driver.implicitly_wait(time_to_wait=3)

            for photos in range(0, len(image_other_li)):
                #상세 이미지 저장
                try : 
                    zoom = WebDriverWait(driver,-1).until( 
                        EC.presence_of_element_located((By.ID,'zoom')))
                    image_src = zoom.find_elements_by_css_selector('.lslide.active img')[0].get_attribute('src')
                    filename = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S-%f') + '.jpg'
                    full_path = TOP_DIR_PATH + '/' + filename
                    urllib.request.urlretrieve(image_src, full_path)
                except : 
                    continue
                
                #다음 상세 이미지 불러오기
                driver.find_element_by_id('zoom').find_element_by_class_name('lSNext').click() #driver.find_elements_by_css_selector('#zoom .lSNext')[0].click()
                driver.implicitly_wait(time_to_wait=1)

            driver.back()
            pages = driver.find_elements_by_css_selector('#pagingArea')[0].find_elements_by_xpath('./a')
            
            if (page != len(pages)-1) :
                if(page>=2):
                    page = page + 1
                pages[page].click()
                driver.implicitly_wait(time_to_wait=3)  
            
driver.close()
driver.quit();
