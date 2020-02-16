import yaml
from influxdb import InfluxDBClient
from influxdb import DataFrameClient
import logging
import pandas as pd


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
            },
            "time": date.replace('.', '-') + 'T12:12:12.000Z',
            "fields": {
                "url": url,
                "pm10": pm10,
                "pm2_5": pm2_5
            }
        }
    ]
    client.write_points(json_body)


def export_db():
    client = InfluxDBClient(host, port, user, password, dbname)
    select_clause = 'SELECT * FROM {}'.format('weather')
    df = pd.DataFrame(client.query(select_clause, chunked=True, chunk_size=20010).get_points())
    df.to_csv('dummy.csv', encoding='utf-16', columns=['id','pm10','pm2_5', 'time'])


def import_db():
    df = pd.read_csv('monit-pnts.csv', sep=';')
    date = []
    for i in range(df.count()[0]):
        date.append(1483013532000000000 + int(str(i) + '000000000'))
    df = df.assign(Date=date)
    # protocol = 'line'

    df['Datetime'] = pd.to_datetime(df['Date'])
    df = df.set_index('Datetime')
    df = df.drop(['Date'], axis=1)
    client_pandas = DataFrameClient(host, port, user, password, dbname)
    client_pandas.write_points(df, 'stations')


export_db()
# import_db()
