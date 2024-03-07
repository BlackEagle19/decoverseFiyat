import requests
from bs4 import BeautifulSoup
import pandas as pd
from telegram import Bot
from telegram import InputFile
import telegram.ext
import asyncio

async def send_excel_file(excel_file_path, bot_token, chat_id):
    # Bot'u başlat
    bot = Bot(token=bot_token)

    # Excel dosyasını gönder
    with open(excel_file_path, 'rb') as file:
        await bot.send_document(chat_id=chat_id, document=file)

# Bot token'ınızı ve hedef chat ID'nizi girin
BOT_TOKEN = '6994284905:AAHhU7PleaVU3eSlMFt_qt3imu_KWHmya0c'
CHAT_ID = '-4157001586'  # Kanal için "@channelusername" şeklinde de kullanılabilir



ürünler=[]
payload = {}
headers = {
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:76.0) Gecko/20100101 Firefox/76.0 SEB',
  'Accept': 'application/json, text/plain, */*',
  'Accept-Language': 'tr-TR,tr;q=0.8,en-US;q=0.5,en;q=0.3',
  'Accept-Encoding': 'gzip, deflate, br',
  'X-CSRFToken': 'H4x9jMmJpCo7hek4UVxp6VRPS7YYRZlQJqoLditYBgEf0OSJgXzcndMf0tQu3jOV',
  'Connection': 'keep-alive',
  'Referer': 'https://www.decoverse.com/list/',
  'Cookie': 'sessionid=riz0k63e4pvkbpsmqahj4piiyzdb0bw0; _gcl_au=1.1.2143641648.1709825686; _ga_S0LXHRVJJV=GS1.1.1709825686.1.1.1709825797.9.0.0; _ga=GA1.2.960081304.1709825687; __rtbh.lid=^%^7B^%^22eventType^%^22^%^3A^%^22lid^%^22^%^2C^%^22id^%^22^%^3A^%^22NSbMMjfFAqd1xbloq5x1^%^22^%^7D; _gid=GA1.2.1923559234.1709825689; _fbp=fb.1.1709825690106.718346288; _ym_uid=1709825690945635067; _ym_d=1709825690; _hjSessionUser_3269857=eyJpZCI6ImExNTUwYWEyLWI3OTItNTk2MS1iZDNiLWU2MmM1YTE4NWFjNCIsImNyZWF0ZWQiOjE3MDk4MjU2OTAzMjYsImV4aXN0aW5nIjp0cnVlfQ==; _hjSession_3269857=eyJpZCI6IjQ5YTM0YjEyLWFmMGMtNGE5OC05ZWJlLWZhODlhOGJmNmYwZiIsImMiOjE3MDk4MjU2OTAzMjYsInMiOjEsInIiOjEsInNiIjowLCJzciI6MCwic2UiOjAsImZzIjoxLCJzcCI6MH0=; _tt_enable_cookie=1; _ttp=bJQNXMehYDs0xQLMRPAXz8fyTaQ; _ym_isad=2; cto_bundle=fuAzQ19LWVhzWDN6bG9uT09lTyUyQmdJTktoSUlhbzZhZXpiVzRNSkx0YkJSQ05wNm41YU5iSmpFdnp2Z0pCYnR4JTJGbXUwN2FoOE03NU1nU3IyandPUnF3N292JTJCVEY4b0hZOW5ma2Rnc3VSSEYzTjVYaElKZVhkWU9PSCUyQnR6RnNMcSUyQmdCdGtla1hyaHBZZWNnMExuOUdEd3cxcSUyRlElM0QlM0Q; __rtbh.uid=^%^7B^%^22eventType^%^22^%^3A^%^22uid^%^22^%^2C^%^22id^%^22^%^3A^%^22undefined^%^22^%^7D; _gat=1; _dc_gtm_UA-238361835-1=1; _uetsid=3bf1c400dc9811eeae4413c8bc9c2c54; _uetvid=3bf1eed0dc9811eeb6a9271a1b31a1f1',
  'Sec-Fetch-Dest': 'empty',
  'Sec-Fetch-Mode': 'cors',
  'Sec-Fetch-Site': 'same-origin',
  'TE': 'trailers'
}

i = 1
while True:

    
    url = f"https://www.decoverse.com/list/?page={i}"

    print(url)

    response = requests.request("GET", url, headers=headers)

    if response.status_code != 200:
        print(response.text)
        break
    
    data = response.json()
    for ürün in data['products']:
        name=ürün['name']
        sku=ürün['sku']
        price = ürün['price']
        ürün={
            "İSİM":name,
            "SKU":sku,
            "PRİCE":price
        }

        ürünler.append(ürün)

    i+=1

df=pd.Dataframe(ürünler)
df.to_excel("decoverse_fiyatlar.xlsx", index=False)

# Göndermek istediğiniz Excel dosyasının yolu
EXCEL_FILE_PATH = 'decoverse_fiyatlar.xlsx'

# Fonksiyonu çağır
asyncio.run(send_excel_file(EXCEL_FILE_PATH, BOT_TOKEN, CHAT_ID))