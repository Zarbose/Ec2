import requester as rq
import unit_manager as um
from datetime import datetime

def initDailyPrice():
    result=[]
    result = rq.getFRPrice()
    return result
    # mf.sendDailyPrice(result)

def optimization(target_value,ASC_parameters,DESC_parameters,prices):
    ## Target
    target = target_value

    ## Duration
    duration_params = um.getTimeParams(ASC_parameters["min_activation_duration"])  # TimeUnit obj
    # print(duration_params)

    ## Calc duration asc and desc
    ASC_duration_activation = um.getDurationActivation(target,ASC_parameters["energy"])
    DESC_duration_activation = um.getDurationActivation(target,DESC_parameters["energy"])
    # print(ASC_duration_activation,DESC_duration_activation)

    ASC_int_part=int(ASC_duration_activation.getValue())
    ASC_deci_part=ASC_duration_activation.getValue() % 1
    # print(ASC_int_part,ASC_deci_part)

    nb_elm=0
    if ASC_deci_part > 0:
        nb_elm=ASC_int_part+1
    else:
        nb_elm=ASC_int_part

    list_result=[]
    for i in range(nb_elm):
        list_result.append(prices[i])

    list_result=sorted(list_result,key=lambda elm:elm[0])

    # ASC_total_sec=ASC_duration_activation.getSeconde()
    # ASC_end_sec=ASC_total_sec-3_600*ASC_int_part

    # if (ASC_end_sec != 0):
        

    print(list_result)

    return 1

def verifySort(list):
    old=float(list[0][1])
    for elm in list:
        if float(elm[1]) < old:
            return False
        old=float(elm[1])
    return True

def fprintSortedList(list):
    for elm in list:
        print(float(elm[1]))

def formatPricesList(list):
    new_list=[]
    # 2023-03-20T12:00:00Z
    for elm in list:
        date=elm[0]
        value=elm[1]
        date=date.split('T')
        date=date[1]
        date=date.replace("Z","")
        date = datetime.strptime(date,'%H:%M:%S')
        new_list.append((date,value))
    return new_list


if __name__ == "__main__":
    prices = initDailyPrice()
    # prices=mf.getDailyPrice()

    sorted_prices=sorted(prices,key=lambda price:price[1])
    
    # print(prices)
    # print(sorted_prices)
    # print("Verification ",verifySort(sorted_prices))
    # fprintSortedList(sorted_prices)

    target={"val":5_000, "unit":"MW"}
    ASC_parameters={"energy":{"val":1_270, "unit":"MWH"},"min_activation_duration":"1.5h"}
    DESC_parameters={"energy":{"val":1_800, "unit":"MWH"}}

    # print(formatPricesList(sorted_prices))
    # print()

    optimization(target,ASC_parameters,DESC_parameters,formatPricesList(sorted_prices))