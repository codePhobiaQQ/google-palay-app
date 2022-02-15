from os import access
from google_play_scraper import app
import requests
from bs4 import BeautifulSoup
from openpyxl import load_workbook

# link = "https://play.google.com/store/search?q=asphalt&c=apps&hl=ru&gl=US"

print("Введите ссылку страницы:")
link = input()

headers = {
    'accept': '*/*',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'
}

# def parser_first():
response = requests.get(link, headers=headers)
src = response.text

#Получаем страницу 
soup = BeautifulSoup(src, "html.parser")

#Находим элемент с определенным классом
all_products = soup.find("div", class_="ZmHEEd").findAll("a")
all_apps_hrefs = []

for item in all_products:
    all_apps_hrefs.append(item.get("href"))
    
#Удаляем дублирующиеся ссылки
no_dublicat = set(all_apps_hrefs)

only_name = []
    
#Удаляем лишнее из ссылки
for item in no_dublicat:
    if (item[item.find("?id=") + 4:])[0:4] == "com.":
        only_name.append(item[item.find("?id=") + 4:])
    
#Печатаем айдишники
# for item in only_name:
#     print(item)
    

#Ссылка на приложение 
#Версия приложения
#Название приложения
#Ссылка на официальный сайт
#Количество установок 
#Разработчик приложения


fn = "example.xlsx"
wb = load_workbook(fn)
ws = wb['data']

ws.append(['title', 'installs', 'url', 'version', 'score', 'price', 'developerWebsite', 'developerEmail'])
ws.append(['', '', '', '', '', '', '', ''])


for item in only_name:
    result = app(
        item,
        lang='ru', # defaults to 'en'
        country='us' # defaults to 'us'
    )
    ws.append([f'{result["title"]}',
               f'{result["installs"]}',
               f'{result["url"]}',
               f'{result["version"]}',
               f'{result["score"]}',
               f'{result["price"]}',
               f'{result["developerWebsite"]}',
               f'{result["developerEmail"]}',
               ])
    
wb.save(fn)
wb.close()



# if __name__ == '__main__':
#     print("Result: ", parser_first())

