import pandas as pd
from kra import *
import tools
import horse_racing_chatbot as chatbot
from horse_xgboost_prob import *
import asyncio

#
# start = '20240607'
# end = '20240609'
#
# df = get_predict_data(start, end)
# print(df)

def main():
    start, end = tools.get_start_end()
    start = '20240615'
    end = '20240615'
    update_rcPlan(start, end)
    print('rcPlan updated')
    update_rcResult(start, end)
    print('rcResult updated')
    update_modelData(start, end)
    print('modelData updated')

    try:
        df = get_predict_data(start, end)
        print(df)
        df = tools.filter_only_winner(df)
        print(df)
        asyncio.run(chatbot.send_df(df))
    except:
        pass


main()

while True:
    ## 매일 00시 01분에 실행
    now = datetime.datetime.now()
    if now.hour == 9 and now.minute == 1:
        try:
            main()
            print('horse prediction completed')
        except Exception as e:
            print(e)