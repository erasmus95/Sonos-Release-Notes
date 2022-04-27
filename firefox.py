from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.firefox import GeckoDriverManager
import os
os.environ['WDM_LOG_LEVEL'] = '0'

def get_soup(siteaddress):
    options = webdriver.FirefoxOptions()
    # using headless so that a window doesn't pop-up and need to load as well
    options.add_argument('--headless')
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    try:
        service = Service(GeckoDriverManager().install())
    except ValueError:
        service = Service('/usr/bin/geckodriver')
    except FileNotFoundError:
        return "Error: driver not found"
    # using webdriver-manager we can dynamically get the driver location and avoid hard coding it
    
    browser = webdriver.Firefox(options=options, service=service)
    
    try:
        browser.get(siteaddress)
        timeout_in_seconds = 10
        #WebDriverWait waits until a certain item if found on the webpage, in this case class = 'row'. 
        # This is because some pages load in data after the inital load
        WebDriverWait(browser, timeout_in_seconds).until(ec.presence_of_element_located((By.CLASS_NAME, 'row')))
        html = browser.page_source
        # parse the webpage for html
        soup = BeautifulSoup(html, 'html.parser')
        soup = soup.get_text()
        #print(soup)
    except TimeoutException:
        #print("Did not find class_name 'row'...giving up...")
        soup = "Error: Did not find class_name 'row'...could not parse webpage" 
    finally:
        browser.quit()

    return soup