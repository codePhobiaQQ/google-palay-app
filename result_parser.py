from os import access
from google_play_scraper import app
import requests
from bs4 import BeautifulSoup
from openpyxl import load_workbook
from selenium import webdriver
import time


f = open("./links.txt", "r")
links = []
for item in f:
    links.append(item)
f.close()


SCROLL_PAUSE_TIME = 1.5

#options
options = webdriver.ChromeOptions()
options.add_argument("'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36")
options.add_argument("'accept': '*/*'")

url = "https://play.google.com/store/search?q=asphalt&c=apps&hl=ru&gl=US"

driver = webdriver.Chrome(
    executable_path="/Users/helloworld/Documents/bots/google-palay-app/chrome/chromedriver",
    options=options,
)

only_name = []

try: 
    for linking in links:
        driver.get(url=linking)
        last_height = driver.execute_script("return document.body.scrollHeight")

        while True:
            # Scroll down to bottom
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            
            # Wait to load page
            time.sleep(SCROLL_PAUSE_TIME)
            
            # Calculate new scroll height and compare with last scroll height
            new_height = driver.execute_script("return document.body.scrollHeight")
            
            if new_height == last_height:
                
                
                html_source = driver.page_source    
                #Получаем страницу 
                soup = BeautifulSoup(html_source, "html.parser")
                all_products = []

                all_products_wrapper = soup.findAll("div", class_="ZmHEEd")

                for item in all_products_wrapper:
                    ptr = item.findAll("a")
                    for ptr_item in ptr: 
                        all_products.append(ptr_item)    

                all_apps_hrefs = []

                for item in all_products:
                    all_apps_hrefs.append(item.get("href"))
                    
                #Удаляем дублирующиеся ссылки
                no_dublicat = set(all_apps_hrefs)
                    
                #Удаляем лишнее из ссылки
                for item in no_dublicat:
                    if (item[item.find("?id=") + 4:])[0:4] == "com.":
                        only_name.append(item[item.find("?id=") + 4:])
                            
                
                # driver.close()
                # driver.quit()   
                break
            
            last_height = new_height
        
except Exception as ex:
    print(ex)
finally:
    driver.close()
    driver.quit() 
    
fn = "result.xlsx"
wb = load_workbook(fn)
ws = wb['data']

ws.append(['title', 'installs', 'url', 'version', 'score', 'price', 'developerWebsite', 'developerEmail'])
ws.append(['', '', '', '', '', '', '', ''])


for item in only_name:
    try:
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
    except Exception as ex:
        pass
    
wb.close()   