import asyncio
import aiohttp
import time
from bs4 import BeautifulSoup

websites = """https://bscscan.com/token/generic-tokentxns2?m=normal&contractAddress=0x27Ae27110350B98d564b9A3eeD31bAeBc82d878d&a=&sid=3e45aee683c8009a2306232676e2ddda&p=1
https://bscscan.com/token/generic-tokentxns2?m=normal&contractAddress=0x27Ae27110350B98d564b9A3eeD31bAeBc82d878d&a=&sid=3e45aee683c8009a2306232676e2ddda&p=1"""
# https://www.facebook.com
# https://www.baidu.com
# https://www.yahoo.com
# https://www.amazon.com
# https://www.wikipedia.org
# http://www.qq.com
# https://www.google.co.in
# https://www.twitter.com
# https://www.live.com
# http://www.taobao.com
# https://www.bing.com
# https://www.instagram.com
# http://www.weibo.com
# http://www.sina.com.cn
# https://www.linkedin.com
# http://www.yahoo.co.jp
# http://www.msn.com
# http://www.uol.com.br
# https://www.google.de
# http://www.yandex.ru
# http://www.hao123.com
# https://www.google.co.uk
# https://www.reddit.com
# https://www.ebay.com
# https://www.google.fr
# https://www.t.co
# http://www.tmall.com
# http://www.google.com.br
# https://www.360.cn
# http://www.sohu.com
# https://www.amazon.co.jp
# http://www.pinterest.com
# https://www.netflix.com
# http://www.google.it
# https://www.google.ru
# https://www.microsoft.com
# http://www.google.es
# https://www.wordpress.com
# http://www.gmw.cn
# https://www.tumblr.com
# http://www.paypal.com
# http://www.blogspot.com
# http://www.imgur.com
# https://www.stackoverflow.com
# https://www.aliexpress.com
# https://www.naver.com
# http://www.ok.ru
# https://www.apple.com
# http://www.github.com
# http://www.chinadaily.com.cn
# http://www.imdb.com
# https://www.google.co.kr
# http://www.fc2.com
# http://www.jd.com
# http://www.blogger.com
# http://www.163.com
# http://www.google.ca
# https://www.whatsapp.com
# https://www.amazon.in
# http://www.office.com
# http://www.tianya.cn
# http://www.google.co.id
# http://www.youku.com
# https://www.example.com
# http://www.craigslist.org
# https://www.amazon.de
# http://www.nicovideo.jp
# https://www.google.pl
# http://www.soso.com
# http://www.bilibili.com
# http://www.dropbox.com
# http://www.xinhuanet.com
# http://www.outbrain.com
# http://www.pixnet.net
# http://www.alibaba.com
# http://www.alipay.com
# http://www.chrome.com
# http://www.booking.com
# http://www.googleusercontent.com
# http://www.google.com.au
# http://www.popads.net
# http://www.cntv.cn
# http://www.zhihu.com
# https://www.amazon.co.uk
# http://www.diply.com
# http://www.coccoc.com
# https://www.cnn.com
# http://www.bbc.co.uk
# https://www.twitch.tv
# https://www.wikia.com
# http://www.google.co.th
# http://www.go.com
# https://www.google.com.ph
# http://www.doubleclick.net
# http://www.onet.pl
# http://www.googleadservices.com
# http://www.accuweather.com
# http://www.googleweblight.com
# http://www.answers.yahoo.com"""

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
    'Referer': 'https://bscscan.com/token/generic-tokentxns2?m=normal&contractAddress=0x27ae27110350b98d564b9a3eed31baebc82d878d&a=&sid=3e45aee683c8009a2306232676e2ddda&p=1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36',
    'Origin': 'https://bscscan.com',
    'pragma': 'no-cache',
    'referer': 'https://bscscan.com/token/generic-tokentxns2?m=normal&contractAddress=0x27ae27110350b98d564b9a3eed31baebc82d878d&a=&sid=3e45aee683c8009a2306232676e2ddda&p=1',
}

params = (
    ('m', 'normal'),
    ('contractAddress', '0x27ae27110350b98d564b9a3eed31baebc82d878d'),
    ('a', ''),
    ('sid', '3e45aee683c8009a2306232676e2ddda'),
    ('p', '1'),
)


async def get(url, session):
    try:
        async with session.get(url=url,headers=headers,params=params) as response:
            resp = await response.text()
            soup = BeautifulSoup(resp, 'html.parser')
            
            print(soup)
            # b = a[1].find_all('td')
            print("Successfully got url {} with resp of length {}.".format(url, len(resp)))
    except Exception as e:
        print("Unable to get url {} due to {}.".format(url, e.__class__))


async def main(urls):
    async with aiohttp.ClientSession() as session:
        ret = await asyncio.gather(*[get(url, session) for url in urls])
    # print("Finalized all. Return is a list of len {} outputs.".format(len(ret)))


urls = websites.split("\n")
import requests

print(urls)
r = requests.get(urls[0],headers=headers,params=params)

print(r)
start = time.time()
asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
asyncio.run(main(urls))
end = time.time()

print("Took {} seconds to pull {} websites.".format(end - start, len(urls)))