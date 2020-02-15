import csv
import requests
from bs4 import BeautifulSoup as bs

headers = {"accept": "*/*",
           "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36'}
#Начало парсинга со страницы арентдных квартир в Санкт-Петербурге
base_url = "http://www.infoeco.ru/index.php?id=2276"

def url_pull():
    pass


#Функция обхода страниц, начало с базового урла
def parse(base_url, headers):
    session = requests.Session() #Эмуляция сессии
    request = session.get(base_url, headers=headers)
    if request.status_code == 200:
        soup = bs(request.content, 'html.parser')
        table = soup.find("table").text
        print(table)
        while '\t' in table:




parse(base_url, headers)
