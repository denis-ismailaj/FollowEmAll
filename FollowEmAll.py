from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, WebDriverException
from selenium.webdriver.common.keys import Keys
from time import sleep

driver = webdriver.Firefox()
driver.get("https://www.instagram.com/accounts/login/")

sleep(1)

username = driver.find_element_by_name("username")
password = driver.find_element_by_name("password")

username.send_keys("usrn")
password.send_keys("passw")

driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/article/div/div[1]/div/form/span/button').submit()

sleep(2)

driver.get("https://www.instagram.com/instagram/")

driver.find_element_by_xpath('//*[@id="react-root"]/section/main/article/header/div[2]/ul/li[2]/a').click()

sleep(2)
    
index = 1

window = driver.find_element_by_xpath('/html/body/div[2]/div/div[2]/div/div[2]')

while True:
    try:
        while True:
            button = driver.find_element_by_xpath('/html/body/div[2]/div/div[2]/div/div[2]/ul/li[{}]/div/div[2]/span/button'.format(index))
            if driver.execute_script("return arguments[0].innerText;", button) == "Follow":
                button.click()
            index += 1
    except NoSuchElementException:
        try:
            # driver.execute_script("arguments[0].scrollTo(0, arguments[0].scrollHeight);", window)
            sleep(1.5)
        except WebDriverException:
            pass
            # sleep(6)
            # driver.find_element_by_xpath('//*[@id="react-root"]/section/main/article/header/div[2]/ul/li[2]/a').click()
    except KeyboardInterrupt:
        driver.close()
