import requester as rq
import manaflux as mf
import unit_manager as um

def initDailyPrice():
    result=[]
    result = rq.getFRPrice()
    mf.sendDailyPrice(result)

def optimization(ASC_parameters,DESC_parameters):

    # Faire les conversions

    ### Reading parameters
    target = 0
    target_max = 0
    if(ASC_parameters["target"] == -1):
        target = target_max = ASC_parameters["target_max"]
    else:
        target = ASC_parameters["target"]
        target_max = ASC_parameters["target_max"]

    duration_params = um.getTimeParams(ASC_parameters["duration"])
    duration_seconds = duration_params["sec"]

    duration_activation = um.getDurationActivation(duration_params,target)

    print(target,target_max,duration_seconds)
    return 1


if __name__ == "__main__":
    # initDailyPrice()
    # prices=mf.getDailyPrice()

    # Exemple pour le Barrage de Grand'Maison
    # ATENTION à la gestion des unités
    ASC_parameters={"target":15_000,"target_max":37_000,"speed":135,"energy":1_270,"duration":"1h"}
    DESC_parameters={"speed":216.3,"energy":1_800}

    optimization(ASC_parameters,DESC_parameters)