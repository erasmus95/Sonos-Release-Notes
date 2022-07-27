from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait

def getSoup(options, service, siteaddress):
    browser = webdriver.Chrome(options=options, service=service)
    try:
        browser.get(siteaddress)
        timeout_in_seconds = 1200
        WebDriverWait(browser, timeout_in_seconds).until(ec.presence_of_element_located((By.CLASS_NAME, 'row')))
        html = browser.page_source
        ## parse the webpage for html
        soup = BeautifulSoup(html, 'html.parser')

        soup = soup.prettify()
        
    except TimeoutException:
        ##print("Did not find class_name 'row'...giving up...")
        soup = "Error: Did not find class_name 'row'...could not parse webpage" 
    finally:
        browser.quit()
    return soup