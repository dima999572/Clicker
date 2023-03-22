from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re


options = webdriver.ChromeOptions()
options.add_experimental_option('detach', True)

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.get('https://orteil.dashnet.org/cookieclicker/')

wait = WebDriverWait(driver, 5)

wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/div[2]/div[1]/div[2]/div[2]/button[1]')))
driver.find_element(By.XPATH, '/html/body/div[3]/div[2]/div[1]/div[2]/div[2]/button[1]').click()

wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="langSelect-EN"]')))
driver.find_element(By.XPATH, '//*[@id="langSelect-EN"]').click()

wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="bigCookie"]')))

button = driver.find_element(By.XPATH, '//*[@id="bigCookie"]') 

pattern = re.compile("^[0-9]+(\,*[0-9]*)?(\.*[0-9]*[a-z]*)$")
str_pattern = re.compile("^[a-z]*$")

current_time = round(time.time())
while True:
    button.click()
    if time.time() - current_time > 5:
        current_time = time.time()
      
        paths = driver.find_element(By.ID, "products").find_elements(By.CLASS_NAME, "price")
        prices = [{int(re.sub(str_pattern, "", path.text.replace(",", "").replace(".", "").replace(" ", ""))) : path} for path in paths if pattern.match(path.text)]
        balance = int(driver.find_element(By.XPATH, '//*[@id="cookies"]').text.split(" ")[0].replace(",", ""))
        for counter in range(len(prices) - 1, -1, -1):
            cost = int(list(prices[counter])[0])
            if balance >= cost:
                driver.find_element(By.XPATH, f'//*[@id="product{counter}"]').click()


        