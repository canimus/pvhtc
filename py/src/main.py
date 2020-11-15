# Browser Interaction
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys

# User Agent Strings
from fake_useragent import UserAgent

# Image Handling
from operator import methodcaller as mc
import numpy as np
import pytesseract
from PIL import Image

# Style Output
import chalk
import time
import sys

EMAIL_WAIT_THRESHOLD = 90 # Seconds

def set_chrome_options() -> None:
    """Sets chrome options for Selenium.
    Chrome options for headless browser is enabled.
    """
    ua = UserAgent()
    userAgent = ua.random

    chrome_options = Options()
    chrome_options.add_argument(f'user-agent={userAgent}')
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_prefs = {}
    chrome_options.experimental_options["prefs"] = chrome_prefs
    chrome_prefs["profile.default_content_settings"] = {"images": 2}
    return chrome_options

if __name__ == "__main__":
    driver = webdriver.Chrome(options=set_chrome_options())
    driver.get("https://emailfake.com/")
    print('EmailGenerator:' + driver.title)

    # Email is imaged as a pair of inputs
    inputs = driver.find_elements_by_tag_name("input")

    ocr = {'email' : 0, 'domain' : 2}
    list(map(lambda x: mc("screenshot", f'/scripts/{x[0]}.png')(inputs[x[1]]), ocr.items()))
    
    email, domain = [pytesseract.image_to_string(Image.open(f'/scripts/{i}.png')).strip() for i in ocr.keys()]

    print(f'Email:[{email}] Check=>{len(email)>0}')
    print(f'Domain:[{domain}] Check=>{len(domain)>0}')

    if len(email)>0 and len(domain)>0:
        print(chalk.cyan("Email Ok"))
    else:
        print(chalk.red("Sorry, my eyes are tired and couldn't parse your email"))
        sys.exit()

    # Induced garbage caracter in domain by image
    if not domain[0].isalnum():
        domain = domain[1:]


    email_address = f'{email}@{domain}'
    print(chalk.magenta(email_address, bold=True))

    # With an account lets try to register
    driver2 = webdriver.Chrome(options=set_chrome_options())
    driver2.maximize_window()
    driver2.get("https://nl.tommy.com/")
    driver2.get_screenshot_as_file('/scripts/tommy_0.png')

    screen_0 = Image.open("/scripts/tommy_0.png")
    assert np.isclose(screen_0.entropy(), 7, rtol=.15) 
    print("Entropy Close Verification")
    
    print("WebSite: " + driver2.title)
    assert "Tommy Hilfiger" in driver2.title

    tommy_logo = driver2.find_element_by_xpath("//a[@title='Tommy Hilfiger']")
    ac = ActionChains(driver2)
    if tommy_logo:
        print('Pointer at Page Logo')
        ac.move_to_element(tommy_logo)
        driver2.get_screenshot_as_file(f'/scripts/tommy_1.png')

    accept_cookies_banner = driver2.find_element_by_xpath("//div[@class='cookie-notice__action']/button[1]")
    if accept_cookies_banner:
        print('Cookies Agreement Banner')
        accept_cookies_banner.click()
        driver2.get_screenshot_as_file(f'/scripts/tommy_2.png')

    free_shipping_banner = driver2.find_element_by_xpath("//button[@class='slide__background--close']")
    if free_shipping_banner:
        print("Shipping Free Banner")
        free_shipping_banner.click()
        driver2.get_screenshot_as_file(f'/scripts/tommy_3.png')

    registration_button = driver2.find_element_by_xpath("//button[@class='header__link']")
    if registration_button:
        print("Opening Registration Panel")
        registration_button.click()
        WebDriverWait(driver2, 2).until(EC.visibility_of_element_located((By.XPATH, "//input[@type='email' and @name='email1']")))
        driver2.get_screenshot_as_file(f'/scripts/tommy_4.png')

    email_field = driver2.find_element_by_xpath("//input[@type='email' and @name='email1']")
    if email_field:
        print("Entering Email")
        email_field.send_keys(email_address)
        driver2.get_screenshot_as_file(f'/scripts/tommy_5.png')

    password_field = driver2.find_element_by_xpath("//div[@class='register__passwords']//input[@type='password' and @name='logonPassword']")
    if password_field:
        print("Entering Password")
        password_field.send_keys("TommyChallenge2020")
        driver2.get_screenshot_as_file(f'/scripts/tommy_6.png')

    password_confirmation_field = driver2.find_element_by_xpath("//div[@class='register__passwords']//input[@type='password' and @name='logonPasswordVerify']")
    if password_confirmation_field:
        print("Confirmation Password")
        password_confirmation_field.send_keys("TommyChallenge2020")
        driver2.get_screenshot_as_file(f'/scripts/tommy_7.png')
    
    accept_terms = driver2.find_element_by_xpath("//label[@for='signUpForTermsCondition1']")
    if accept_terms:
        print("Accept Terms and Conditions")
        accept_terms.click()
        driver2.get_screenshot_as_file(f'/scripts/tommy_8.png')

    button_registration = driver2.find_element_by_xpath("//button[contains(text(), 'Registreren') and @type='submit']")
    if button_registration:
        print("Complete Registration")
        button_registration.click()
        WebDriverWait(driver2, timeout=10, poll_frequency=2).until(EC.title_contains('Mijn account'))
        driver2.get_screenshot_as_file(f'/scripts/tommy_9.png')
    
    # TODO: Address the wait with Expected Condition. Left on purpose    
    time.sleep(EMAIL_WAIT_THRESHOLD)

    print(chalk.yellow("New Mail!"))

    # TODO: Actions.movo_to element but this also works
    email_body = driver.find_element_by_tag_name('body')
    email_body.send_keys(Keys.PAGE_DOWN)
    email_body.send_keys(Keys.PAGE_DOWN)
    
    driver.get_screenshot_as_file(f'/scripts/tommy_10.png')
    print(chalk.green("OK"))
    driver.quit()