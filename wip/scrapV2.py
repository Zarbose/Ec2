import requester as rq
import utilsV2 as ut
import manaflux as mf
from datetime import timedelta

def scrap_initDailyPrice():
    result=[]
    result = rq.getFRPrice() 
    # mf.manaflux_send_daily_price(result)
    return result

def scrap_extract_prices():
    prices = scrap_initDailyPrice()
    # prices=mf.getDailyPrice() ## Une erreur
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
    formatted_settings['asc_tmp_min'] = ut.utils_format_time(params['asc_tmp_min'],params['asc_tmp_min_choices'])
    formatted_settings['asc_capa_max'] = ut.utils_format_watt(params['asc_capa_max'],params['asc_capa_max_choices'])
    formatted_settings['asc_capa_actu'] = ut.utils_format_watt(params['asc_capa_actu'],params['asc_capa_actu_choices'])
    formatted_settings['desc_consomation'] = ut.utils_format_watt(params['desc_consomation'],params['desc_consomation_choices'])
    formatted_settings['desc_capa_max'] = ut.utils_format_watt(params['desc_capa_max'],params['desc_capa_max_choices'])
    formatted_settings['desc_capa_actu'] = ut.utils_format_watt(params['desc_capa_actu'],params['desc_capa_actu_choices'])
    formatted_settings['target'] = ut.utils_format_watt(params['target'],params['target_choices'])

    return formatted_settings

## Simple optimisation
def scrap_basic_construction_segment_list(formatted_prices,formatted_settings):
    asc_duration = ut.utils_get_duration_activation(formatted_settings['target'],formatted_settings['asc_consomation'])
    asc_duration_int=int(asc_duration)
    asc_duration_deci=asc_duration % 1

    if (asc_duration_int >= 24):
        return -1
    # print(asc_duration, asc_duration_int,asc_duration_deci)

    # Construction de la liste des segments ou le pompage va être effectué
    if asc_duration_deci != 0:
        nb_segments = asc_duration_int+1
    else:
        nb_segments = asc_duration_int

    list_segments = []
    for i in range(nb_segments):
        elm = {'time': formatted_prices[i]['time'], 'val': formatted_prices[i]['val'], 'status': 1}
        list_segments.append(elm)
    
    
    list_segments.sort(key=ut.utils_key_sorted_times)

    # ut.utils_print_prices(list_segments)

    # Calcul de la date de fin
    total_sec=asc_duration*3_600
    end_sec=3_600-(total_sec-3_600*asc_duration_int)
    # end_sec=int(end_sec/60)

    end=list_segments[len(list_segments)-1]
    end = (end['time'] + timedelta(hours=1)) - timedelta(seconds=end_sec)
    # print(end)

    return {"segments":list_segments, "end":end}

## Optimisation complexe
def scrap_complex_construction_segment_list(formatted_prices,formatted_settings):
    asc_duration = ut.utils_get_duration_activation(formatted_settings['target'],formatted_settings['asc_consomation'])
    asc_duration_int=int(asc_duration)
    asc_duration_deci=asc_duration % 1

    if (asc_duration_int >= 24):
        return -1

## Choix de l'optimisation a effectuer
def scrap_contruct_segment_list(formatted_prices,formatted_settings):
    return scrap_basic_construction_segment_list(formatted_prices,formatted_settings)

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
            points.append({'start':list_segments[0]['time'] ,'end':list_segments[0]['time'] + timedelta(hours=1)})
        elif point_to_add['start'] == old_point_end: # Contigue
            points[len(points)-1]['end'] = point_to_add['end']
        else: # Non contigue
            points.append(point_to_add)

        old_point_end=point_to_add['end']

    points[len(points)-1]['end'] = end

    return points

## Calcul du cout total de l'opération
def scrap_total_price_operation(optimized_segment_list, formatted_settings):
    asc = ut.utils_format_watt_to_mega_watt(formatted_settings['asc_consomation'])
    end = optimized_segment_list['segments'][len(optimized_segment_list['segments'])-1]['time']
    end = end + timedelta(hours=1)
    delta = end - optimized_segment_list['end']
    delta = int(delta.total_seconds()) / 3600
    total = 0
    for elm in optimized_segment_list['segments']:
        total = total + asc * 1
    total -= asc * delta
    total = round(total,3) 

    return total

## Clcul de la durée d'activation / désactivation de l'opération
def scrap_total_duration_operation(point_list):
    total = 0
    for elm in point_list:
        a = elm['start']
        b = elm['end']
        delta = b - a
        delta = int(delta.total_seconds())
        total += delta

    return round(total/3600,2)


def scrap_optimisation(formatted_prices,formatted_settings):
    optimized_segment_list = scrap_contruct_segment_list(formatted_prices,formatted_settings)
    if (optimized_segment_list == -1):
        print("Impossible d'optimiser")
    else : 
        total_price = scrap_total_price_operation(optimized_segment_list,formatted_settings)
        mf.manaflux_send_total_price(total_price) 

        point_list = scrap_construct_influxdb_list(optimized_segment_list)
        
        total_duration = scrap_total_duration_operation(point_list)
        mf.manaflux_send_total_duration(total_duration)

        mf.manaflux_send_opti(ut.utils_format_point_to_influxdb(point_list))
        # for elm in ut.utils_format_point_to_influxdb(point_list):
        #     print(elm)



if __name__ == "__main__":

    input_params = {'asc_consomation': '1_170', 'asc_consomation_choices': 4, 
                    'asc_tmp_min': '1', 'asc_tmp_min_choices': 1, 
                    'asc_capa_max': '37_000', 'asc_capa_max_choices': 4, 
                    'asc_capa_actu': '20_000', 'asc_capa_actu_choices': 4, 
                    'desc_consomation': '1_800', 'desc_consomation_choices': 4, 
                    'desc_capa_max': '33_000', 'desc_capa_max_choices': 4, 
                    'desc_capa_actu': '3_000', 'desc_capa_actu_choices': 4, 
                    'target': '5_000', 'target_choices': 4, 
                    'titre': 'Titre'}
    
    prices = scrap_extract_prices()
    # ut.utils_print_prices(prices)
    formatted_prices = scrap_format_prices(prices)
    formatted_settings = scrap_extract_params(input_params)

    # ut.utils_print_prices(prices)
    # ut.utils_print_params(formatted_settings)

    scrap_optimisation(formatted_prices,formatted_settings)