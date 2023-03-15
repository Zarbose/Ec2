import requester as rq
import manaflux as mf
from urllib3.exceptions import NewConnectionError

def initDailyPrice():
    result=[]
    result = rq.getFRPrice()
    mf.sendDailyPrice(result)


if __name__ == "__main__":
    initDailyPrice()
    prices=mf.getDailyPrice()