import yaml
from influxdb import InfluxDBClient
from influxdb import DataFrameClient
import logging
import pandas as pd


with open("creds.yml", 'r') as ymlfile:
    cfg = yaml.safe_load(ymlfile)
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
    Send data to influxdb
    :return: result
    """
    json_body = [
        {
            "measurement": "weather",
            "tags": {
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
    measurement = "weather"
    select_clause = f"SELECT * FROM {measurement}"
    df = pd.DataFrame(client.query(select_clause, chunked=True, chunk_size=20010).get_points())
    df.to_csv('notebook/dummy.csv', encoding='utf-16', columns=['id', 'pm10', 'pm2_5', 'time'])
    df = df.set_index('time')
    new_df = format_df(df)
    new_df.to_csv('notebook/formatted.csv', encoding='utf-16')


def format_df(df):
    new_df = pd.DataFrame()
    for key in df['id'].unique():
        new_df[f"id={key}, pm=2_5"] = df.loc[df['id'] == f"{key}"]['pm2_5']
        new_df[f"id={key}, pm=10"] = df.loc[df['id'] == f"{key}"]['pm10']
    return new_df

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
