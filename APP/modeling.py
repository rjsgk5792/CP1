import pandas as pd
import pickle
import psycopg2
import sqlite3

host = 'salt.db.elephantsql.com'
user = 'enbagafy'
password = 'BVQpFmcjvhlTjrgYrbsWJeAsUtx1kvuZ'
database = 'enbagafy'

connection = psycopg2.connect(
    host=host,
    user=user,
    password=password,
    database=database
)

cur = connection.cursor()

cur.execute("select * from modify_csv")

movie=[]
rows = cur.fetchall()
for row in rows:
    movie.append(list(row))

movie = pd.DataFrame(movie, columns = ['영화명','감독','제작사','수입사','배급사','개봉일','국적','스크린수'
                                ,'관객수','장르','등급'])
                             
movie2=movie.drop(['영화명'], axis=1)

#int형으로 바꾸기
movie2["관객수"]=movie2["관객수"].apply(lambda x : int(x.replace(",", ""))) 
movie2["스크린수"]=movie2["스크린수"].apply(lambda x : int(x.replace(",", ""))) 
#달만 넣기
movie2["개봉일"]=movie2["개봉일"].apply(lambda x : int(str(x).replace("-", "")[4:6])) 

#훈련,테스트 세트 나누기
from sklearn.model_selection import train_test_split

target = movie2['관객수']
train, test = train_test_split(movie2, train_size=0.70, test_size=0.30, 
                              random_state=2)

target = '관객수'
features = train.columns.drop([target])

X_train = train[features]
y_train = train[target]

X_test = test[features]
y_test = test[target]

from category_encoders import OrdinalEncoder
from sklearn.metrics import r2_score
from xgboost import XGBRegressor
from sklearn.preprocessing import LabelEncoder

encoder = OrdinalEncoder()
X_train_encoded = encoder.fit_transform(X_train) 
X_test_encoded = encoder.transform(X_test) 

boosting = XGBRegressor(
    n_estimators=1000,
    objective='reg:squarederror', # default
    max_depth = 10,
    cv=5,
    child_weight = 6,
    gamma = 0.5,
    learning_rate=0.2,
    scoring=' neg_mean_squared_error',
    verbose=1,
    n_jobs=-1
)

eval_set = [(X_train_encoded, y_train), 
            (X_test_encoded, y_test)]

boosting.fit(X_train_encoded, y_train, 
          eval_set=eval_set,
          early_stopping_rounds=50
         )
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import r2_score

y_pred = boosting.predict(X_train_encoded)
r2 = r2_score(y_train, y_pred)
mae = mean_absolute_error(y_train, y_pred)

print(f' MAE: {mae}')
print(f' r2: {r2}')

from xgboost import plot_importance
import matplotlib.pyplot as plt

import matplotlib.font_manager as fm 
path = 'C:\\Users\\Downloads\\NanumBarunGothic.ttf' 

fig, ax = plt.subplots(figsize = (10, 12))
plt.rc('font', size=12)
plt.rc('font', family='NanumBarunGothic') 
plot_importance(boosting, ax = ax)

y_pred = boosting.predict(X_test_encoded)
r2 = r2_score(y_test, y_pred)
mae = mean_absolute_error(y_test, y_pred)

print(f' MAE: {mae}')
print(f' r2: {r2}')

student_card = pd.DataFrame({'감독':['김한민'],
                             '제작사':['(주)제이케이필름'],
                             '수입사':['None'],
                             '배급사':['CJ ENM'],
                             '개봉일':[7],
                             '국적':['한국'],
                             '스크린수':[1900],
                             '장르':['액션'],
                             '등급':['청소년관람불가']})
X_tests_encoded = encoder.transform(student_card) 

print(boosting.predict(X_tests_encoded))
# ###부호화
with open('model.pkl','wb') as pickle_file:
    pickle.dump(boosting, pickle_file)

with open('encoder.pkl','wb') as pf:
    pickle.dump(encoder, pf)