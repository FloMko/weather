import yaml
from influxdb import InfluxDBClient

with open("creds.yml", 'r') as ymlfile:
    cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)
    host = cfg['influx']['host']
    user = cfg['influx']['user']
    password = cfg['influx']['password']
    dbname = cfg['influx']['db']
    port = cfg['influx']['port']

client = InfluxDBClient(host, port, user, password, dbname)
# client.create_database(dbname)
print(client.get_list_database())