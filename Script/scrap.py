import requests
import subprocess
import csv
from bs4 import BeautifulSoup
from datetime import datetime

date = datetime.today().strftime('%d.%m.%Y')
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
            datetime_object = datetime.strptime(string, '%Y-%m-%dT%H:%M:%S%f')
            self.result[i][0]=(str(datetime_object)+".000000000Z").replace(" ","T")

    def __repr__(self):
        return "{0}".format(self.result)

    def __str__(self):
        to_print=""
        for i in range(len(self.result)):
            to_print+=str(self.result[i][0])+" "+str(self.result[i][1])+"\n"

        return to_print


# req = HtmlRequest(url,date)
# req.getPage()
# print(req)

class DataManager:
    def __init__(self):
        self.bucket="Test"
        self.org="Ec2"
        self.token="sdCawSGLxeLRVbaNsjdIMHspt7jdqvB6sVmRTzikxPeb9MxW_zDLoK7fk5qi4iWee2td9OSkp55RGeG6fARhFw=="
        self.url_local="http://localhost:8086"
        self.url_distant="http://localhost:8086"


    def dataToCSV(self):
        print("TODO")

    def sendData(self):
        exitCode = subprocess.call(["influx","write","--host",self.url_distant,"-o",self.org,"-b",self.bucket,"-t",self.token,"-f","test_influxdb.csv"])

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
        with open(self.path, 'a+',newline='') as csvfile:
            writer = csv.writer(csvfile,delimiter=',')
            data=['','','0','2023-02-20T13:27:05.046873851Z','2023-02-21T13:27:05.046873851Z','2023-02-21T03:00:00.046873851Z','138.52','euros','cout_electricite','France']
            writer.writerow(data)

csw = CSVWriter('mod.csv')
csw.writeData()
