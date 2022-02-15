from os import access
from google_play_scraper import app
import requests
from bs4 import BeautifulSoup

link = "https://play.google.com/store/search?q=aliexpress&c=apps&hl=ru&gl=US"
headers = {
    'accept': '*/*',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'
}

# def parser_first():
response = requests.get(link, headers=headers)
src = response.text
# print(src)



# with open("index1.html", "w") as file: 
#     file.read(src)
    
soup = BeautifulSoup(src, "lxml")

all_products = soup.findAll(class_="ZmHEEd")

for item in all_products:
    print(item)

    # soup = BeautifulSoup(response.content, 'html.parser')
    # data = soup.find('div', {'class': 'wXUyZd'}).text
    # return data

# result = app(
#     'com.MagnoliaArt.HachiRoku',
#     lang='en', # defaults to 'en'
#     country='us' # defaults to 'us'
# )

# print(result)

# if __name__ == '__main__':
#     print("Result: ", parser_first())

