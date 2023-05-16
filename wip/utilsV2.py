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
    return elm/1_000_000

def utils_end_of_day(value):
    value_day = int(value.strftime('%d'))
    if value_day == 2:
        return (value) - timedelta(seconds=1)
    return value 

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

def utils_format_point_to_influxdb(point_list,time_list_set,val):
    formated_list=[]

    if (len(time_list_set) == 0):
        time_list_set=[]

    for elm in point_list:
        start = elm['start']
        end = elm['end']

        while start <= end:
            if start in time_list_set and val == -1:
                formated_list.append({ 'time': utils_format_datetime_to_infuxdb(start + timedelta(seconds=1)), 'val': val})
                elm['start']=start + timedelta(seconds=1)
                time_list_set.append(start + timedelta(seconds=1))
            else:
                formated_list.append({ 'time': utils_format_datetime_to_infuxdb(start), 'val': val})
                time_list_set.append(start)
            
            start += timedelta(hours=1)
        
        if end != start:
            if start in time_list_set and val == -1:
                formated_list.append({ 'time': utils_format_datetime_to_infuxdb(end + timedelta(seconds=1)), 'val': val})
            else:
                formated_list.append({ 'time': utils_format_datetime_to_infuxdb(end), 'val': val})

    formated_list.sort(key=utils_key_sorted_influxdb)
    return (formated_list,time_list_set)

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
