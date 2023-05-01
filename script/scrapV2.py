import requester as rq
import utils as ut
import manaflux as mf
from datetime import timedelta

def initDailyPrice():
    result=[]
    result = rq.getFRPrice() 
    mf.sendDailyPrice(result)
    return result



if __name__ == "__main__":
    prices = initDailyPrice()
    # prices=mf.getDailyPrice() ## Une erreur

    prices.sort(key=ut.getVal)

    target={"val":5_000, "unit":"MW"}
    ASC_parameters={"energy":{"val":1_270, "unit":"MWH"},"min_activation_duration":"1.5h","max":{"val":37_000, "unit": "MW"},"max_actu":{"val":20_000, "unit": "MW"}}
    DESC_parameters={"energy":{"val":1_800, "unit":"MWH"},"max":{"val":33_000, "unit": "MW"},"max_actu":{"val":3_000, "unit": "MW"}}