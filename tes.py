from controller.forecasting import *
from controller.readdata import *
from controller.prepocessing import return_data

forecast = Forecasting(return_data("Jawa Timur"))
# print(forecast.grup)
for i in range(len(forecast.list_didi)):
    print(forecast.list_difi[i], forecast.list_didi[i], forecast.list_mape[i])
