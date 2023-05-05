import requester as rq
import manaflux as mf

def initDailyPrice():
    result=[]
    result = rq.getFRPrice() 
    if result == -1:
        print("Site web indisponible")
    else:
        mf.sendDailyPrice(result)

if __name__ == "__main__":
    initDailyPrice()