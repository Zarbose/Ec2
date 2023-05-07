import requester as rq
import utilsV2 as ut

def scrap_initDailyPrice():
    result=[]
    result = rq.getFRPrice() 
    # mf.sendDailyPrice(result)
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

if __name__ == "__main__":

    input_params = {'asc_consomation': '12', 'asc_consomation_choices': 1, 
                    'asc_tmp_min': '12', 'asc_tmp_min_choices': 1, 
                    'asc_capa_max': '12', 'asc_capa_max_choices': 1, 
                    'asc_capa_actu': '12', 'asc_capa_actu_choices': 1, 
                    'desc_consomation': '12', 'desc_consomation_choices': 1, 
                    'desc_capa_max': '12', 'desc_capa_max_choices': 1, 
                    'desc_capa_actu': '12', 'desc_capa_actu_choices': 1, 
                    'target': '12', 'target_choices': 1, 
                    'titre': 'Titre'}
    
    prices = scrap_extract_prices()
    prices = scrap_format_prices(prices)
    formatted_settings = scrap_extract_params(input_params)

    ut.utils_print_prices(prices)
    print(formatted_settings)