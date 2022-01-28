import asyncio
import aiohttp
import time
from bs4 import BeautifulSoup
class WebScraper(object):
    def __init__(self, urls):
        self.urls = urls
        # Global Place To Store The Data:
        self.all_data  = []
        self.master_dict = {}
        # Run The Scraper:
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        asyncio.run(self.main())

    async def fetch(self, session, url):
        try:
            async with session.get(url) as response:
                text = await response.text()
                return text, url
        except Exception as e:
            print(str(e))

    async def main(self):
        tasks = []
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

        async with aiohttp.ClientSession(headers=headers,params=params) as session:
            for url in self.urls:
                tasks.append(self.fetch(session, url))

            htmls = await asyncio.gather(*tasks)
            self.all_data.extend(htmls)

            # Storing the raw HTML data.
            for html in htmls:
                if html is not None:
                    url = html[1]
                    self.master_dict[url] = {'Raw Html': html[0]}
                else:
                    continue
# 1. Create a list of URLs for our scraper to get the data for:
urls = ['https://bscscan.com/token/generic-tokentxns2?m=normal&contractAddress=0x27Ae27110350B98d564b9A3eeD31bAeBc82d878d&a=&sid=33c025ece3347012ceb7a8270c11c388&p=1',
'https://bscscan.com/token/generic-tokentxns2?m=normal&contractAddress=0x27Ae27110350B98d564b9A3eeD31bAeBc82d878d&a=&sid=33c025ece3347012ceb7a8270c11c388&p=1',
'https://bscscan.com/token/generic-tokentxns2?m=normal&contractAddress=0x27Ae27110350B98d564b9A3eeD31bAeBc82d878d&a=&sid=33c025ece3347012ceb7a8270c11c388&p=1']

# 2. Create the scraper class instance, this will automatically create a new event loop within the __init__ method:
scraper = WebScraper(urls = urls)

# 3. Notice how we have a list length of 2:
len(scraper.all_data)