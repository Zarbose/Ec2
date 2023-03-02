import requests
from bs4 import BeautifulSoup
from datetime import datetime
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

date = datetime.today().strftime('%d.%m.%Y')
url = 'https://transparency.entsoe.eu/transmission-domain/r2/dayAheadPrices/show?name=&defaultValue=false&viewType=TABLE&areaType=BZN&atch=false&dateTime.dateTime='+date+'+00:00|CET|DAY&biddingZone.values=CTY|10YFR-RTE------C!BZN|10YFR-RTE------C&resolution.values=PT60M&dateTime.timezone=CET_CEST&dateTime.timezone_input=CET+(UTC+1)+/+CEST+(UTC+2)'

class DataManager:
    def __init__(self,data):
        self.url="http://localhost:8086"
        self.org="Ec2"
        self.bucket="daily-price"
        self.token="sdCawSGLxeLRVbaNsjdIMHspt7jdqvB6sVmRTzikxPeb9MxW_zDLoK7fk5qi4iWee2td9OSkp55RGeG6fARhFw=="
        self.data=data

    def sendData(self):
        client = InfluxDBClient(url="http://localhost:8086", token=self.token, org=self.org)
        write_api = client.write_api(write_options=SYNCHRONOUS)
        for i in range(len(self.data)):
            # print(type(self.data[i][0]),type(float(self.data[i][1])))
            point = Point("cout-electricite").tag("location", "France").field("euros", float(self.data[i][1])).time(self.data[i][0], WritePrecision.NS)
            write_api.write(bucket=self.bucket, record=point)

    def getData(self):
        print("TODO")

class HtmlRequest:
    def __init__(self,url):
        self.url = url
        self.result = []
        self.dm = DataManager(self.result)

    def getPage(self):
        response = requests.get(self.url)
        if response.status_code != 200:
            print("Error fetching page code "+str(response.status_code))
            exit(1)

        soup = BeautifulSoup(response.content, 'html.parser')
        listValues = soup.find_all(class_="data-view-detail-link")

        if (len(listValues) != 24):
            print("Error when reading the web page")
            exit(2)

        N=len(listValues)
        curent_day = datetime.today().strftime('%Y-%m-%d')
        for i in range(N):
            if i<10:
                time=curent_day+"T0"+str(i)+":00:00Z"
            else:
                time=curent_day+"T"+str(i)+":00:00Z"
            self.result.append([time,listValues[i].text])

        self.dm.sendData()

    def __repr__(self):
        return "{0}".format(self.result)

    def __str__(self):
        to_print=""
        for i in range(len(self.result)):
            to_print+=str(self.result[i][0])+" "+str(self.result[i][1])+"\n"

        return to_print

req = HtmlRequest(url)
req.getPage()
# print(req)

#79yVmTjFqqYQj5bXDRmNYJfqghYsqqom73zvgXStjkw1WK7QgGr-7rAiHNEkORlBTQvV9nwL7mcB5IQTFKYbUw==