import requester as rq
import unit_manager as um
from datetime import datetime
from datetime import timedelta

def initDailyPrice():
    result=[]
    result = rq.getFRPrice()
    return result
    # mf.sendDailyPrice(result)

def getVal(prices):
  return float(prices['val'])

def getTime(list_result):
    return list_result['time']

def constructResult(ASC_duration_activation,DESC_duration_activation):
    ASC_int_part=int(ASC_duration_activation.getValue())
    ASC_deci_part=ASC_duration_activation.getValue() % 1

    nb_elm=0
    if ASC_deci_part > 0:
        nb_elm=ASC_int_part+1
    else:
        nb_elm=ASC_int_part

    list_result=[]
    for i in range(nb_elm):
        list_result.append(prices[i])

    list_result.sort(key=getTime)

    ASC_total_sec=ASC_duration_activation.getSeconde()
    ASC_end_sec=3_600-(ASC_total_sec-3_600*ASC_int_part)

    end=um.formatDateInfuxToDatetime(list_result[len(list_result)-1])
    end = ((end[0] + timedelta(hours=1)) - timedelta(seconds=ASC_end_sec), end[1])

    list_result[len(list_result)-1]['time']= um.formatDateDatetimeToInfux(end[0])
   
    return list_result


def optimization(target_value,ASC_parameters,DESC_parameters,prices):
    ## Target
    target = target_value

    ## Duration
    duration_params = um.getTimeParams(ASC_parameters["min_activation_duration"])  # TimeUnit obj

    ## Calc duration asc and desc
    ASC_duration_activation = um.getDurationActivation(target,ASC_parameters["energy"])
    DESC_duration_activation = um.getDurationActivation(target,DESC_parameters["energy"])


    result = constructResult(ASC_duration_activation,DESC_duration_activation)

    return result

if __name__ == "__main__":
    prices = initDailyPrice()
    # prices=mf.getDailyPrice()

    # print(prices)
    prices.sort(key=getVal)

    target={"val":5_000, "unit":"MW"}
    ASC_parameters={"energy":{"val":1_270, "unit":"MWH"},"min_activation_duration":"1.5h","max":{"val":37_000, "unit": "MW"},"max_actu":{"val":20_000, "unit": "MW"}}
    DESC_parameters={"energy":{"val":1_800, "unit":"MWH"},"max":{"val":33_000, "unit": "MW"},"max_actu":{"val":3_000, "unit": "MW"}}


    # opt_table = getSegment(target,ASC_parameters,DESC_parameters,prices) TODO
    opt_table = optimization(target,ASC_parameters,DESC_parameters,prices)

    print(opt_table)