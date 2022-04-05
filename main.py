# Importing libraries
import time
import hashlib
from urllib.request import urlopen, Request
import requests
from bs4 import BeautifulSoup
import difflib
import time
from datetime import datetime

def site_changes(siteaddress : str):
    # target URL
    url = siteaddress
    # act like a browser
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:98.0) Gecko/20100101 Firefox/98.0'}

    PrevVersion = ""
    FirstRun = True
    while True:

        # download the page
        certificate_location = "\Sonos-Release-Notes\sonos-cert.cer"
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
                OldPage = NewPage
                #print ('\n'.join(diff))
                PrevVersion = soup
        else:
            print( "No Changes "+ str(datetime.now()))
        time.sleep(10)
        continue


def main(url):
    site_changes(url)

if __name__ == "__main__":
    main()
