import requests
from bs4 import BeautifulSoup
from datetime import datetime

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