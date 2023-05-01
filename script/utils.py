from datetime import datetime

### Sort utils

def getVal(prices):
  return float(prices['val'])

def getTime(list_result):
    return list_result['time']

### Time and Energy utils

class TimeUnit:
    def __init__(self,unit,value):
        self.unit=unit
        self.value=value
        self.seconde=0

        if self.unit == "h":
            self.seconde=self.value*3_600
        elif self.unit == "m":
            self.seconde=self.value*60
        elif self.unit == "s":
            self.seconde=self.value

    def getSeconde(self):
        return int(self.seconde)
    
    def getValue(self):
        return self.value
    
    def __str__(self):
        return str(self.value)+" "+str(self.unit)
    
class EnergyUnit:
    def __init__(self,value,unit):
        self.unit=unit
        self.value=value
        self.wattH=0

        if self.unit == "TWH" or self.unit == "TW":
            self.wattH = self.value*1_000_000_000_000
        elif self.unit == "GWH" or self.unit == "GW":
            self.wattH = self.value*1_000_000_000
        elif self.unit == "MWH" or self.unit == "MW":
            self.wattH = self.value*1_000_000
        elif self.unit == "KWH" or self.unit == "KW":
            self.wattH = self.value*1_000
        elif self.unit == "WH" or self.unit == "W":
            self.wattH = self.value


    def getNorma(self):
        return self.wattH

#### LA
def getTimeParams(str_time):
    units=["d","h","m","s"]
    for unit in units:
        if unit in str_time:
            if unit == "h":
                nb = float(str_time.replace("h",''))
                return TimeUnit("h",nb)
            elif unit == "m":
                nb = float(str_time.replace("m",''))
                return TimeUnit("m",nb)
            elif unit == "s":
                nb = float(str_time.replace("s",''))
                return TimeUnit("s",nb)
            
def getDurationActivation(target,energy):
    a = EnergyUnit(energy["val"],energy["unit"]) ## Watt/h
    b = EnergyUnit(target["val"],target["unit"]) ## Watt

    return TimeUnit("h",b.getNorma()/a.getNorma())

def formatDateInfuxToDatetime(elm):
    date=elm
    date=date.replace("Z","")
    date = datetime.strptime(date,'%Y-%m-%dT%H:%M:%S')
    return date

def formatElmDateInfuxToDatetime(elm):
    date=elm['time']
    value=elm['val']
    date=date.split('T')
    date=date[1]
    date=date.replace("Z","")
    date = datetime.strptime(date,'%H:%M:%S')
    return (date,value)

# 1900-01-01 23:56:13
# 2023-03-29T00:00:00Z

def formatDateDatetimeToInfux(elm):
    curent_day = datetime.today().strftime('%Y-%m-%d')
    string=str(curent_day)+"T"+str(elm.time())
    return string

def formatElmDateDatetimeToInfux(elm):
    curent_day = datetime.today().strftime('%Y-%m-%d')
    string=str(curent_day)+"T"+str(elm.time())
    return string


if __name__ == "__main__":
    print("Cannot used as a script")