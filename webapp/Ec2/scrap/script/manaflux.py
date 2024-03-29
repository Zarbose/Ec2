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

def manaflux_send_opti(data):
    client = InfluxDBClient(url=url, token=token, org=org)
    write_api = client.write_api(write_options=SYNCHRONOUS)
    for elm in data:
        point = Point("resultat_otpi").tag("location", "France").field("statut_charge", float(elm["val"])).time(elm["time"], WritePrecision.NS)
        write_api.write(bucket=bucket, record=point)

def manaflux_send_total_price(data):
    date = datetime.today().strftime('%Y-%m-%d')
    date = date+"T01:00:00Z"

    client = InfluxDBClient(url=url, token=token, org=org)
    write_api = client.write_api(write_options=SYNCHRONOUS)
    point = Point("resultat_otpi").tag("location", "France").field("prix_total", float(data)).time(date, WritePrecision.NS)
    write_api.write(bucket=bucket, record=point)

def manaflux_send_total_duration(data):
    date = datetime.today().strftime('%Y-%m-%d')
    date = date+"T01:00:00Z"

    client = InfluxDBClient(url=url, token=token, org=org)
    write_api = client.write_api(write_options=SYNCHRONOUS)
    point = Point("resultat_otpi").tag("location", "France").field("duration_total", float(data)).time(date, WritePrecision.NS)
    write_api.write(bucket=bucket, record=point)

def manaflux_send_rendement(data):
    date = datetime.today().strftime('%Y-%m-%d')
    date = date+"T01:00:00Z"

    client = InfluxDBClient(url=url, token=token, org=org)
    write_api = client.write_api(write_options=SYNCHRONOUS)
    point = Point("resultat_otpi").tag("location", "France").field("rendement", float(data)).time(date, WritePrecision.NS)
    write_api.write(bucket=bucket, record=point)

def manaflux_reset():
    client = InfluxDBClient(url=url, token=token)

    delete_api = client.delete_api()

    """
    Delete Data
    """
    start = "2021-01-01T00:00:00Z"
    stop = "2024-02-01T00:00:00Z"
    delete_api.delete(start, stop, '_measurement=resultat_otpi', bucket=bucket, org=org)

    """
    Close client
    """
    client.close()

def manaflux_get_daily_price():
    client = InfluxDBClient(url=url, token=token, org=org)
    query_api = client.query_api()

    query = 'import "date"\
    from(bucket:"price")\
    |> range(start: today(), stop: date.add(d: 24h, to: today()))\
    |> filter(fn:(r) => r._measurement == "cout_electricite")\
    |> filter(fn:(r) => r.location == "France")\
    |> filter(fn:(r) => r._field == "euros")'

    result = query_api.query(org=org, query=query)
    results = []
    for table in result:
        for record in table.records:
            results.append({'time':record.get_time().strftime('%Y-%m-%dT%H:%M:%SZ') , 'val': record.get_value()})
    return results

if __name__ == "__main__":
    print("Cannot used as a script")