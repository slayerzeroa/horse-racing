import pandas as pd
from kra import *
import tools
import horse_racing_chatbot as chatbot
from horse_xgboost_prob import *
import asyncio


start = '20240607'
end = '20240609'

df = get_predict_data(start, end)
print(df)

def main():
    start, end = tools.get_start_end()
    start = '20240607'
    end = '20240609'
    try:
        update_rcPlan()
    except:
        pass

    try:
        update_rcResult(start, end)
    except:
        pass

    try:
        update_modelData(start, end)
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


if __name__ == '__main__':
    main()