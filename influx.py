import yaml
from influxdb import InfluxDBClient
import logging

logging.getLogger().setLevel(logging.DEBUG)

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
            "fields": {
                "date": date,
                "id": index,
                "url": url,
                "address": address,
                "pm10": pm10,
                "pm2_5": pm2_5
            }
        }
    ]
    client.write_points(json_body)
