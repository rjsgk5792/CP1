from flask import Flask, render_template, request
import pandas as pd
import pickle
from ccc import abc
import datetime

# import os
# import psycopg2
# import sqlite3

# DB_FILENAME = 'datadb.db'
# DB_FILEPATH = os.path.join(os.getcwd(), DB_FILENAME)

# conn = sqlite3.connect(DB_FILENAME) #없으면 자동생성
# cur = conn.cursor()

# cur.execute("select * from priceBytime")

# data=[]
# rows = cur.fetchall()
# for row in rows:
#     data.append(list(row))

with open("rf_model.pkl","rb") as fr:
   boosting = pickle.load(fr)

app = Flask(__name__)
   
@app.route('/',methods = ['GET','POST'])
def home(): 
   # return render_template('blog.html',data=data)
   if request.method == 'GET':
      return render_template('blog.html')
   
   elif request.method == 'POST':
      value=abc()
      return render_template('blog.html',
                              name1=value[0],
                              name2=value[1],
                              name3=value[2],
                              name4=value[3],
                              name5=value[4],
                              name6=value[5],
                              name7=value[6],
                              name8=value[7],
                              name9=value[8],
                              name10=value[9],
                              name11=value[10],
                              name12=value[11],
                              name13=value[12],
                              name14=value[13],
                              name15=value[14],
                              name16=value[15],
                              name17=value[16],
                              name18=value[17],
                              name19=value[18],
                              name20=value[19],
                              name21=value[20],
                              name22=value[21],
                              name23=value[22],
                              name24=value[23],
                              name25=value[24],
                              name26=value[25],
                              name27=value[26],
                              name28=value[27],
                              name29=value[28],
                              name30=value[29],
                              name31=value[30],
                              name32=value[31],
                              name33=value[32],
                              name34=value[33],
                              name35=value[34],
                              name36=value[35],
                              name37=value[36],
                              name38=value[37],
                              name39=value[38],
                              name40=value[39],
                              name41=value[40],
                              name42=value[41],
                              name43=value[42],
                              name44=value[43],
                              name45=value[44],
                              name46=value[45],
                              name47=value[46],
                              name48=value[47],
                              name49=value[48],
                              name50=value[49])
  
@app.route('/result',methods = ['GET','POST'])
def result():
   

   if request.method == 'POST':
      result = request.form
      print(request.form)
      result=result.to_dict(flat=False)
      # print(result['발매일'])


      date = result['발매일'][0].split('/')
      dateToday = datetime.date(int(date[2]), int(date[0]), int(date[1]))
      toOrdinal = dateToday.toordinal()  

      date = result['주문일'][0].split('/')
      dateToday = datetime.date(int(date[2]), int(date[0]), int(date[1]))
      toOrdinal2 = dateToday.toordinal()

      time = toOrdinal2 - toOrdinal
      print(toOrdinal2)
      test = pd.DataFrame({'Order_date':toOrdinal2,
                           'Retail_Price':result['소매가'],
                                 'time_gap': time,                                 
                                 'Sneaker_Name_Adidas Yeezy Boost':0.0,
                                 'Sneaker_Name_Air Jordan 1':0.0,
                                 'Sneaker_Name_Nike Air Force':0.0,
                                 'Sneaker_Name_Nike Air Max':0.0,
                                 'Sneaker_Name_Nike Air Presto':0.0,
                                 'Sneaker_Name_Nike Air VaporMax':0.0,
                                 'Sneaker_Name_Nike Blazer Mid':0.0,
                                 'Sneaker_Name_Nike React Hyperdunk':0.0,
                                 'Sneaker_Name_Nike Zoom Fly':0.0,
                                 'Brand_Adidas':0.0,
                                 'Brand_Jordan':0.0,
                                 'Brand_Nike':0.0,                                 
                                 })
      print('여기')
      lists = ['Brand_Adidas','Brand_Jordan'	,'Brand_Nike']                       
      list2 = [ 'Sneaker_Name_Adidias Yeezy Boost', 'Sneaker_Name_Air Jordan 1', 'Sneaker_Name_Nike Air Force', 'Sneaker_Name_Nike Air Max', 'Sneaker_Name_Nike Air Presto', 'Sneaker_Name_Nike Air VaporMax','Sneaker_Name_Nike Blazer Mid', 'Sneaker_Name_Nike React Hyperdunk', 'Sneaker_Name_Nike Zoom Fly']             
      for i in lists:
         if result['브랜드'][0] == i:
            test[result['브랜드']] = 1.0
            print(i)
            break

      for j in list2:
         if result['상품명'][0] == j:
            test[result['상품명']] = 1.0
            print(i)
            break
      # student_card = pd.DataFrame({'Retail_Price':result['Retail_Price'],
      #                            'Shoe_Size':result['Shoe_Size'],
      #                            'time_gap':result['time_gap'],
      #                            'adidas':result['adidas'],#10개
      #                            'boost':result['boost'],
      #                            '350':result['350'],
      #                            'yeezy':result['yeezy'],
      #                            'v2':result['v2'],
      #                            'white':result['white'],
      #                            'off':result['off'],
      #                            'nike':result['nike'],
      #                            'air':result['air'],
      #                            'blue':result['blue']})

      # X_tests_encoded = encoder.transform(student_card)  
      pd.set_option('display.max_columns', 20)
      print(test)
      result2=int(boosting.predict(test))#-int(result['소매가'][0])
      
      return render_template("cover.html",result = result2)
      
if __name__ == "__main__":
    app.run(debug=True)
