import requester as rq
import utils as ut
import manaflux as mf
from datetime import datetime
from datetime import timedelta

def initDailyPrice():
    result=[]
    result = rq.getFRPrice() 
    mf.sendDailyPrice(result)
    return result

def constructSegmentList(ASC_duration_activation):

    ASC_int_part=int(ASC_duration_activation.getValue())
    ASC_deci_part=ASC_duration_activation.getValue() % 1

    ### Combien de segments ?
    nb_elm=0
    if ASC_deci_part > 0:
        nb_elm=ASC_int_part+1
    else:
        nb_elm=ASC_int_part

    ### Ajout des segments les moins cher
    list_result=[]
    for i in range(nb_elm):
        list_result.append(prices[i])

    ### Tris par dates
    list_result.sort(key=ut.getTime)

    ### Calcul de la date de fin
    ASC_total_sec=ASC_duration_activation.getSeconde()
    ASC_end_sec=3_600-(ASC_total_sec-3_600*ASC_int_part)

    end=ut.formatElmDateInfuxToDatetime(list_result[len(list_result)-1])
    end = ((end[0] + timedelta(hours=1)) - timedelta(seconds=ASC_end_sec), end[1])
   
    return {"segments":list_result, "end":ut.formatElmDateDatetimeToInfux(end[0])}

### Pas finit ==> Faire des testes
def constructTimePointList(segments_list):

    # segments_list={'segments': [{'time': '2023-04-02T09:00:00Z', 'val': '31.83'}, {'time': '2023-04-02T11:00:00Z', 'val': '17.52'}, {'time': '2023-04-02T17:00:00Z', 'val': '22.24'}, {'time': '2023-04-02T18:00:00Z', 'val': '31.13'}], 'end': '2023-04-02T18:56:13'}
    ##  13h 15h - 17h 18h56
    key_point=[]

    segments=segments_list["segments"]
    end=segments_list["end"]

    # print()
    old_time = segments[0]["time"]
    format_old_time=ut.formatDateInfuxToDatetime(old_time)

    periode = {"start":old_time,"end":""}

    # key_point.append(old_time)
    for elm in segments:
        cur_time=elm["time"]
        format_cur_time=ut.formatDateInfuxToDatetime(cur_time)

        delta = format_cur_time - format_old_time

        if (delta.seconds != 0) and (delta.seconds > 3600):
            periode["end"]=ut.formatDateDatetimeToInfux(format_old_time + timedelta(hours=1))
            key_point.append(periode)
            periode = {"start":cur_time,"end":""}

        format_old_time=format_cur_time

    periode["end"]=end
    key_point.append(periode)
    # print(key_point)

    return key_point

def optimization(target_value,ASC_parameters,DESC_parameters,prices):

    ASC_duration_activation = ut.getDurationActivation(target,ASC_parameters["energy"])

    segments_list = constructSegmentList(ASC_duration_activation)

    time_point = constructTimePointList(segments_list)

    print(time_point)

    # mf.sendOptiTime(segment_list)


if __name__ == "__main__":
    prices = initDailyPrice()
    # prices=mf.getDailyPrice() ## Une erreur

    prices.sort(key=ut.getVal)

    target={"val":5_000, "unit":"MW"}
    ASC_parameters={"energy":{"val":1_270, "unit":"MWH"},"min_activation_duration":"1.5h","max":{"val":37_000, "unit": "MW"},"max_actu":{"val":20_000, "unit": "MW"}}
    DESC_parameters={"energy":{"val":1_800, "unit":"MWH"},"max":{"val":33_000, "unit": "MW"},"max_actu":{"val":3_000, "unit": "MW"}}

    # opt_table = optimization(target,ASC_parameters,DESC_parameters,prices)

    # print(opt_table)