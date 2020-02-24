import logging
import logging.config
import requests
from bs4 import BeautifulSoup as bs
import influx
import yaml

# Onboard logging
with open("log.conf.yml", 'r') as ymlfile:
    cfg = yaml.safe_load(ymlfile)
    logging.config.dictConfig(cfg)


headers = {"accept": "*/*",
           "User-Agent": 'bot that watch for big brother'}


def urls_pull():
    linklist = []
    urlsforears = ['http://www.infoeco.ru/index.php?id=2820', 'http://www.infoeco.ru/index.php?id=3259',
                   'http://www.infoeco.ru/index.php?id=4352', 'http://www.infoeco.ru/index.php?id=6529',
                   'http://www.infoeco.ru/index.php?id=8209']
    urlsforears.sort(reverse=True)
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


# Функция обхода страниц, начало с базового урла
def get_info(link, headers):
    session = requests.Session()  # Эмуляция сессии
    request = session.get(link, headers=headers)
    if request.status_code == 200:
        try:
            soup = bs(request.content, 'html.parser')
            rows = soup.find("table", border=1).find_all("tr")
            date = soup.find("table", border=1).find("td").get_text().strip().split(' ')[-1]
            return rows, date
        except Exception as e:
            logging.warning(f"{link} with error {e}")


def check_value(value: str):
    """
    Convert str value to float
    :param value: str
    :return: float
    """
    if value in ['менее 0,1', 'Mенее 0,1']:
        return 0.05
    try:
        return float(value.replace(',', '.'))
    except ValueError:
        return None


def parse(rows, date, link):
    for row in rows:
        try:
            rn = row.find_all("td")[0].get_text().strip()
            sr = row.find_all("td")[1].get_text().strip()
            d = row.find_all("td")[2].get_text().strip()
            n = row.find_all("td")[3].get_text().strip()
            d = check_value(d)
            n = check_value(n)
            data = {
                    'date': date,
                    'url': link.strip(),
                    'index': rn,
                    'address': sr,
                    'pm10': d,
                    'pm2_5': n
            }
            logging.warning(data)
            influx.populate(data['date'], data['index'], data['url'], data['address'], data['pm10'],
                            data['pm2_5'])
        except Exception as e:
            logging.warning(f" main error {e} with {date} and link {link} and {row}")


linklist = urls_pull()
for link in linklist:
    try:
        rows, date = get_info(link, headers)
    except Exception as e:
        logging.error(f" main error {e}")
        date = None
    if date is not None:
        parse(rows, date, link)
influx.export_db()
