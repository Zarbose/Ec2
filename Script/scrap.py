import requests
import subprocess
from bs4 import BeautifulSoup
from datetime import datetime
import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS
from influxdb_client.domain.write_precision import WritePrecision
from influxdb_client import InfluxDBClient, Point, WriteOptions
from influxdb_client import InfluxDBClient, WriteOptions
import pandas as pd

from prometheus_client import start_http_server, Summary
import random
import time


# pip install beautifulsoup4
# pip install influxdb-client
date = '21.02.2023'
url = 'https://transparency.entsoe.eu/transmission-domain/r2/dayAheadPrices/show?name=&defaultValue=false&viewType=TABLE&areaType=BZN&atch=false&dateTime.dateTime='+date+'+00:00|CET|DAY&biddingZone.values=CTY|10YFR-RTE------C!BZN|10YFR-RTE------C&resolution.values=PT60M&dateTime.timezone=CET_CEST&dateTime.timezone_input=CET+(UTC+1)+/+CEST+(UTC+2)'


class HtmlRequest:
    def __init__(self,url,date):
        self.date = date
        self.url = url
        self.result = []

    def getPage(self):
        response = requests.get(self.url)
        if response.status_code != 200:
            print("Error fetching page code "+str(response.status_code))
            exit(1)

        soup = BeautifulSoup(response.content, 'html.parser')
        listValues = soup.find_all(class_="data-view-detail-link")
        listHours = soup.find_all(class_="first")

        if (len(listValues) != len(listHours)):
            print("Error when reading the web page")
            exit(2)

        N=len(listValues)
        for i in range(N):
            self.result.append([listHours[i].text,listValues[i].text])

        for i in range(0,N):
            string = self.date+" "+str(i)+":0:0"
            string = datetime.strptime(string, '%d.%m.%Y %H:%M:%S').isoformat()
            datetime_object = datetime.strptime(string, '%Y-%m-%dT%H:%M:%S')
            ts=datetime.timestamp(datetime_object)
            self.result[i][0]=str(datetime_object)+".000000Z"

    def printResult(self):
        for i in range(len(self.result)):
            print(self.result[i][0],self.result[i][1])


# req = HtmlRequest(url,date)
# req.getPage()
# req.printResult()

class DataManager:
    def __init__(self):
        self.bucket="Test"
        self.org="Ec2"
        self.token="sdCawSGLxeLRVbaNsjdIMHspt7jdqvB6sVmRTzikxPeb9MxW_zDLoK7fk5qi4iWee2td9OSkp55RGeG6fARhFw=="
        self.url="http://localhost:8086"


    def dataToCSV(self):
        print("TODO")

    def sendData(self):
        # print("Send data")

        # with InfluxDBClient(url=self.url, token=self.token, org=self.org, debug=True) as _client:
        #     with _client.write_api(write_options=SYNCHRONOUS) as _write_client:
        #         p = Point("h2o_feet").tag("location", "coyote_creek").field("water_level", 4.0).time(1674658800,WritePrecision.S)
        #         _write_client.write(self.bucket, self.org, record=p)
        #         print("Sending : ",p.to_line_protocol())
    
        

        # exitCode = subprocess.call(["influx","write","-b","Test","-f","test_influxdb.csv"])


        # client = influxdb_client.InfluxDBClient(
        #     url=self.url,
        #     token=self.token,
        #     org=self.org,
        #     debug=True
        # )
        # write_api = client.write_api(write_options=SYNCHRONOUS)
        # p = influxdb_client.Point("h2o_feet").tag("location", "coyote_creek").field("water_level", 4.0).time(1674658800,WritePrecision.S)
        # write_api.write(bucket=self.bucket, org=self.org, record=p,write_precision=WritePrecision.S)
        # print("Sending : ",p.to_line_protocol())
        # write_api.close()
        # client.close()

        with InfluxDBClient(url=self.url, token=self.token, org=self.org) as client:
            for df in pd.read_csv("test2.csv", chunksize=1_000):
                with client.write_api() as write_api:
                    # try:
                    print(df)
                    write_api.write(
                        bucket="Test",
                        org="Ec2",
                        record=df,
                        data_frame_measurement_name="stocks",
                        data_frame_tag_columns=["symbol"],
                        # data_frame_timestamp_column="timestamp",
                    )
                    # except InfluxDBClientError as e:
                    #     print("Ici", e)
        

    def getData(self):
        print("TODO")

    def genBucket(self):
        print("TODO")

class CSVWriter:
    def __init__(self,path):
        self.path=path

    def addHeader(self):
        print("TODO")

    def writeData(self):
        print("TODO")



# dm = DataManager()
# dm.sendData()

#79yVmTjFqqYQj5bXDRmNYJfqghYsqqom73zvgXStjkw1WK7QgGr-7rAiHNEkORlBTQvV9nwL7mcB5IQTFKYbUw==


# exitCode = subprocess.call(["influx","write","-b","Test","-f","test_influxdb.csv"])

# write_api = client.write_api(write_options=SYNCHRONOUS) 

# point = Point("h2o_feet") \
#     .field("water_level", 10) \
#     .tag("location", "pacific") \

# print(f'Time serialized with nanosecond precision: {point.to_line_protocol()}')
# print()
# write_api.write(bucket="Test", record=point.to_line_protocol())

# p = influxdb_client.Point("my_measurement").tag("location", "Prague").field("temperature", 107.93)
# write_api.write(bucket=bucket, org=org, record=p)

