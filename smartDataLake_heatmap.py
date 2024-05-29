import streamlit as st
import numpy as np
import pandas as pd
from pandasai import SmartDataframe , SmartDatalake
import os
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from pandasai.llm.openai import OpenAI
import plotly.express as px
import numpy as np

@st.cache_resource
def connectOpenAI() :
    os.environ["PANDASAI_API_KEY"] = "$2a$10$HBNWVPYc6w3.8DLvRU4g1ePESJ7NgUiI0eIPd8vIsqhLMhnFhNxIy"

def connectMongo() :
    uri = "mongodb+srv://kong:2GgNZ7V0V0q5Go9d@botnoivoiceprod.f4igi.mongodb.net/?retryWrites=true&readPreference=secondary&readPreferenceTags=nodeType:ANALYTICS&w=majority&appName=botnoivoiceprod"
    # Create a new client and connect to the server
    client = MongoClient(uri, server_api=ServerApi('1'))
    # Send a ping to confirm a successful connection
    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
        paymentdb = client['prod-tts-payment']

        df_pay = pd.DataFrame(paymentdb.payment.find())
        #df_personalForm = pd.DataFrame(paymentdb.personal_form.find())
        df_message = pd.DataFrame(paymentdb.message.find())

        df_message_droped = df_message.drop(columns=[ 'url', 'audio_id', 'page'])
        #df_personalForm_droped = df_personalForm.drop(columns=['accept' , 'feedback' ,  'feedback_comment' , 'advice' ])
        df_pay_droped = df_pay.drop(columns=['qrcode' ,'transactionid', 'actual_time'	,'sale_code_name'	, 'package_sub','ref1',	'action'	,'subscription',	'sub_id'])

        df_message_droped = df_message_droped.astype(str) 
        #df_personalForm_droped  = df_personalForm_droped.astype(str) 
        df_pay_droped = df_pay_droped.astype(str) 

        df_pay_droped['datetime'] = pd.to_datetime(df_pay_droped['datetime'])
        df_message_droped['datetime'] = pd.to_datetime(df_message_droped['datetime'])

        df_message_droped['count'] = df_message_droped['count'].astype(float)
        df_pay_droped['price'] = df_pay_droped['price'].astype(float)
        df_pay_droped['point'] = df_pay_droped['point'].astype(float)

        #df_pay_droped = df_pay_droped[df_pay_droped['status'] == 'True']
        df_pay_droped = df_pay_droped[(df_pay_droped.datetime > '2024-01-01 00:00:00') & (df_pay_droped.status == 'True')]
        df_message_droped = df_message_droped[(df_message_droped.datetime > '2024-01-01 00:00:00') & (df_message_droped.channel == 'download')]
        df_message_droped.rename(columns={'count': 'point'}, inplace=True)
        df_message_droped['provider'].fillna('web', inplace=True)

        df_pay_droped['Year'] = df_pay_droped['datetime'].dt.year
        df_pay_droped['Month'] = df_pay_droped['datetime'].dt.month
        df_pay_droped['Week'] = df_pay_droped['datetime'].dt.isocalendar().week
        df_pay_droped['Day'] =df_pay_droped['datetime'].dt.day
        df_pay_droped['Hour'] = df_pay_droped['datetime'].dt.hour
        df_pay_droped['Day_of_Week'] =df_pay_droped['datetime'].dt.day_name()
        df_pay_droped['Year'] = df_pay_droped['Year'].astype('Int32')
        df_pay_droped['Month'] = df_pay_droped['Month'].astype('Int32')
        df_pay_droped['Week'] = df_pay_droped['Week'].astype('Int32')
        df_pay_droped['Day'] = df_pay_droped['Day'].astype('Int32')
        df_pay_droped['Hour'] = df_pay_droped['Hour'].astype('Int32')

        df_message_droped['Year'] = df_message_droped['datetime'].dt.year
        df_message_droped['Month'] = df_message_droped['datetime'].dt.month
        df_message_droped['Week'] = df_message_droped['datetime'].dt.isocalendar().week
        df_message_droped['Day'] = df_message_droped['datetime'].dt.day
        df_message_droped['Hour'] = df_message_droped['datetime'].dt.hour
        df_message_droped['Day_of_Week'] = df_message_droped['datetime'].dt.day_name()

        df_message_droped['Year'] = df_message_droped['Year'].astype('Int32')
        df_message_droped['Month'] = df_message_droped['Month'].astype('Int32')
        df_message_droped['Week'] = df_message_droped['Week'].astype('Int32')
        df_message_droped['Day'] = df_message_droped['Day'].astype('Int32')
        df_message_droped['Hour'] = df_message_droped['Hour'].astype('Int32')

        return df_pay  , df_message_droped
    
    except Exception as e:
        print(e)

def to_smartDataLake(df_pay , df_message) :
    df_lake = SmartDatalake([df_pay , df_message])
    return df_lake

def create_heatmap(dataframe, year):
    dataframe['datetime'] = pd.to_datetime(dataframe['datetime'])
     # Filter data for the specified year
    df_thisYear = dataframe[dataframe['datetime'].dt.year == year]

    # Create additional columns for grouping data
    df_thisYear['month'] = df_thisYear['datetime'].dt.strftime('%B')
    df_thisYear['day'] = df_thisYear['datetime'].dt.day

    # เรียงลำดับแกน y เพื่อให้เรียงตามเดือนจริง ๆ
    months_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    df_thisYear['month'] = pd.Categorical(df_thisYear['month'], categories=months_order, ordered=True)

    # Convert the price to integers
    df_thisYear['price'] = df_thisYear['price'].astype(float)

    # Pivot table เพื่อสร้างเมทริกซ์สำหรับ heatmap
    heatmap_data = df_thisYear.pivot_table(index='month', columns='day', values='price', aggfunc='sum')

    # สร้าง heatmap โดยใช้ Plotly Express และแสดงตัวเลขในแต่ละเซลล์
    fig = px.imshow(heatmap_data, 
                    labels={'x': 'Day', 'y': 'Month', 'color': 'Summery Price'},
                    x=heatmap_data.columns, 
                    y=heatmap_data.index, 
                    title='Heatmap of Summary Price In 2024',
                    text_auto=True,
                    color_continuous_scale='Purples')  
    fig.update_xaxes(side="top")  
    #fig.show() 
    return fig

#set up
connectOpenAI()
df_pay , df_message  = connectMongo()
df_lake = to_smartDataLake(df_pay  , df_message)

# UI
st.title("Test show Graphs")

#import data form mongoDB test checked !
#st.dataframe(df_pay.head(10))
#st.dataframe(df_personalForm.head(10))
#st.dataframe(df_message.head(10))

heatmap_fig = create_heatmap(df_pay,2024)
st.plotly_chart(heatmap_fig)
