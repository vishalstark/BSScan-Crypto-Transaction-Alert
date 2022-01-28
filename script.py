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


# r = requests.get('https://bscscan.com/token/generic-tokentxns2?m=normal&contractAddress=0x27ae27110350b98d564b9a3eed31baebc82d878d&a=&sid=33c025ece3347012ceb7a8270c11c388&p=1')

import requests

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
    'Referer': 'https://bscscan.com/token/generic-tokentxns2?m=normal&contractAddress=0x27ae27110350b98d564b9a3eed31baebc82d878d&a=&sid=33c025ece3347012ceb7a8270c11c388&p=1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36',
    'Origin': 'https://bscscan.com',
    'pragma': 'no-cache',
    'referer': 'https://bscscan.com/token/generic-tokentxns2?m=normal&contractAddress=0x27ae27110350b98d564b9a3eed31baebc82d878d&a=&sid=33c025ece3347012ceb7a8270c11c388&p=1',
}

params = (
    ('m', 'normal'),
    ('contractAddress', '0x27ae27110350b98d564b9a3eed31baebc82d878d'),
    ('a', ''),
    ('sid', '33c025ece3347012ceb7a8270c11c388'),
    ('p', '1'),
)

prevhash = ''

def send_mail(body):
    message = MIMEMultipart()
    message['Subject'] = 'Transaction Alert'
    message['From'] = 'techhuv@gmail.com'
    message['To'] = 'vishalbothra98@gmail.com'

    body_content = body
    message.attach(MIMEText(body_content, "html"))
    msg_body = message.as_string()

    server = SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(message['From'], "haurvi@133001")
    server.sendmail(message['From'], message['To'], msg_body)
    print("####################################")
    print('\n Alert! New Trnx Detected \n')
    print("####################################")
    server.quit()

def start_mail(b):

    global prevhash
    sender = b[3].text
    receiver = b[5].text
    qty = b[6].text

    prevhash = trnxhash

    df = pd.DataFrame([[trnxhash,dnt,sender,receiver,qty]],columns=['Trnx Hash','Date and Time','From','To','Qty'])
    output = build_table(df, 'blue_light')
    send_mail(output)
    print('Mail Sent')

print(" --------- Script Running -------")
while True:
    
    # try:
    
    response = requests.get('https://bscscan.com/token/generic-tokentxns2', headers=headers, params=params)

    html = response.text

    soup = BeautifulSoup(html, 'html.parser')
    a = soup.find_all('tr')

    b = a[1].find_all('td')
    
    # print(b)
    dnt = b[1].text
    dnt = datetime.strptime(dnt,'%Y-%m-%d %H:%M:%S')

    current_time = datetime.utcnow()
    # print(f'current_time : {current_time}')

    difference = current_time - dnt
    trnxhash = b[0].text

    if difference.total_seconds() < 30:
        if prevhash != trnxhash:
            start_mail(b)
            
            
    # except:
    #     print('Failed to fetch data')

    time.sleep(10)
