import requests
from bs4 import BeautifulSoup
from datetime import date, datetime
import json
import pandas as pd
import requests
import smtplib
from smtplib import SMTP
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pretty_html_table import build_table
import time

###########################################################################################
## Enable Less Secure on the GMAIL Account which you will be using for sending notifications
## IF you dont know how to do that watch this -> https://www.youtube.com/watch?v=Ee7PDsbfOUI&ab_channel=wpguide
############################################################################################

EMAIL = 'techhuv@gmail.com'
PASSWORD = 'haurvi@133001'
RECEIVER_EMAIL = 'vishalbothra98@gmail.com'

###########################################################################################
### Append new addresses here
###########################################################################################

list_of_addresses = ['https://bscscan.com/token/0x27ae27110350b98d564b9a3eed31baebc82d878d',
'https://bscscan.com/token/0xd475c9c934dcd6d5f1cac530585aa5ba14185b92']

def send_mail(body):
    message = MIMEMultipart()
    message['Subject'] = 'Transaction Alert'
    message['From'] = EMAIL # sender email address
    message['To'] =  RECEIVER_EMAIL # receiver email address

    body_content = body
    message.attach(MIMEText(body_content, "html"))
    msg_body = message.as_string()

    server = SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(message['From'], PASSWORD)
    server.sendmail(message['From'], message['To'], msg_body)
    print("####################################")
    print('\n Alert! New Trnx Detected \n')
    print("####################################")
    server.quit()

def start_mail(b):

    # trnxhash = b[0].text
    # dnt = b[1].text
    # sender = b[3].text
    # receiver = b[5].text
    # qty = b[6].text

    df = pd.DataFrame([[b[0].text,b[1].text,b[3].text,b[5].text,b[6].text]],columns=['Trnx Hash','Date and Time','From','To','Qty'])
    output = build_table(df, 'blue_light')
    send_mail(output)
    print('Mail Sent')

def get_headers(url):
    headers = {
    'authority': 'bscscan.com',
    'cache-control': 'no-cache',
    'sec-ch-ua': '^\\^',
    'sec-ch-ua-mobile': '?0',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36',
    'accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'no-cors',
    'sec-fetch-user': '?1',
    'sec-fetch-dest': 'image',
    'accept-language': 'en-IN,en-GB;q=0.9,en-US;q=0.8,en;q=0.7',
    'cookie': 'ASP.NET_SessionId=vyjn24v5evunpe1t5j5wl0iy; __cflb=0H28vyb6xVveKGjdV3Nuszrk2HsjSpzzku4hLsMR6di; _ga=GA1.2.1373328447.1622557714; _gid=GA1.2.1256883113.1622557714; bscscan_cookieconsent=True; __cf_bm=12bddab25a628b6f799aacfa55defd70c28bbdc4-1622630494-1800-AQ+qGhQH87jOSwLt3Xu85GHW+xP0xVtW8z8yrAzFJwsylpJWWuuaBSlQbpBKn47a3OE8tPi1E84vHVIXSwFnMVPegufubCbkc+T5FGKp8GPKKumtseATCWFctVRNMJNDvg==',
    'Referer': url,
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36',
    'Origin': 'https://bscscan.com',
    'pragma': 'no-cache',
    'referer': url
    }
    return headers


new_address_list = []

sid = '33c025ece3347012ceb7a8270c11c388'

params = {}
prevhash = {}
for i in list_of_addresses:
    ca = i.rpartition('/')[-1]
    link = f'https://bscscan.com/token/generic-tokentxns2?m=normal&contractAddress={ca}&a=&sid={sid}&p=1'
    new_address_list.append(link)
    params[link] = ca
    prevhash[ca] = ''

print(" --------- Script Running ------- \n")

while True:
    
    for i in new_address_list:
        
        try:

            ca = params[i]
            print(f'Checking for Address -> {ca}')
            headers = get_headers(i)

            par = (
                ('m', 'normal'),
                ('contractAddress', ca),
                ('a', ''),
                ('sid', sid),
                ('p', '1'),
            )
        
            response = requests.get('https://bscscan.com/token/generic-tokentxns2', headers=headers, params=par)
            # print(response)
            html = response.text
            # print(html)

            soup = BeautifulSoup(html, 'html.parser')
            a = soup.find_all('tr')
            b = a[1].find_all('td')

            dnt = b[1].text
            dnt = datetime.strptime(dnt,'%Y-%m-%d %H:%M:%S')

            current_time = datetime.utcnow()
            # print(f'current_time : {current_time}')

            difference = current_time - dnt
            trnxhash = b[0].text

            if difference.total_seconds() < 30:
                if prevhash[ca] != trnxhash:
                    prevhash[ca] = trnxhash
                    start_mail(b)
        
        except:
            pass

    # time.sleep(10)
