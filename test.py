import pandas as pd
# from data.api.legacy.legacy_240829 import *

from data.api.kra_api import *
from data.db.kra_db import *

from data.preprocess import tools
from chatbot import horse_racing_chatbot as chatbot
from models.tree_model.boosting_model.prob_model.horse_xgboost_prob import *
import asyncio
import datetime


def main(date:str):
    # start, end = tools.get_start_end()
    today = date
    start = today
    end = today

    update_rcPlan(start, end)
    print('rcPlan updated')
    update_rcResult(start, end)
    print('rcResult updated')
    update_modelData(start, end)
    print('modelData updated')

    df = get_predict_data(start, end)
    print(df)
    df = tools.filter_only_winner(df)
    print(df)
    asyncio.run(chatbot.send_df(df))


# # start = datetime 2024-06-17
# start = '20240617'
# start = datetime.datetime.strptime(start, '%Y%m%d').date()

# while start <= datetime.datetime.today().date():
#     main(start.strftime('%Y%m%d'))
#     print('horse prediction completed')
#     print(start)
#     print(datetime.datetime.today().date())
#     start = start + datetime.timedelta(days=1)







# # update_rcResult(start, end)
# rcResult_df = (get_rcResult(start))
# print(rcResult_df)
# modelData_df = get_modelData(rcResult_df)
# print(modelData_df)

# update_rcResult(rcResult_df)
# print('rcResult updated')
# update_modelData(modelData_df)
# print('modelData updated')

# print(get_daily_rcResult(3, end))
# update_modelData(start, end)

start ='20240615'
end = '20240829'

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

while start <= end:
    try:
        rcResult_df = (get_rcResult(start))
        print(rcResult_df)
        modelData_df = get_modelData(rcResult_df)
        print(modelData_df)
    except:
        print('no data')
        start = datetime.datetime.strptime(start, '%Y%m%d').date() + datetime.timedelta(days=1)
        start = start.strftime('%Y%m%d')
        continue

    update_rcResult(rcResult_df)
    print('rcResult updated')
    update_modelData(modelData_df)
    print('modelData updated')
    start = datetime.datetime.strptime(start, '%Y%m%d').date() + datetime.timedelta(days=1)
    start = start.strftime('%Y%m%d')