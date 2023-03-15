from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
from influxdb_client.client.exceptions import InfluxDBError
import requests

url="http://localhost:8086"
org="Ec2"
bucket="daily-price"
token="sdCawSGLxeLRVbaNsjdIMHspt7jdqvB6sVmRTzikxPeb9MxW_zDLoK7fk5qi4iWee2td9OSkp55RGeG6fARhFw=="

#      79yVmTjFqqYQj5bXDRmNYJfqghYsqqom73zvgXStjkw1WK7QgGr-7rAiHNEkORlBTQvV9nwL7mcB5IQTFKYbUw==


def sendDailyPrice(data):
    client = InfluxDBClient(url=url, token=token, org=org)
    write_api = client.write_api(write_options=SYNCHRONOUS)
    for i in range(len(data)):
        point = Point("cout-electricite").tag("location", "France").field("euros", float(data[i][1])).time(data[i][0], WritePrecision.NS)
        write_api.write(bucket=bucket, record=point)

def getDailyPrice():
    client = InfluxDBClient(url=url, token=token, org=org)
    query_api = client.query_api()

    query = 'import "date"\
    from(bucket:"daily-price")\
    |> range(start: today(), stop: date.add(d: 24h, to: today()))\
    |> filter(fn:(r) => r["_measurement"] == "cout-electricite")\
    |> filter(fn:(r) => r["location"] == "France")\
    |> filter(fn:(r) => r["_field"] == "euros")'

    result = query_api.query(org=org, query=query)
    results = []
    for table in result:
        for record in table.records:
            results.append((record.get_field(), record.get_value()))
    return results

if __name__ == "__main__":
    print("Cannot used as a script")