# Importing libraries
#from pickle import FALSE
import urllib3
urllib3.disable_warnings()
from bs4 import BeautifulSoup
import difflib
from datetime import datetime
import smtplib
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
from email.message import EmailMessage

def is_initial_run(file : str):
    '''
    Tests whether or not this is the initial run of the script
    '''
    with open(file) as f:
        count = sum(1 for _ in f)
    
    if count > 1: return False
    else: return True
def current_version(soup : str):
    #find the line number of "Current software version"
    start = soup.find("Current software version")
    #find the line number of "Previous software vesrions"
    end = soup.find("Previous software versions")
    
    return soup[start:end].strip()#.encode(encoding = 'UTF-8', errors = 'strict')

def Initial_Run(file_to_write_to : str,text_to_write):
    '''
    If the PreviousVersion file is empty then it is the initial run. 
    The soup is written to the file to act as the reference for the script going forward until an update occurs
    '''
    with open(file_to_write_to,'w',encoding='utf-8') as file:
        file.write(text_to_write)
        file.close()

def read_previous_version(file:str):
    with open(file, 'r', encoding='utf-8') as file_to_read:
        output = file_to_read.read()
    return output

def write_to_log(file:str,message:str):
    '''
    Writes the message to a privded log file
    Parameters: file to write to, string to append to the log file
    '''
    with open(file,'a') as file:
        file.write(message)

def email_alert(message:str):
   
    # create an email message with just a subject line,
    msg = EmailMessage()
    msg['From'] = "gregoryrobben@gmail.com"
    msg['To'] = "gregoryrobben@gmail.com"
    msg['Subject'] = "Sonos app update!"
    msg.set_payload(message.replace("Current","Previous",1).encode(encoding = 'UTF-8', errors = 'strict'));
    msg.as_string()
    # set the 'from' address,
    fromaddr = "gregoryrobben@gmail.com"
    # set the 'to' addresses,
    toaddrs  = ["gregoryrobben@gmail.com"]#,'A_SECOND_EMAIL_ADDRESS', 'A_THIRD_EMAIL_ADDRESS']
    
    # setup the email server,
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    # add my account login name and password,
    server.login("gregoryrobben@gmail.com", "ujsazigsqebantxz")
    
    # Print the email's contents
    print('From: ' + fromaddr)
    print('To: ' + str(toaddrs))
    print('Message: ' + message.replace("Current","Previous",1))
    
    # send the email
    #server.sendmail(fromaddr, toaddrs, msg.encode(encoding = 'UTF-8', errors = 'strict'),)
    server.send_message(msg)
    # disconnect from the server
    server.quit()

def site_changes(siteaddress : str,title:str):
    #set our static variables
    url = siteaddress
    log_file = title + '_monitoring_log.txt'
    updates_file = title + '_updates.txt'
    PreviousVersion_file = title + '_PreviousVersion.txt'
    # act like a browser
    #headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36'}

    options = webdriver.FirefoxOptions()
    options.add_argument('--headless')
    # executable_path param is not needed if you updated PATH
    #PATH = "C:\Users\Gregory Robben\SynologyDrive\Documents\Drivers\geckodriver.exe"
    #PATH = "C:\\Users\\Gregory Robben\\SynologyDrive\\Documents\\Drivers\geckodriver.exe"
    #s = Service(PATH)
    s = Service(GeckoDriverManager().install())

    browser = webdriver.Firefox(options=options, service=s)
    
    #determin if this is the first run of the script for the given site.
    FirstRun = is_initial_run(PreviousVersion_file)

    if FirstRun:
        PrevVersion = ""
    else:
        PrevVersion = read_previous_version(PreviousVersion_file)
    
    try:
    
        browser.get("https://support.sonos.com/s/article/3521?language=en_US")
        timeout_in_seconds = 10
        WebDriverWait(browser, timeout_in_seconds).until(ec.presence_of_element_located((By.CLASS_NAME, 'row')))
        #time.sleep(10)
        html = browser.page_source
        #soup = BeautifulSoup(html, features="html.parser")
        # parse the webpage for lxml
        soup = BeautifulSoup(html, 'html.parser')
        
        soup = soup.get_text()
        #print(soup)
    except TimeoutException:
        print("Did not find class_name 'row'...giving up...")
    finally:
        browser.quit()
    
    CurVersion = current_version(soup)
    # compare the page text to the previous version
    if PrevVersion != CurVersion:
        # on the first run - just memorize the page
        if FirstRun == True:
            PrevVersion = CurVersion
            Initial_Run(PreviousVersion_file,CurVersion)
            #FirstRun = False
            start_message = "Start Monitoring "+url+ ""+ str(datetime.now())
            write_to_log(log_file,start_message +"\n")
            print (start_message)
        else:
            change_message = "Changes detected at: "+ str(datetime.now())
            write_to_log(log_file,change_message +"\n")
            print (change_message)
            OldPage = PrevVersion.splitlines()
            NewPage = CurVersion.splitlines()
            # compare versions and highlight changes using difflib
            #d = difflib.Differ()
            #diff = d.compare(OldPage, NewPage)
            diff = difflib.context_diff(OldPage,NewPage,n=10)
            out_text = "\n".join([ll.rstrip() for ll in '\n'.join(diff).splitlines() if ll.strip()])
            write_to_log(updates_file,out_text)
            write_to_log (log_file,"Update detected" + str(datetime.now()))
            email_alert(out_text)
            #OldPage = NewPage
            #print ('\n'.join(diff))
            #PrevVersion = CurVersion
            Initial_Run(PreviousVersion_file,CurVersion)
    else:
        no_change_message = "No Changes "+ str(datetime.now())
        write_to_log(log_file,no_change_message)
        print(no_change_message)

def main(url,title:str):
    site_changes(url,title)

if __name__ == "__main__":
    main("https://support.sonos.com/s/article/3521?language=en_US","s2")
