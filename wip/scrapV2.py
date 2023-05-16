import requester as rq
import utilsV2 as ut
import manaflux as mf
from datetime import timedelta
from datetime import datetime

def scrap_initDailyPrice():
    result=[]
    result = rq.getFRPrice() 
    # mf.manaflux_send_daily_price(result)
    return result

def scrap_extract_prices():
    # prices = scrap_initDailyPrice()
    prices=mf.manaflux_get_daily_price()
    prices.sort(key=ut.utils_key_sorted_prices)

    return prices

def scrap_format_prices(prices):
    for elm in prices:
        elm['time'] = ut.utils_format_infludb_to_datetime(elm['time'])
        elm['val'] = float(elm['val'])
    return prices

def scrap_extract_params(params):
    formatted_settings = {}

    formatted_settings['asc_consomation'] = ut.utils_format_watt(params['asc_consomation'],params['asc_consomation_choices'])
    formatted_settings['asc_capa_max'] = ut.utils_format_watt(params['asc_capa_max'],params['asc_capa_max_choices'])
    formatted_settings['asc_capa_actu'] = ut.utils_format_watt(params['asc_capa_actu'],params['asc_capa_actu_choices'])
    formatted_settings['desc_consomation'] = ut.utils_format_watt(params['desc_consomation'],params['desc_consomation_choices'])
    formatted_settings['desc_capa_max'] = ut.utils_format_watt(params['desc_capa_max'],params['desc_capa_max_choices'])
    formatted_settings['desc_capa_actu'] = ut.utils_format_watt(params['desc_capa_actu'],params['desc_capa_actu_choices'])
    formatted_settings['target'] = ut.utils_format_watt(params['target'],params['target_choices'])

    return formatted_settings

## Simple optimisation
def scrap_basic_construction_segment_list(formatted_prices,formatted_settings,status):
    if status == 1:
        duration = ut.utils_get_duration_activation(formatted_settings['target'],formatted_settings['asc_consomation'])
    else:
        duration = ut.utils_get_duration_activation(formatted_settings['target'],formatted_settings['desc_consomation'])
    
    duration_int=int(duration)
    duration_deci=duration % 1

    if (duration_int >= 24):
        return -1
    # print(duration, duration_int,duration_deci)

    # Construction de la liste des segments ou le pompage va être effectué
    if duration_deci != 0:
        nb_segments = duration_int+1
    else:
        nb_segments = duration_int

    list_segments = []
    for i in range(nb_segments):
        elm = {'time': formatted_prices[i]['time'], 'val': formatted_prices[i]['val']}
        list_segments.append(elm)
    
    # Calcul de la date de fin
    total_sec=duration*3_600
    end_sec=3_600-(total_sec-3_600*duration_int)
    # end_sec=int(end_sec/60)

    end=list_segments[len(list_segments)-1]
    end = (end['time'] + timedelta(hours=1)) - timedelta(seconds=end_sec)

    list_segments.sort(key=ut.utils_key_sorted_times)

    return {"segments":list_segments, "end":end}

## Choix de l'optimisation a effectuer
def scrap_contruct_segment_list(formatted_prices,formatted_settings,status):
    return scrap_basic_construction_segment_list(formatted_prices,formatted_settings,status)

## Formatage pour influxdb
def scrap_construct_influxdb_list(optimized_segment_list):
    end = optimized_segment_list['end']
    list_segments = optimized_segment_list['segments']

    points = []
    old_point_end=list_segments[0]['time'] + timedelta(hours=1)

    for elm in list_segments:
        point_to_add =  {'start':elm['time'] ,'end':elm['time'] + timedelta(hours=1)}

        if len(points) == 0:
            old_point_end=list_segments[0]['time'] + timedelta(hours=1)
            if elm['time'].hour == end.hour:
                points.append({'start':list_segments[0]['time'] ,'end':end})
            else:
                points.append({'start':list_segments[0]['time'] ,'end':list_segments[0]['time'] + timedelta(hours=1)})

        elif point_to_add['start'] == old_point_end: # Contigue
            if elm['time'].hour == end.hour:
                points[len(points)-1]['end'] = end
            else:
                points[len(points)-1]['end'] = point_to_add['end']
        else: # Non contigue
            if elm['time'].hour == end.hour:
                point_to_add['end']=end
                points.append(point_to_add)
            else:
                points.append(point_to_add)

        old_point_end=points[len(points)-1]['end']

    if points[len(points)-1]['end'].hour == end.hour:
        points[len(points)-1]['end'] = end

    for elm in points:
        elm['end']=ut.utils_end_of_day(elm['end'])

    return points

## Calcul du cout total de l'opération
def scrap_total_price_operation(optimized_segment_list, formatted_settings,status):

    if status == 1:
        power = ut.utils_format_watt_to_mega_watt(formatted_settings['asc_consomation'])
    else:
        power = ut.utils_format_watt_to_mega_watt(formatted_settings['desc_consomation'])

    to_find=optimized_segment_list['end'].hour
    for elm in optimized_segment_list['segments']:
        if elm['time'].hour == to_find:
            elm_end = elm
            break

    end=elm_end['time']

    end = end + timedelta(hours=1)
    delta = end - optimized_segment_list['end']
    delta = int(delta.total_seconds()) / 3600
    total=0
    for elm in optimized_segment_list['segments']:
        total = total + power * elm['val']

    total -= (power * delta)*elm_end['val']
    total = round(total,3) 

    return total

## Calcul de la durée d'activation / désactivation de l'opération
def scrap_total_duration_operation(point_list):
    total = 0
    for elm in point_list:
        a = elm['start']
        b = elm['end']
        delta = b - a
        delta = int(delta.total_seconds())
        total += delta

    return round(total/3600,2)

def scrap_calcul_rendement(formatted_settings):
    a = formatted_settings['asc_consomation']
    b = formatted_settings['desc_consomation']
    return round(a/b,2)

def scrap_optimisation(formatted_prices,formatted_settings):

    optimized_segment_list = scrap_contruct_segment_list(formatted_prices,formatted_settings,1) # OK
    
    ## Besoin de turbiner ?
    a = formatted_settings['asc_capa_actu'] + formatted_settings['target']
    new_target = a - formatted_settings['asc_capa_max']
    formatted_settings['target']=new_target
    reverse = 0
    if new_target > 0:
        reverse=1
    ##

    if reverse == 1: 
        formatted_prices.reverse()
        optimized_segment_list_reverse = scrap_contruct_segment_list(formatted_prices,formatted_settings,-1) # OK

    if (optimized_segment_list == -1):
        print("Impossible d'optimiser")
    else : 
        
        total_price = scrap_total_price_operation(optimized_segment_list,formatted_settings,1) # OK
        if reverse == 1: 
            total_price += scrap_total_price_operation(optimized_segment_list_reverse,formatted_settings,-1) # OK
        mf.manaflux_send_total_price(total_price)

    
        rendement = scrap_calcul_rendement(formatted_settings) # OK
        mf.manaflux_send_rendement(rendement)


        point_list = scrap_construct_influxdb_list(optimized_segment_list) # OK
        point_list_reverse=[]
        if reverse == 1:
            point_list_reverse = scrap_construct_influxdb_list(optimized_segment_list_reverse) # OK


        total_duration = scrap_total_duration_operation(point_list) # OK
        if reverse == 1:
            total_duration += scrap_total_duration_operation(point_list_reverse) # OK
        mf.manaflux_send_total_duration(total_duration)

        scrap_send_point_list(reverse,point_list,point_list_reverse)

def scrap_send_point_list(reverse,point_list,point_list_reverse):

    time_list_set=[]
    simple_point_list = ut.utils_format_point_to_influxdb(point_list,time_list_set,1)
    time_list_set = simple_point_list[1]
    mf.manaflux_send_opti(simple_point_list[0])

    if reverse == 1:
        reverse_point_list = ut.utils_format_point_to_influxdb(point_list_reverse,time_list_set,-1)
        mf.manaflux_send_opti(reverse_point_list[0])

    hour_list_set=[]
    zero_list=[]

    time_list_set= sorted(time_list_set)

    for elm in time_list_set:
        hour_list_set.append(elm.hour)

    for i in range(0,24):
        if i in hour_list_set:
            continue
        string = "1900 1 1 "+str(i)+" 0"
        time = datetime.strptime(string, "%Y %m %d %H %M")
        zero_list.append({ 'time': ut.utils_format_datetime_to_infuxdb(time), 'val': 0})

    for elm in point_list:
        start = elm ['start']
        end = elm ['end']

        to_add=0
        for rev_elm in point_list_reverse:
            rev_start=rev_elm['start']
            rev_end=rev_elm['end']
            
            if start - timedelta(seconds=1) == rev_end:
                to_add = -1 

        if to_add == 0:
            zero_list.append({ 'time': ut.utils_format_datetime_to_infuxdb(start - timedelta(seconds=1)), 'val': 0})
        to_add = 0

        for rev_elm in point_list_reverse:
            rev_start=rev_elm['start']
            rev_end=rev_elm['end']
            
            if end + timedelta(seconds=1) == rev_start:
                to_add = -1 
        if to_add == 0:
            zero_list.append({ 'time': ut.utils_format_datetime_to_infuxdb(end + timedelta(seconds=1)), 'val': 0})
        to_add = 0

    for elm in point_list_reverse:
        start = elm ['start']
        end = elm ['end']

        to_add=0
        for rev_elm in point_list:
            rev_start=rev_elm['start']
            rev_end=rev_elm['end']
            
            if start - timedelta(seconds=1) == rev_end:
                to_add = -1 

        if to_add == 0:
            zero_list.append({ 'time': ut.utils_format_datetime_to_infuxdb(start - timedelta(seconds=1)), 'val': 0})
        to_add = 0

        for rev_elm in point_list_reverse:
            rev_start=rev_elm['start']
            rev_end=rev_elm['end']
            
            if end + timedelta(seconds=1) == rev_start:
                to_add = -1 
        if to_add == 0:
            zero_list.append({ 'time': ut.utils_format_datetime_to_infuxdb(end + timedelta(seconds=1)), 'val': 0})
        to_add = 0


    mf.manaflux_send_opti(zero_list)

def scrap_is_valid(formatted_settings):
    if formatted_settings['asc_capa_actu'] + formatted_settings['target'] > formatted_settings['asc_capa_max']:
        a = formatted_settings['asc_capa_actu'] + formatted_settings['target']
        b = a - formatted_settings['asc_capa_max']
        c = formatted_settings['desc_capa_actu'] + b

        if c < formatted_settings['desc_capa_max']:
            time1 = ut.utils_get_duration_activation(formatted_settings['target'],formatted_settings['asc_consomation'])
            time2 = ut.utils_get_duration_activation(b,formatted_settings['desc_consomation'])
            if time1+time2 > 24:
                return -1
        else:
            return -1
    else:
        time = ut.utils_get_duration_activation(formatted_settings['target'],formatted_settings['asc_consomation'])
        if time > 24:
            return -1
    return 0

if __name__ == "__main__":

    input_params = {'asc_consomation': '1_270', 'asc_consomation_choices': 3, 
                'asc_capa_max': '37_000', 'asc_capa_max_choices': 3, 
                'asc_capa_actu': '20_000', 'asc_capa_actu_choices': 3, 
                'desc_consomation': '1_800', 'desc_consomation_choices': 3, 
                'desc_capa_max': '33_000', 'desc_capa_max_choices': 3, 
                'desc_capa_actu': '3_000', 'desc_capa_actu_choices': 3, 
                'target': '5_000', 'target_choices': 3, 
                'titre': 'Titre'}
    
    # prices = scrap_extract_prices()
    # formatted_prices = scrap_format_prices(prices)
    # formatted_settings = scrap_extract_params(input_params)
    # mf.manaflux_reset()
    # scrap_optimisation(formatted_prices,formatted_settings)
