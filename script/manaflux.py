from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
from datetime import datetime
import os

url="http://influxdb:8086"
org="Ec2"
bucket="price"

token = os.environ['DOCKER_INFLUXDB_INIT_ADMIN_TOKEN']

def manaflux_send_daily_price(data):
    client = InfluxDBClient(url=url, token=token, org=org)
    write_api = client.write_api(write_options=SYNCHRONOUS)
    for i in range(len(data)):
        point = Point("cout_electricite").tag("location", "France").field("euros", float(data[i]["val"])).time(data[i]["time"], WritePrecision.NS)
        write_api.write(bucket=bucket, record=point)

if __name__ == "__main__":
    print("Cannot used as a script")