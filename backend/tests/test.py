from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.common.actions import key_actions
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.action_chains import ActionChains
#open website
driver = webdriver.Chrome("chromedriver.exe")
driver.get("http://localhost:3000/")

#click on sign in button
sign_in_button = driver.find_element(By.ID,"sign_in_button")
sign_in_button.click()

driver.find_element(By.NAME,'username').send_keys('test')
driver.find_element(By.NAME,'password').send_keys('1234')
driver.find_element(By.XPATH,"//*[contains(text(), 'Submit')]").click()
ActionChains(driver).key_down(Keys.ESCAPE).perform()
time.sleep(0.25)

driver.find_element(By.ID,'search_button').click()
driver.find_element(By.NAME,'search').send_keys('wanda')
time.sleep(0.25)
driver.find_element(By.CLASS_NAME,'movieCard').click()

ActionChains(driver).move_to_element(driver.find_element(By.XPATH,"//*[contains(text(), '25')]")).click().perform()
ActionChains(driver).move_to_element(driver.find_element(By.XPATH,"//*[contains(text(), '26')]")).click().perform()
ActionChains(driver).move_to_element(driver.find_element(By.XPATH,"//*[contains(text(), '27')]")).click().perform()
driver.find_element(By.XPATH,"//*[contains(text(), 'Book Now')]").click()
time.sleep(5)
driver.switch_to.frame(driver.find_element(By.CLASS_NAME,"razorpay-checkout-frame"))
driver.find_element(By.XPATH,"//*[@method='card']").click()
time.sleep(0.25)
driver.find_element(By.NAME,'card[number]').send_keys("5267 3181 8797 5449")
driver.find_element(By.NAME,'card[expiry]').send_keys("03/24")
driver.find_element(By.NAME,'card[cvv]').send_keys("522")
time.sleep(1)
driver.find_element(By.XPATH,"//*[contains(text(), 'Pay Now')]").click()
time.sleep(2)
driver.find_element(By.XPATH,"//*[contains(text(), 'Skip saving card')]").click()

time.sleep(100)

driver.quit()

