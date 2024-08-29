import pandas as pd
from data.api.legacy.legacy_240829 import *
from data.preprocess import tools
from chatbot import horse_racing_chatbot as chatbot
from models.tree_model.boosting_model.prob_model.horse_xgboost_prob import *
import asyncio

#
# start = '20240617'
# end = '20240'
#
# df = get_predict_data(start, end)
# print(df)

def main():
    # start, end = tools.get_start_end()
    today = datetime.datetime.today().strftime('%Y%m%d')
    print(today)
    start = today
    end = today

    try:
        update_rcPlan(start, end)
        print('rcPlan updated')
        update_rcResult(start, end)
        print('rcResult updated')
        update_modelData(start, end)
        print('modelData updated')
    except:
        pass

    try:
        df = get_predict_data(start, end)
        print(df)
        df = tools.filter_only_winner(df)
        print(df)
        asyncio.run(chatbot.send_df(df))
    except:
        pass


while True:
    ## 매일 00시 01분에 실행
    now = datetime.datetime.now()
    if now.hour == 9 and now.minute == 1:
        try:
            main()
            print('horse prediction completed')
        except Exception as e:
            print(e)