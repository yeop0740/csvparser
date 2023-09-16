import pandas as pd
import yaml as yml

from sqlalchemy import create_engine

with open('info.yml') as info:
    data = yml.load(info, Loader=yml.FullLoader)

url = data['dataSource']['url']
file = data['file']


# print(data['dataSource']['url'])
# print(file)

# 서울시 병의원 위치 정보, https://data.seoul.go.kr/dataList/OA-20337/S/1/datasetView.do
hospitals = pd.read_csv(file, encoding="cp949")

data = hospitals[['주소', '비고', '기관설명상세', '기관명', '대표전화1', '병원경도', '병원위도']]

a = data.loc[
    (data['비고'].str.contains("정신", na=False)) |
    (data['기관설명상세'].str.contains("정신", na=False)) |
    (data['기관명'].str.contains('정신', na=False))
    ]

for stri in a['주소']:
    print(stri)

a['주소'] = a['주소'].astype('str')
splited_address = a['주소'].str.split(',', maxsplit=1)
a['area'] = splited_address.str.get(1)
a['주소a'] = splited_address.str.get(0)
a['주소a'] = a['주소a'].astype('str')
areas = a['주소a'].str.split(' ')
a['area1'] = areas.str.get(0)
a['area2'] = areas.str.get(1)
a['area3'] = areas.str.get(2).str.cat(areas.str.get(3), sep=' ')

final = a[['기관명', '대표전화1', 'area1', 'area2', 'area3', 'area']]

# areas = splited_address[0].astype('str').split(' ')
# areas = splited_address.str.split(' ')

toSQL = final.rename(columns={'기관명':'name', '대표전화1':'telephone'})
# toSQL['create_date'] = ''
# toSQL['last_modified_date'] = ''
# toSQL['average_rating'] = ''
# toSQL['number_of_reviews'] = ''
# toSQL['total_rating'] = ''
# toSQL['url'] = ''
toSQL['map_url'] = ''


# engine = create_engine(url, echo=True)
# toSQL.to_sql(name='hospital', if_exists='append' ,con=engine, index=False)
