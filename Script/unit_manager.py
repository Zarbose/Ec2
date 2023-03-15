def getTimeParams(str_time):
    units=["d","h","m","s"]
    for unit in units:
        if unit in str_time:
            if unit == "d":
                nb = int(str_time.replace("d",''))
                return {"sec":nb*86_400, "value":nb, "unit":"day"}
            elif unit == "h":
                nb = int(str_time.replace("h",''))
                return {"sec":nb*3_600, "value":nb, "unit":"hour"}
            elif unit == "m":
                nb = int(str_time.replace("m",''))
                return {"sec":nb*60, "value":nb, "unit":"minute"}
            elif unit == "s":
                nb = int(str_time.replace("s",''))
                return {"sec":nb, "value":nb, "unit":"second"}
            
def getDurationActivation(speed,energy,target):
    # ATENTION conversion
    result = {"sec":0, "value":0, "unit":""}


    # if duration_params["unit"] == "day":
    #     nb_s = duration_params["sec"]
    #     nb_v = duration_params["value"]
    #     return {"sec":nb*86_400, "value":nb, "unit":"day"}
    # elif duration_params["unit"] == "hour":
    #     return {"sec":nb*3_600, "value":nb, "unit":"hour"}
    # elif duration_params["unit"] == "minute":
    #     return {"sec":nb*60, "value":nb, "unit":"minute"}
    # elif duration_params["unit"] == "second":
    #     return {"sec":nb, "value":nb, "unit":"second"}

    return 1


if __name__ == "__main__":
    print("Cannot used as a script")