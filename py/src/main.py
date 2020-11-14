from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from fake_useragent import UserAgent
from operator import methodcaller as mc
import pytesseract
from PIL import Image
import chalk
import time

def set_chrome_options() -> None:
    """Sets chrome options for Selenium.
    Chrome options for headless browser is enabled.
    """
    ua = UserAgent()
    userAgent = ua.random
    print(userAgent)

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

    # Induced garbage caracter in domain by image
    if not domain[0].isalnum():
        domain = domain[1:]

    print(chalk.magenta(f'{email}@{domain}', bold=True))

    # With an account lets try to register
    driver2 = webdriver.Chrome(options=set_chrome_options())
    driver2.maximize_window()
    driver2.get("https://nl.tommy.com/")
    driver2.get_screenshot_as_file(f'/scripts/tommy_1.png')
    
    print("WebSite: " + driver2.title)
    assert "Tommy Hilfiger" in driver2.title

    accept_cookies = driver2.find_element_by_xpath("//div[@class='cookie-notice__action']/button[1]")
    if accept_cookies:
        print('Cookies Agreement')
        accept_cookies.click()
        driver2.get_screenshot_as_file(f'/scripts/tommy_2.png')

    print("Verification: " + driver.title)
    driver.quit()