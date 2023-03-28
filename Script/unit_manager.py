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


    def getWattH(self):
        return self.wattH


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
    a = EnergyUnit(energy["val"],energy["unit"])
    b = EnergyUnit(target["val"],target["unit"])

    return TimeUnit("h",b.getWattH()/a.getWattH())


# ASC_parameters={"energy":{"val":1_270, "unit":"MWH"},"min_activation_duration":"1.5h","max":{"val":37_000, "unit": "MW"},"max_actu":{"val":20_000, "unit": "MW"}}
def formatAscParams(params_table):
    return "TODO"


if __name__ == "__main__":
    print("Cannot used as a script")