from selenium import webdriver
import time

from selenium.webdriver.common.by import By

url = 'https://jobs.dou.ua/companies/'
driver = webdriver.Chrome(executable_path='/home/btdl/PycharmProjects/scrapping_test/chromedriver')
driver.get(url=url)
time.sleep(2)
try:
    while True:
        div = driver.find_element(By.CLASS_NAME, 'more-btn')
        button = div.find_element(By.TAG_NAME, 'a')
        try:
            button.click()
            time.sleep(0.5)
        except:
            print('Can`t click')
            with open("/home/btdl/PycharmProjects/scrapping_test/companies.html", "w") as f:
                f.write(driver.execute_script("return document.getElementsByTagName('html')[0].innerHTML"))
            break
except Exception as e:
    print(e)
finally:
    driver.close()
    driver.quit()
