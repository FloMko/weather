import csv
import requests
from bs4 import BeautifulSoup as bs
import influx
import logging

logging.getLogger().setLevel(logging.DEBUG)


headers = {"accept": "*/*",
           "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36'}
#Начало парсинга со страницы арентдных квартир в Санкт-Петербурге


base_url = "http://www.infoeco.ru/index.php?id=2276"





def urls_pull(linklist = list):
    linklist = []
    urlsforears = ['http://www.infoeco.ru/index.php?id=2820', 'http://www.infoeco.ru/index.php?id=3122', 'http://www.infoeco.ru/index.php?id=4355', 'http://www.infoeco.ru/index.php?id=6532', 'http://www.infoeco.ru/index.php?id=8221']
    for url_year in urlsforears:
        for index in range(500):
            if index % 20 == 0 or index - 1 == 0:
                url = url_year + f'&start={index}'
                session = requests.Session()  # Эмуляция сессии
                request = session.get(url, headers=headers)
                if request.status_code == 200:
                    soup = bs(request.content, 'html.parser')
                    content = soup.find_all(attrs={'class': 'clearfix'})
                    for i in content:
                        partoflink = i.find('a').attrs['href']
                        link = "http://www.infoeco.ru/" + partoflink
                        linklist.append(link)
            else:
                pass

    return linklist

#Функция обхода страниц, начало с базового урла
def parse(base_url, headers):
    table_string =[]
    session = requests.Session() #Эмуляция сессии
    request = session.get(base_url, headers=headers)
    if request.status_code == 200:
        soup = bs(request.content, 'html.parser')
        table = soup.find("table").find_all("tr")
        rows = soup.find("table", border=1).find("tbody").find_all("tr")
        date = soup.find("table", border=1).find("td").get_text().strip().split(' ')[-1]
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
                    'url': base_url,
                    'index': rn,
                    'address': sr,
                    'pm10': d,
                    'pm2_5':n
                }
                influx.populate(data['date'],data['index'],data['url'], data['address'], data['pm10'], data['pm2_5'])
                print(data)
            except:
                pass


linklist = urls_pull()
for link in linklist:
    parse(link,headers)
    logging.debug(link)

#parse(base_url, headers)
