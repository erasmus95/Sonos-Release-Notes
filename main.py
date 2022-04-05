# Importing libraries
import email
import time
import hashlib
import certifi
import urllib3
urllib3.disable_warnings()
from urllib.request import urlopen, Request
import requests
from bs4 import BeautifulSoup
import difflib
import time
from datetime import datetime
import smtplib
import ssl

def site_changes(siteaddress : str):
    # target URL
    url = siteaddress
    # act like a browser
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36'}

    PrevVersion = ""
    FirstRun = True
    while True:

        # download the page
        #certificate_location = 'C:\Users\Gregory_Robben\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.9_qbz5n2kfra8p0\LocalCache\local-packages\Python39\site-packages\certifi\cacert.pem'

        http = urllib3.PoolManager(cert_reqs ='CERT_REQUIRED',
                                ca_certs=certifi.where()
        )
        #response = http.request('GET',siteaddress)#,headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:98.0) Gecko/20100101 Firefox/98.0'})
        response = requests.get(url, headers= headers, verify = False)
        # parse the downloaded homepage
        soup = BeautifulSoup(response.text, "lxml")
        
        # remove all scripts and styles
        for script in soup(["script", "style"]):
            script.extract() 
        soup = soup.get_text()
        # compare the page text to the previous version
        if PrevVersion != soup:
            # on the first run - just memorize the page
            if FirstRun == True:
                PrevVersion = soup
                FirstRun = False
                print ("Start Monitoring "+url+ ""+ str(datetime.now()))
            else:
                print ("Changes detected at: "+ str(datetime.now()))
                OldPage = PrevVersion.splitlines()
                NewPage = soup.splitlines()
                # compare versions and highlight changes using difflib
                #d = difflib.Differ()
                #diff = d.compare(OldPage, NewPage)
                diff = difflib.context_diff(OldPage,NewPage,n=10)
                out_text = "\n".join([ll.rstrip() for ll in '\n'.join(diff).splitlines() if ll.strip()])
                print (out_text)
                email_alert(out_text)
                OldPage = NewPage
                #print ('\n'.join(diff))
                PrevVersion = soup
        else:
            print( "No Changes "+ str(datetime.now()))
        time.sleep(10)
        continue

def email_alert(message:str):
    # create an email message with just a subject line,
    msg = '''\
            From: gregoryrobben@gmail.com
            Subject: Sonos app update

            ''' + message
    # set the 'from' address,
    fromaddr = 'gregoryrobben@gmail.com'
    # set the 'to' addresses,
    toaddrs  = ['gregoryrobben@gmail.com']#,'A_SECOND_EMAIL_ADDRESS', 'A_THIRD_EMAIL_ADDRESS']
    
    # setup the email server,
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    # add my account login name and password,
    server.login("gregoryrobben@gmail.com", "ujsazigsqebantxz")
    
    # Print the email's contents
    print('From: ' + fromaddr)
    print('To: ' + str(toaddrs))
    print('Message: ' + msg)
    
    # send the email
    server.sendmail(fromaddr, toaddrs, msg)
    # disconnect from the server
    server.quit()

def main(url):
    site_changes(url)

if __name__ == "__main__":
    main("https://support.sonos.com/s/article/3521?language=en_US")
