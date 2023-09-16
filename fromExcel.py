import pandas as pd
import yaml as yml

import numpy as np
from sqlalchemy import create_engine

with open('info.yml') as info:
    data = yml.load(info, Loader=yml.FullLoader)

url = data['dataSource']['url']
file = data['file']

# 파일 불러오기
hospital_infos = pd.read_excel('/Users/heeyeop/Study/python/pythonProject1/1.병원정보서비스.xlsx')
hospital_details = pd.read_excel('/Users/heeyeop/Study/python/pythonProject1/5.의료기관별상세정보서비스_03_진료과목정보.xlsx')

print(hospital_details.info())

print(hospital_details.head())
target = hospital_details.loc[
    (hospital_details['진료과목코드'] == 2) |
    (hospital_details['진료과목코드'] == 3) |
    (hospital_details['진료과목코드'] == 84)
    ]
# 한방신경정신과 : 84 정신건강의학과 : 03 신경과:02

# details = hospital_details[['암호화요양기호', '요양기관명', '진료과목코드명', '과목별 전문의수', '선택진료 의사수']]

# 조인하기
# total = pd.merge(left=hospital_infos, right=hospital_details, how='inner', on='암호화요양기호')
# result = np.unique(total[['암호화요양기호']])

result = target.groupby(['암호화요양기호']).size().reset_index()
# print(result)

final = pd.merge(left=result, right=hospital_infos, how='inner', on='암호화요양기호')
data = final[['요양기관명', '주소', '전화번호']]
for_sql = data.rename(columns={'요양기관명': 'name', '전화번호': 'telephone', '주소': 'area'})

print(for_sql)

# https://map.naver.com/p/entry/place/12841376?lng=127.13962276849269&lat=37.53756467972275&placePath=%2Fhome&c=15.00,0,0,0,dh
# https://map.naver.com/p/search/%EB%A6%B4%EB%A6%AC%EC%84%B1%ED%98%95%EC%99%B8%EA%B3%BC%EC%9D%98%EC%9B%90/place/1790446530?isCorrectAnswer=true&c=15.00,0,0,0,dh

# engine = create_engine(url, echo=True)
# for_sql.to_sql(name='hospital', if_exists='append', con=engine, index=False)
