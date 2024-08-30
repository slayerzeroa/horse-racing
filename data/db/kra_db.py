import pandas as pd
from data.preprocess import tools
import pymysql
import datetime

# 최종 DB 관련 함수

# meet {1: 서울, 2: 제주, 3: 부경}
# date = 'yyyymmdd'
def update_rcPlan(rcPlan_df: pd.DataFrame):
    # DB에 저장
    host, user, password, db = tools.get_env('DB')

    conn = pymysql.connect(host=host, user=user, password=password, db=db, charset='utf8mb4')
    curs = conn.cursor()

    # 만약 rcId가 이미 존재한다면 update 하고 없으면 insert
    for row in rcPlan_df.iterrows():
        sql = f"""
        INSERT INTO rcPlan (rcId, ageCond, budam, buga1, buga2, buga3, chaksun1, chaksun2, chaksun3, chaksun4, chaksun5, 
                            ilsu, meet, rank, rcDate, rcDist, rcNo, schStTime, sexCond, spRating, stRating) 
        VALUES ('{row[1]['rcId']}', '{row[1]['ageCond']}', '{row[1]['budam']}', '{row[1]['buga1']}', '{row[1]['buga2']}', 
                '{row[1]['buga3']}', '{row[1]['chaksun1']}', '{row[1]['chaksun2']}', '{row[1]['chaksun3']}', 
                '{row[1]['chaksun4']}', '{row[1]['chaksun5']}', '{row[1]['ilsu']}', '{row[1]['meet']}', '{row[1]['rank']}', 
                '{row[1]['rcDate']}', '{row[1]['rcDist']}', '{row[1]['rcNo']}', '{row[1]['schStTime']}', '{row[1]['sexCond']}', 
                '{row[1]['spRating']}', '{row[1]['stRating']}')
        ON DUPLICATE KEY UPDATE
            ageCond=VALUES(ageCond), 
            budam=VALUES(budam), 
            buga1=VALUES(buga1), 
            buga2=VALUES(buga2), 
            buga3=VALUES(buga3), 
            chaksun1=VALUES(chaksun1), 
            chaksun2=VALUES(chaksun2), 
            chaksun3=VALUES(chaksun3), 
            chaksun4=VALUES(chaksun4), 
            chaksun5=VALUES(chaksun5), 
            ilsu=VALUES(ilsu), 
            meet=VALUES(meet), 
            rank=VALUES(rank), 
            rcDate=VALUES(rcDate), 
            rcDist=VALUES(rcDist), 
            rcNo=VALUES(rcNo), 
            schStTime=VALUES(schStTime), 
            sexCond=VALUES(sexCond), 
            spRating=VALUES(spRating), 
            stRating=VALUES(stRating)
        """
        curs.execute(sql)

        conn.commit()
        conn.close()



def update_rcResult(rcResult_df: pd.DataFrame):
    rcResult_df['hrNameEn'] = rcResult_df['hrNameEn'].apply(lambda x: x.replace("'", "''") if isinstance(x, str) else x)
    rcResult_df['jkNameEn'] = rcResult_df['jkNameEn'].apply(lambda x: x.replace("'", "''") if isinstance(x, str) else x)
    rcResult_df['owNameEn'] = rcResult_df['owNameEn'].apply(lambda x: x.replace("'", "''") if isinstance(x, str) else x)
    rcResult_df['trNameEn'] = rcResult_df['trNameEn'].apply(lambda x: x.replace("'", "''") if isinstance(x, str) else x)

    # DB에 저장
    host, user, password, db = tools.get_env('DB')
    conn = pymysql.connect(host=host, user=user, password=password, db=db, charset='utf8mb4')
    curs = conn.cursor()

    # 기존 rcResult 테이블의 globalUnique 키 목록 가져오기
    curs.execute("SELECT globalUnique FROM rcResult")
    existing_keys = {row[0] for row in curs.fetchall()}

    for index, row in rcResult_df.iterrows():
        if row['globalUnique'] in existing_keys:
            # 중복되는 행은 업데이트
            update_values = []
            for col in rcResult_df.columns:
                if col != 'globalUnique':  # Skip the primary key column
                    value = row[col]
                    if pd.isna(value):
                        value = 'NULL'
                    elif isinstance(value, str):
                        value = f"'{value}'"
                    else:
                        value = str(value)
                    update_values.append(f"{col} = {value}")

            update_sql = f"UPDATE rcResult SET {', '.join(update_values)} WHERE globalUnique = '{row['globalUnique']}'"
            curs.execute(update_sql)
        else:
            # 중복되지 않는 행은 삽입
            insert_values = []
            for col in rcResult_df.columns:
                value = row[col]
                if pd.isna(value):
                    value = 'NULL'
                elif isinstance(value, str):
                    value = f"'{value}'"
                else:
                    value = str(value)
                insert_values.append(value)

            insert_sql = f"INSERT INTO rcResult ({', '.join(rcResult_df.columns)}) VALUES ({', '.join(insert_values)})"
            curs.execute(insert_sql)

    conn.commit()
    conn.close()

def update_modelData(modelData_df: pd.DataFrame):
    # DB에 저장
    host, user, password, db = tools.get_env('DB')
    conn = pymysql.connect(host=host, user=user, password=password, db=db, charset='utf8mb4')
    curs = conn.cursor()

    # 기존 model 테이블의 globalUnique 키 목록 가져오기
    curs.execute("SELECT globalUnique FROM model")
    existing_keys = {row[0] for row in curs.fetchall()}

    for index, row in modelData_df.iterrows():
        if row['globalUnique'] in existing_keys:
            # 중복되는 행은 업데이트
            update_values = []
            for col in modelData_df.columns:
                if col != 'globalUnique':  # Skip the primary key column
                    value = row[col]
                    if pd.isna(value):
                        value = 'NULL'
                    elif isinstance(value, str):
                        value = f"'{value}'"
                    else:
                        value = str(value)
                    update_values.append(f"{col} = {value}")

            update_sql = f"UPDATE model SET {', '.join(update_values)} WHERE globalUnique = '{row['globalUnique']}'"
            curs.execute(update_sql)
        else:
            # 중복되지 않는 행은 삽입
            insert_values = []
            for col in modelData_df.columns:
                value = row[col]
                if pd.isna(value):
                    value = 'NULL'
                elif isinstance(value, str):
                    value = f"'{value}'"
                else:
                    value = str(value)
                insert_values.append(value)

            insert_sql = f"INSERT INTO model ({', '.join(modelData_df.columns)}) VALUES ({', '.join(insert_values)})"
            curs.execute(insert_sql)

    conn.commit()
    conn.close()



def load_rcResult():
    host, user, password, db = tools.get_env('DB')
    conn = pymysql.connect(host=host, user=user, password=password, db=db, charset='utf8mb4')
    curs = conn.cursor()

    curs.execute("SELECT * FROM rcResult")
    rcResult_df = pd.DataFrame(curs.fetchall(), columns=[col[0] for col in curs.description])

    conn.close()

    return rcResult_df