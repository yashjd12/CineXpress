from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

#open website
try:
    o = webdriver.ChromeOptions()
    o.add_argument("--user-data-dir=C:/Users/sahil/AppData/Local/Google/Chrome/User Data/Default")
    driver = webdriver.Chrome(executable_path="C:/Users/sahil/Downloads/chromedriver.exe",chrome_options=o)
    driver.maximize_window()
    driver.get("http://localhost:3000/")

    #click on sign in button
    sign_in_button = driver.find_element(By.ID,"sign_in_button")
    sign_in_button.click()
    print("-Signup modal opened")

    #switch to sign in page
    or_signup_instead = driver.find_element(By.XPATH,"//*[contains(text(), 'Or Signup Instead')]")
    or_signup_instead.click()
    print("-Switched to sign in page")

    #fill signup form
    driver.find_element(By.NAME,'first_name').send_keys('Sahil')
    driver.find_element(By.NAME,'last_name').send_keys('Nawale')
    driver.find_element(By.NAME,'username').send_keys('SahilNawale')
    driver.find_element(By.NAME,'email').send_keys('sahilnawale@gmail.com')
    driver.find_element(By.NAME,'password').send_keys('1234')
    driver.find_element(By.NAME,'confirm_password').send_keys('1234')
    print("-Sign up form filled")

    #click signup button
    driver.find_element(By.XPATH,"//*[contains(text(), 'Submit')]").click()

    #switch to login
    driver.find_element(By.XPATH,"//*[contains(text(), 'Or Login Instead')]").click()
    print("-Signup successfull")

    #login
    driver.find_element(By.XPATH,"//*[contains(text(), 'Submit')]").click()
    print("-Login successfull")

    #close login modal
    ActionChains(driver).key_down(Keys.ESCAPE).perform()

    #go to profile
    driver.find_element(By.ID,'profile_button').click()
    time.sleep(1)
    driver.find_element(By.XPATH,"//*[contains(text(), 'Profile')]").click()
    time.sleep(1)
    print("-Navigated to profile page")

    #edit profile
    driver.find_element(By.XPATH,"//*[contains(text(), 'Edit Profile')]").click()
    for i in range(100):
        driver.find_element(By.NAME,'email').send_keys(Keys.BACK_SPACE)
    driver.find_element(By.NAME,'email').send_keys("sahilnawale2@gmail.com")
    time.sleep(1)
    driver.find_element(By.XPATH,"//*[contains(text(), 'Submit')]").click()
    driver.refresh()
    print("-Profile edited")

    #search for movies
    time.sleep(2)
    driver.find_element(By.ID,'search_button').click()
    driver.find_element(By.NAME,'search').send_keys('wanda')
    time.sleep(1)
    driver.find_element(By.CLASS_NAME,'movieCard').click()
    print("-Movie Searched successfully")

    #select movies seats
    ActionChains(driver).move_to_element(driver.find_element(By.XPATH,"//*[contains(text(), '25')]")).click().perform()
    ActionChains(driver).move_to_element(driver.find_element(By.XPATH,"//*[contains(text(), '26')]")).click().perform()
    ActionChains(driver).move_to_element(driver.find_element(By.XPATH,"//*[contains(text(), '27')]")).click().perform()
    print("-Seats selected")

    # Book seats
    driver.find_element(By.XPATH,"//*[contains(text(), 'Book Now')]").click()

    #make payment with razorpay
    time.sleep(5)
    driver.switch_to.frame(driver.find_element(By.CLASS_NAME,"razorpay-checkout-frame"))
    driver.find_element(By.XPATH,"//*[@method='card']").click()
    print("-Card payment initiated")
    time.sleep(2)
    driver.find_element(By.NAME,'card[number]').send_keys("5267 3181 8797 5449")
    driver.find_element(By.NAME,'card[expiry]').send_keys("03/24")
    driver.find_element(By.NAME,'card[cvv]').send_keys("522")
    print("-Card Details Entered")
    time.sleep(1)
    driver.find_element(By.XPATH,"//*[contains(text(), 'Pay Now')]").click()
    time.sleep(2)
    driver.find_element(By.XPATH,"//*[contains(text(), 'Skip saving card')]").click()
    print("-Payment Tested")

    print(" \n\n\n_______ Test Success ________\n\n\n")

    time.sleep(100)

    driver.quit()

except :
    print(" \n\n\n_______ Test Failed ________\n\n\n")
    exit()