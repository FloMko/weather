import yaml
from influxdb import InfluxDBClient
import logging


with open("creds.yml", 'r') as ymlfile:
    cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)
    host = cfg['influx']['host']
    user = cfg['influx']['user']
    password = cfg['influx']['password']
    dbname = cfg['influx']['db']
    port = cfg['influx']['port']


client = InfluxDBClient(host, port, user, password, dbname)
# client.create_database(dbname)
logging.debug(client.get_list_database())
def populate(date: str, index: str, url: str, address: str, pm10: str, pm2_5: str):
    """
    send data to influxdb
    :return: result
    """
    json_body = [
        {
            "measurement": "weather",
            "tags" : {
                "id": index,
                "date": date.replace('.', '-') + 'T12:12:12.000Z'
            },
            "time": date.replace('.', '-') + 'T12:12:12.000Z',
            "fields": {
                "url": url,
                "address": address,
                "pm10": pm10,
                "pm2_5": pm2_5
            }
        }
    ]
    client.write_points(json_body)


def import_db():
    client = InfluxDBClient(host, port, user, password, dbname)
    select_clause = 'SELECT * FROM {}'.format('weather')
    df = pd.DataFrame(client.query(select_clause, chunked=True, chunk_size=10000).get_points())
    df.to_csv('dummy.csv', encoding='utf-16', columns=['id', 'address', 'pm10','pm2_5', 'time'])


# import_db()
