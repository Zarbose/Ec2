import requester as rq
import manaflux as mf

def initDailyPrice():
    result=[]
    result = rq.getFRPrice() 
    mf.sendDailyPrice(result)

if __name__ == "__main__":
    initDailyPrice()