import requests
from bs4 import BeautifulSoup
from datetime import datetime

date = datetime.today().strftime('%d.%m.%Y')
url = 'https://transparency.entsoe.eu/transmission-domain/r2/dayAheadPrices/show?name=&defaultValue=false&viewType=TABLE&areaType=BZN&atch=false&dateTime.dateTime='+date+'+00:00|CET|DAY&biddingZone.values=CTY|10YFR-RTE------C!BZN|10YFR-RTE------C&resolution.values=PT60M&dateTime.timezone=CET_CEST&dateTime.timezone_input=CET+(UTC+1)+/+CEST+(UTC+2)'

def getFRPrice():
    response = requests.get(url)
    if response.status_code != 200:
        print("Error fetching page error : "+str(response.status_code))
        exit(1)

    soup = BeautifulSoup(response.content, 'html.parser')
    listValues = soup.find_all(class_="data-view-detail-link")

    if (len(listValues) != 24):
        print("Error when reading the web page")
        exit(2)

    N=len(listValues)
    result=[]
    curent_day = datetime.today().strftime('%Y-%m-%d')
    for i in range(N):
        if i<10:
            time=curent_day+"T0"+str(i)+":00:00Z"
        else:
            time=curent_day+"T"+str(i)+":00:00Z"
        result.append({'time':time,'val':listValues[i].text})

    return result

if __name__ == "__main__":
    print(getFRPrice())