from datetime import datetime

WATT_CHOICES ={'1': "W",'2': "KW",'3': "MW",'4': "GW",'5': "TW"}

WATTH_CHOICES = {'1': "Wh",'2': "KWh",'3': "MWh",'4': "GWh",'5': "TWh"}

TIME_CHOICES ={'1': "H",'2': "M",'3': "S"}

def utils_key_sorted_prices(prices):
    return float(prices['val'])

def utils_format_watt(elm,unit):
    elm=float(elm)
    unit=int(unit)

    if (unit == 1):
        return elm
    elif (unit == 2):
        return elm*1_000
    elif (unit == 3):
        return elm*1_000_000
    elif (unit == 4):
        return elm*1_000_000_000
    elif (unit == 5):
        return elm*1_000_000_000_000


def utils_format_time(elm,unit):
    elm=float(elm)
    unit=int(unit)

    if (unit == 1):
        return elm*3_600
    elif (unit == 2):
        return elm*60
    elif (unit == 3):
        return elm
    
# 2023-05-07T14:00:00Z ==> datetime(2023-05-07T14:00:00)
def utils_format_infuxsb_to_datetime(elm):
    date=elm
    date=date.replace("Z","")
    date = datetime.strptime(date,'%Y-%m-%dT%H:%M:%S')
    return date

# 2023-05-07T14:00:00Z ==> datetime(14:00:00)
def utils_format_infludb_to_datetime(elm):
    date=elm
    date=date.split('T')
    date=date[1]
    date=date.replace("Z","")
    date = datetime.strptime(date,'%H:%M:%S')
    return (date)

def utils_print_prices(prices):
    for elm in prices:
        print(elm['time'],elm['val'])
