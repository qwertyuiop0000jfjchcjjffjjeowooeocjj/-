import os
import pandas as pd 
from selenium import webdriver
from selenium.webdriver.common.by import By


browser = webdriver.Chrome()
browser.maximize_window() # 창 최대화



url = 'https://finance.naver.com/sise/sise_market_sum.naver?&page='
browser.get(url)

#조회 항목 초기화
checkboxes = browser.find_elements(By.NAME, 'fieldIds')
for checkbox in checkboxes:
    if checkbox.is_selected(): # 체크된 상태라면?
        checkbox.click()



#조회 항목 설정(원하는 항목)
#items_to_select = ['영업이익', '자산총계', '매출액']
items_to_select = ['시가', '고가', '저가']
for checkbox in checkboxes:
    parent = checkbox.find_element(By.XPATH, '..') #부모 element
    label = parent.find_element(By.TAG_NAME, 'label')
    # print(label.text) #이름확인
    if label.text in items_to_select:
        checkbox.click() #선택항목과 일치 한다면

btn_apply = browser.find_element(By.XPATH, '//a[@href="javascript:fieldSubmit()"]')
btn_apply.click()

for idx in range(1, 40):
    # 사전작업 페이지이동
    browser.get(url + str(idx))



    # 데이터 추출
    df = pd.read_html(browser.page_source)[1]
    df.dropna(axis='index', how='all', inplace=True)
    df.dropna(axis='columns', how='all', inplace=True)
    if len(df) == 0:
        break

    #파일 저장
    f_name = 'sise.csv'
    if os.path.exists(f_name):
        df.to_csv(f_name, encoding='utf-8-sig', index=False, mode='a', header=False)
    else:
        df.to_csv(f_name, encoding='utf-8-sig', index=False)
    print(f'{idx} 페이지 완료')

browser.quit()#브라우저 종룟