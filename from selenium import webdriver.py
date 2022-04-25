from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.service import Service



options = webdriver.FirefoxOptions()
options.add_argument('--headless')
# executable_path param is not needed if you updated PATH
#PATH = "C:\Users\Gregory Robben\SynologyDrive\Documents\Drivers\geckodriver.exe"
PATH = "C:\\Users\\Gregory Robben\\SynologyDrive\\Documents\\Drivers\geckodriver.exe"
s = Service(PATH)
browser = webdriver.Firefox(options=options, service=s)

try:
    
    browser.get("https://support.sonos.com/s/article/3521?language=en_US")
    timeout_in_seconds = 10
    WebDriverWait(browser, timeout_in_seconds).until(ec.presence_of_element_located((By.CLASS_NAME, 'row')))
    
    heading2 = browser.find_element(by=By.CSS_SELECTOR, value='h2').text
    print(heading2)
    html = browser.page_source
    #soup = BeautifulSoup(html, features="html.parser")
    soup = BeautifulSoup(html, "lxml")
    for script in soup(["script", "style"]):
        script.extract() 
    soup = soup.get_text()
    #print(soup)
except TimeoutException:
    print("I give up...")
finally:
    browser.quit()