import logging
import requests
from bs4 import BeautifulSoup as bs
import influx

logger = logging.getLogger()
handler = logging.StreamHandler()
formatter = logging.Formatter(
        '%(levelname)s %(module)s - %(funcName)s: %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.ERROR)
# logging.basicConfig(
#     level=logging.WARNING,
#     format='%(levelname)s %(module)s - %(funcName)s: %(message)s',
#     datefmt='%Y-%m-%d %H:%M:%S',
#     stream=sys.stderr
# )
logging = logging.getLogger(__name__)

headers = {"accept": "*/*",
           "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36'}


logging.error('test')


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
    rows = {}
    session = requests.Session()  # Эмуляция сессии
    request = session.get(link, headers=headers)
    if request.status_code == 200:
        try:
            soup = bs(request.content, 'html.parser')
            rows = soup.find("table", border=1).find_all("tr")
            date = soup.find("table", border=1).find("td").get_text().strip().split(' ')[-1]
            return rows, date
        except Exception as e:
            logging.error(f"{link} with error {e}")


def parse(rows, date, link):
        for row in rows:
            try:
                rn = row.find_all("td")[0].get_text().strip()
                sr = row.find_all("td")[1].get_text().strip()
                d = row.find_all("td")[2].get_text().strip()
                n = row.find_all("td")[3].get_text().strip()
                if d == 'менее 0,1' or d == '-*':
                    d = '0,05'
                if n == 'менее 0,1' or n == '-*':
                    n = '0,05'
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
                logging.error(f" main error {e} with {date} and link {link} and {row}")


linklist = urls_pull()
for link in linklist:
    try:
        rows, date = get_info(link, headers)
    except Exception as e:
        logging.error(f" main error {e}")
        date = None
    if date is not None:
        parse(rows, date, link)
    logging.debug(link)
influx.export_db()
