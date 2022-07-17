from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

#from webdriver_manager.chrome import ChromeDriverManager
#import os

#os.environ['WDM_LOG_LEVEL'] = '0'

def get_soup(siteaddress):

    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    #options.add_experimental_option('excludeSwitches', ['enable-logging'])
    #try:
    #    s = Service(ChromeDriverManager().install())
    #except ValueError:
    #    s = Service('/usr/bin/chromedriver')
    #except FileNotFoundError:
    #    return "Error: driver not found"
    browser = webdriver.Chrome(options=options)#, service=s)
    #browser = webdriver.Chrome()
    try:
        browser.get(siteaddress)
        timeout_in_seconds = 1200
        WebDriverWait(browser, timeout_in_seconds).until(ec.presence_of_element_located((By.CLASS_NAME, 'row')))
        html = browser.page_source
        # parse the webpage for html
        soup = BeautifulSoup(html, 'html.parser')

        #soup = soup.get_text()
        soup = soup.prettify()
        #print(soup)
    except TimeoutException:
        #print("Did not find class_name 'row'...giving up...")
        soup = "Error: Did not find class_name 'row'...could not parse webpage" 
    finally:
        browser.quit()
    return soup