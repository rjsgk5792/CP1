from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time

# DB_FILENAME = 'kream_400.db'
# DB_FILEPATH = os.path.join(os.getcwd(), DB_FILENAME)

# conn = sqlite3.connect(DB_FILENAME) #없으면 자동생성
# cur = conn.cursor()

# cur.execute("DROP TABLE IF EXISTS T_etc;")
# cur.execute("""CREATE TABLE T_etc(
# 				카테고리 NVARCHAR(50),
# 				세부카테고리 NVARCHAR(50),
#                 거래량 NVARCHAR(50),
#                 브랜드 NVARCHAR(100),
#                 상품명 NVARCHAR(150),
#                 최저구매가 NVARCHAR(50),
#                 저장수 NVARCHAR(50),
#                 피드수 NVARCHAR(50)
#                 ); 
# 			""")
def abc():
    columns=['브랜드', '상품명', '즉시구매가', '거래량','저장수'] 

    #창 숨기는 옵션 
    options = webdriver.ChromeOptions()
    options.add_argument("headless")
    driver = webdriver.Chrome("chromedriver",options=options)
    count = 0

    driver.get("https://kream.co.kr/search")

    #로그인
    driver.find_element(By.XPATH, '//*[@id="__layout"]/div/div[1]/div[1]/div/ul/li[4]/a').click()
    time.sleep(2)
    driver.find_element(By.XPATH,'//*[@id="__layout"]/div/div[2]/div[1]/div/div[1]/div/input').send_keys('emforhs0303@hanmail.net')
    driver.find_element(By.XPATH,'//*[@id="__layout"]/div/div[2]/div[1]/div/div[2]/div/input').send_keys('dks153153!')
    driver.find_element(By.XPATH,'//*[@id="__layout"]/div/div[2]/div[1]/div/div[3]/a').click()
    time.sleep(2)

    deal=driver.find_elements(By.CLASS_NAME,f'product')#거래량
    brand=driver.find_elements(By.CLASS_NAME,f'title')#브랜드&상품명
    price=driver.find_elements(By.CLASS_NAME,f'amount')#최저구매가
    save=driver.find_elements(By.CLASS_NAME,f'wish_figure')#저장수

    dicts={i : 0 for i in range(5)}
    value = []
    for i in range(10):
        print(i+1)
           
        value.extend(brand[i].text.split('\n')[:2])
        value.append(price[i].text)

        #수정한 부분
        if deal[i].text != '': 
            value.append(deal[i].text.split(' ')[1])
        else : value.append(0) #거래량이 없을 경우    

        value.append(save[i].text)
    
    return value