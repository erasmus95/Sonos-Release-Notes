#!user/bin/env python3


import difflib
import os
import re
import smtplib
from datetime import datetime
from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from post_to_reddit import Reddit_Post
import markdownify
import urllib3
urllib3.disable_warnings()

def is_initial_run(file: str):
    """
    Tests whether or not this is the initial run of the script
    """
    with open(file) as f:
        count = sum(1 for _ in f)

    if count > 1:
        return False
    else:
        return True


def current_version(soup: str):
    # find the line number of "Current software version"
    start = soup.find("Current software version")
    # find the line number of "Previous software vesrions"
    end = soup.find("Previous software versions")
    
    #scrubed_aura_time = re.sub('data-aura-rendered-by="\d\d:\d\d\d;a"',soup[start:end])
    return soup[start:end].replace('data-aura-rendered-by="12:319;a"',"").strip()  # .encode(encoding = 'UTF-8', errors = 'strict')
    

def Write_To_File(file_to_write_to: str, text_to_write):
    """
    The provided text is written to the file
    """
    with open(file_to_write_to, "w", encoding="utf-8") as file:
        file.write(text_to_write)
        file.close()


def read_previous_version(file: str):
    with open(file, "r", encoding="utf-8") as file_to_read:
        output = file_to_read.read()
    return output


def write_to_log(file: str, message: str):
    """
    Writes the message to a privded log file
    Parameters: file to write to, string to append to the log file
    """
    with open(file, "a") as file:
        file.write(message)


def email_alert(message: str):

    # create an email message with just a subject line,
    msg = EmailMessage()
    msg["From"] = "gregoryrobben@gmail.com"
    msg["To"] = "gregoryrobben@gmail.com"
    msg["Subject"] = "Sonos app update!"
    msg.set_payload(
        message.replace("Current", "Previous", 1).encode(
            encoding="UTF-8", errors="strict"
        )
    )
    msg.as_string()
    # set the 'from' address,
    fromaddr = "gregoryrobben@gmail.com"
    # set the 'to' addresses,
    toaddrs = [
        "gregoryrobben@gmail.com"
    ]  # ,'A_SECOND_EMAIL_ADDRESS', 'A_THIRD_EMAIL_ADDRESS']

    # setup the email server,
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    # add my account login name and password,
    server.login("gregoryrobben@gmail.com", "ujsazigsqebantxz")

    # Print the email's contents
    print("From: " + fromaddr)
    print("To: " + str(toaddrs))
    print("Message: " + message.replace("Current", "Previous", 1))

    # send the email
    # server.sendmail(fromaddr, toaddrs, msg.encode(encoding = 'UTF-8', errors = 'strict'),)
    server.send_message(msg)
    # disconnect from the server
    server.quit()

def fancy_email_alert(message: str):
    # create an email message with just a subject line,
    msg = MIMEMultipart()
    msg["From"] = "gregoryrobben@gmail.com"
    msg["To"] = "gregoryrobben@gmail.com"
    msg["Subject"] = "Sonos app update!"

    msg.attach(MIMEText("".join(message),'html'))#.replace("Current", "Previous", 1), 'html'))
    
    text = msg.as_string()
    
    ## set the 'from' address,
    fromaddr = "gregoryrobben@gmail.com"
    ## set the 'to' addresses,
    toaddrs = [
        "gregoryrobben@gmail.com"
    ]  # ,'A_SECOND_EMAIL_ADDRESS', 'A_THIRD_EMAIL_ADDRESS']

    ## setup the email server,
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        ## add my account login name and password,
        server.login("gregoryrobben@gmail.com", "ujsazigsqebantxz")
        server.sendmail(fromaddr,toaddrs,text)
    finally:
        ## disconnect from the server
        server.quit()
    
def send_to_reddit(text):
    start_of_version = text.find("\n",text.find("</h2>")+10)
    end_of_version = text.find("</h2>",text.find("</h2>")+1)
    title = "Sonos S2 Firmware v." + (text[start_of_version:end_of_version].strip()) + " Avaliable"

    body = text[text.find("\n"):]
    markeddown = markdownify.markdownify(body, heading_style="ATX")
    update_post = Reddit_Post(title,markeddown)
    update_post.post_to_reddit()

def site_changes(siteaddress: str, title: str, browser: str):
    # set our static variables
    here = os.path.dirname(os.path.abspath(__file__))
    url = siteaddress
    log_file = os.path.join(here, title + "_monitoring_log.txt")
    updates_file = os.path.join(here, title + "_updates.txt")
    PreviousVersion_file = os.path.join(here, title + "_PreviousVersion.txt")
    compareVersion_file = os.path.join(here, title + "_compareVersion.txt")

    browser = browser.lower()
    if browser == "firefox":
        from firefox import get_soup
    elif browser == "chrome":
        from chrome import get_soup
    elif browser == "chromium":
        from chromium import get_soup

    # determin if this is the first run of the script for the given site.
    FirstRun = is_initial_run(PreviousVersion_file)
    if FirstRun:
        PrevVersion = ""
    else:
        PrevVersion = read_previous_version(PreviousVersion_file)
    # order some soup
    soup = get_soup(siteaddress)
    if soup[:5] == "Error":
        error_msg = (
            str(datetime.now())
            + " - Waiter! Waiter! There's a fly in my soup!\n"
            + soup
            + "\n"
        )
        write_to_log(log_file, error_msg)
        exit()  # if there is a fly in the soup we are leaving

    # compare the page text to the previous version

    #to clean up and remove embeded information we take the soup, encode it to UTF-8, write it to a file, read it back so we have strings, replace the timestamps with nothing, 
    #and then continue with our comparisons using the destamped version as a variable...this is probably terrible but it works...
    CurVersion =current_version(soup)
    Write_To_File(compareVersion_file, CurVersion)
    CurVersion = read_previous_version(compareVersion_file)
    CurVersion = re.sub(' data-aura-rendered-by="\d\d:\d\d\d;a"','',CurVersion)
   
    if PrevVersion != CurVersion:
        # on the first run - memorize the page only, no alerts
        if FirstRun == True:
            PrevVersion = CurVersion
            Write_To_File(PreviousVersion_file, CurVersion)
            start_message = str(datetime.now()) + " - Start Monitoring " + url
            write_to_log(log_file, start_message + "\n")
        else:
            change_message = str(datetime.now()) + " - Changes detected"
            write_to_log(log_file, change_message + "\n")
            OldPage = PrevVersion.splitlines()
            NewPage = CurVersion.splitlines()
            diff = difflib.context_diff(OldPage, NewPage, n=10)
            out_text = "\n".join(
                [ll.rstrip() for ll in "\n".join(diff).splitlines() if ll.strip()]
            )
            write_to_log(updates_file, out_text)
            write_to_log(log_file, str(datetime.now()) + " - " + "Update detected \n")
            #email_alert(out_text)
            fancy_email_alert(NewPage)
            send_to_reddit(CurVersion)
            Write_To_File(PreviousVersion_file, CurVersion)
    else:
        no_change_message = str(datetime.now()) + " - " + "No Changes \n"
        write_to_log(log_file, no_change_message)


def main(url, title: str, browser):
    site_changes(url, title, browser)


if __name__ == "__main__":
    main("https://support.sonos.com/s/article/3521?language=en_US", "s2", "chrome")
