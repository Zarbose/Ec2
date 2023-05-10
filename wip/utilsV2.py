from datetime import datetime
from datetime import timedelta

WATT_CHOICES ={'1': "W",'2': "KW",'3': "MW",'4': "GW",'5': "TW"}

WATTH_CHOICES = {'1': "Wh",'2': "KWh",'3': "MWh",'4': "GWh",'5': "TWh"}

TIME_CHOICES ={'1': "H",'2': "M",'3': "S"}

# Key function to sort list
def utils_key_sorted_prices(prices):
    return float(prices['val'])

def utils_key_sorted_times(list):
    return list['time']

def utils_key_sorted_influxdb(list):
    return str(list['time'])

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
    
def utils_format_watt_to_mega_watt(elm):
    return elm/1_000_000_000

# 2023-05-07T14:00:00Z ==> datetime(14:00:00)
def utils_format_infludb_to_datetime(elm):
    date=elm
    date=date.split('T')
    date=date[1]
    date=date.replace("Z","")
    date = datetime.strptime(date,'%H:%M:%S')
    return (date)

def utils_format_datetime_to_infuxdb(elm):
    elm = elm.replace(microsecond=0)
    curent_day = datetime.today().strftime('%Y-%m-%d')
    string=str(curent_day)+"T"+str(elm.time())+"Z"
    return string

def utils_format_point_to_influxdb(point_list): # bugger
    formated_list=[]
    for elm in point_list:
        formated_list.append({ 'time': utils_format_datetime_to_infuxdb(elm['start']), 'val': 1})
        formated_list.append({ 'time': utils_format_datetime_to_infuxdb(elm['end']), 'val': 1})

    string = "1900 1 1 0 0"
    old_time = datetime.strptime(string, "%Y %m %d %H %M")

    end_time = formated_list[len(formated_list)-1]['time']
    copy_formated_list = []
    for elm in formated_list:
        copy_formated_list.append(elm)


    for elm in copy_formated_list:
        while old_time < utils_format_infludb_to_datetime(elm['time']):
            if utils_format_infludb_to_datetime(elm['time']) == utils_format_infludb_to_datetime(end_time) :
                formated_list.append({ 'time': utils_format_datetime_to_infuxdb(utils_format_infludb_to_datetime(elm['time']) + timedelta(minutes=1)), 'val': 0})
                formated_list.append({ 'time': utils_format_datetime_to_infuxdb(old_time + timedelta(hours=1)), 'val': 0})
                old_time += timedelta(hours=1)
            else:
                formated_list.append({ 'time': utils_format_datetime_to_infuxdb(old_time), 'val': 0})
                old_time += timedelta(hours=1)
        old_time += timedelta(hours=1)

    while old_time < datetime.strptime("1900 1 1 23 59", "%Y %m %d %H %M"):
        formated_list.append({ 'time': utils_format_datetime_to_infuxdb(old_time), 'val': -1}) ## ICI !!!!!!
        old_time += timedelta(hours=1)

    formated_list.sort(key=utils_key_sorted_influxdb)
    return formated_list

def utils_get_duration_activation(target,energy):
    a = energy # Watt/h
    b = target # Watt
    return b/a

# Print functions
def utils_print_prices(prices):
    for elm in prices:
        print(elm['time'],elm['val'])

def utils_print_params(params):
    for keys,value in params.items():
        print(keys,value)
