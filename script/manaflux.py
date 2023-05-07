from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

url="http://influxdb:8086"
org="Ec2"
bucket="price"
token="c5gyOEb7KSRLIoFuFrFDMUo9UDgmAlSMty9GJJZEMN3X5qfn6mkgVRCSxXottjfG8BZduRNOLivEql4FCngFjQ=="

#      c5gyOEb7KSRLIoFuFrFDMUo9UDgmAlSMty9GJJZEMN3X5qfn6mkgVRCSxXottjfG8BZduRNOLivEql4FCngFjQ==


def sendDailyPrice(data):
    client = InfluxDBClient(url=url, token=token, org=org)
    write_api = client.write_api(write_options=SYNCHRONOUS)
    for i in range(len(data)):
        point = Point("cout-electricite").tag("location", "France").field("euros", float(data[i]["val"])).time(data[i]["time"], WritePrecision.NS)
        write_api.write(bucket=bucket, record=point)

def getDailyPrice():
    client = InfluxDBClient(url=url, token=token, org=org)
    query_api = client.query_api()

    query = 'import "date"\
    from(bucket:"price")\
    |> range(start: today(), stop: date.add(d: 24h, to: today()))\
    |> filter(fn:(r) => r["_measurement"] == "cout-electricite")\
    |> filter(fn:(r) => r["location"] == "France")\
    |> filter(fn:(r) => r["_field"] == "euros")'

    result = query_api.query(org=org, query=query)
    results = []
    for table in result:
        for record in table.records:
            results.append((record.get_field(), float(record.get_value())))
    return results

def sendOptiTime(data):

    # segments=data["segments"]
    # end=data["end"]

    # client = InfluxDBClient(url=url, token=token, org=org)
    # write_api = client.write_api(write_options=SYNCHRONOUS)
    # for i in range(len(data)):
    #     point = Point("cout-electricite").tag("location", "France").field("euros", float(data[i]["val"])).time(data[i]["time"], WritePrecision.NS)
    #     write_api.write(bucket=bucket, record=point)

    return 1

if __name__ == "__main__":
    print("Cannot used as a script")