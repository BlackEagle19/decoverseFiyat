import requests
from bs4 import BeautifulSoup
import pandas as pd
from telegram import Bot
from telegram import InputFile
import telegram.ext
import asyncio, json

async def send_message(bot_token, chat_id, message):
    bot = Bot(token=bot_token)
    await bot.send_message(chat_id=chat_id, text=message)


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
  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
  'Accept-Language': 'tr-TR,tr;q=0.8,en-US;q=0.5,en;q=0.3',
  'Accept-Encoding': 'gzip, deflate, br',
  'Referer': 'https://www.decoverse.com/artema-samba-a45680sta-3f-surgulu-el-dusu-takimi-krom/',
  'Connection': 'keep-alive',
  'Cookie': 'sessionid=9xhcxzsz4il2mhvhe2l06lla3btbwso0; _gcl_au=1.1.1276435215.1709836544; _ga_S0LXHRVJJV=GS1.1.1709836544.1.1.1709836594.10.0.0; _ga=GA1.2.1706590656.1709836544; __rtbh.uid=^%^7B^%^22eventType^%^22^%^3A^%^22uid^%^22^%^2C^%^22id^%^22^%^3A^%^22undefined^%^22^%^7D; __rtbh.lid=^%^7B^%^22eventType^%^22^%^3A^%^22lid^%^22^%^2C^%^22id^%^22^%^3A^%^22Qi8JiZhLZk86sPaU6jL2^%^22^%^7D; _gid=GA1.2.534741044.1709836547; _fbp=fb.1.1709836547554.633095752; _ym_uid=1709836548520708137; _ym_d=1709836548; _tt_enable_cookie=1; _ttp=fyNA6_ov3VXxWXQVr3WRck7t1Zo; _ym_isad=2; _hjSessionUser_3269857=eyJpZCI6ImQ3NGZhNzczLWNkNTItNTAwNS1iMTRjLWFjZDNiNzNlNWVhYSIsImNyZWF0ZWQiOjE3MDk4MzY1NDk0NjksImV4aXN0aW5nIjp0cnVlfQ==; _hjSession_3269857=eyJpZCI6IjNhZjU4OGI0LWEwMWMtNGFhNS05MTYzLWI3YTQyY2E2MGI4ZiIsImMiOjE3MDk4MzY1NDk0NzAsInMiOjEsInIiOjEsInNiIjowLCJzciI6MCwic2UiOjAsImZzIjoxLCJzcCI6MH0=; cto_bundle=9afiiF9aVkVCamlpWmtkS2labldFMDFINTNuWFhOdWpzYjAlMkJHeWFGeHNWRktxVWxydE1ESG52V0NtN0glMkJYMWlrMkJ3TmNJazJKc08wdCUyQlVieGNlbWNGemlWU2dXTjlQJTJCcUZ3WlFPJTJGblE2bmpjbjhhQnJ5aFd3VzNTMzVuNjl5TDZrRUQ5OGVtYXNNcFVHbVJkQ0RVenpYNklRJTNEJTNE; _uetsid=839d68a0dcb111ee9ec2071df89e6b38; _uetvid=839d8b10dcb111ee9d98ad5bcaa80a53; sessionid=9xhcxzsz4il2mhvhe2l06lla3btbwso0',
  'Upgrade-Insecure-Requests': '1',
  'Sec-Fetch-Dest': 'document',
  'Sec-Fetch-Mode': 'navigate',
  'Sec-Fetch-Site': 'same-origin',
  'Pragma': 'no-cache',
  'Cache-Control': 'no-cache'
}


df_kodlar = pd.read_excel('listesiDeco.xlsx')['KOD'].to_list()


for kod in df_kodlar:
    try:
        url = f"https://www.decoverse.com/list/?search_text={kod}"
        print(url)
        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            asyncio.run(send_message(BOT_TOKEN, CHAT_ID, f"Error {response.status_code} for URL: {url}"))
            continue
        
        soup = BeautifulSoup(response.content, 'html.parser')
        dataaa = soup.find_all('div', class_="analytics-data")
        for data in dataaa:
            data_text = data.text

            if 'productListViewed' in data_text:
                json_data = json.loads(data_text)

                for item in json_data['payload']:
                    ürün = {
                        "İSİM": item['name'],
                        "SKU": kod,
                        "PRİCE": item['price']
                    }
                    ürünler.append(ürün)
                break
    except Exception as e:
        asyncio.run(send_message(BOT_TOKEN, CHAT_ID, f"Exception occurred: {str(e)}"))
        continue


df=pd.DataFrame(ürünler)
df.to_excel("decoverse_fiyatlar.xlsx", index=False)

# Göndermek istediğiniz Excel dosyasının yolu
EXCEL_FILE_PATH = 'decoverse_fiyatlar.xlsx'

# Fonksiyonu çağır
asyncio.run(send_excel_file(EXCEL_FILE_PATH, BOT_TOKEN, CHAT_ID))