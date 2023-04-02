import requester as rq
import utils as ut
from datetime import datetime
from datetime import timedelta

def initDailyPrice():
    result=[]
    result = rq.getFRPrice()
    return result
    # mf.sendDailyPrice(result)


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

    end=ut.formatDateInfuxToDatetime(list_result[len(list_result)-1])
    end = ((end[0] + timedelta(hours=1)) - timedelta(seconds=ASC_end_sec), end[1])
   
    return {"segments":list_result, "end":ut.formatDateDatetimeToInfux(end[0])}

def optimization(target_value,ASC_parameters,DESC_parameters,prices):

    ASC_duration_activation = ut.getDurationActivation(target,ASC_parameters["energy"])

    segment_list = constructSegmentList(ASC_duration_activation)

    print(segment_list)


if __name__ == "__main__":
    prices = initDailyPrice()
    # prices=mf.getDailyPrice()

    prices.sort(key=ut.getVal)

    target={"val":5_000, "unit":"MW"}
    ASC_parameters={"energy":{"val":1_270, "unit":"MWH"},"min_activation_duration":"1.5h","max":{"val":37_000, "unit": "MW"},"max_actu":{"val":20_000, "unit": "MW"}}
    DESC_parameters={"energy":{"val":1_800, "unit":"MWH"},"max":{"val":33_000, "unit": "MW"},"max_actu":{"val":3_000, "unit": "MW"}}

    opt_table = optimization(target,ASC_parameters,DESC_parameters,prices)

    # print(opt_table)