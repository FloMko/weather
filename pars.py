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
    table_string =[]
    session = requests.Session() #Эмуляция сессии
    request = session.get(base_url, headers=headers)
    if request.status_code == 200:
        soup = bs(request.content, 'html.parser')
        table = soup.find("table").find_all("tr")
        rows = soup.find("table", border=1).find("tbody").find_all("tr")
        date = soup.find("table", border=1).find("td").get_text().strip()
        for i in range(len(rows)):
            try:
                stringintable = table[i]
                for td in stringintable:
                    rn = stringintable.find_all("td")[0].get_text().strip()
                    sr = stringintable.find_all("td")[1].get_text().strip()
                    d = stringintable.find_all("td")[2].get_text().strip()
                    n = stringintable.find_all("td")[3].get_text().strip()

                data = {
                    'date': date,
                    'number': rn,
                    'adress': sr,
                    'PM10': d,
                    'PM25':n
                }
                print(data)
            except:
                pass


        #for i in range(len(table)):
        #    if table[i] != '' and table[i] != '\n':
                # table_string.append(table[i])
        #Stringtable = ''.join(table_string)
        #print(Stringtable)





parse(base_url, headers)
