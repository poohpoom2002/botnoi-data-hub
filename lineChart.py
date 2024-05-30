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
import calendar

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
        df_pay_droped = df_pay.drop(columns=['qrcode' ,'transactionid', 'actual_time'	,'sale_code_name'	, 'package_sub','ref1',	'action'	,'subscription',	'sub_id'])

        df_pay_droped = df_pay_droped.astype(str) 

        df_pay_droped['datetime'] = pd.to_datetime(df_pay_droped['datetime'])
        df_pay_droped['price'] = df_pay_droped['price'].astype(float)
        df_pay_droped['point'] = df_pay_droped['point'].astype(float)

        df_pay_droped = df_pay_droped[(df_pay_droped.datetime > '2024-01-01 00:00:00') & (df_pay_droped.status == 'True')]

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

        return df_pay_droped 
    
    except Exception as e:
        print(e)
#---------------- start here ----------------
def plot_revenue_trend(df, period):
    df['datetime'] = pd.to_datetime(df['datetime'])
    df['price'] = df['price'].astype(float)

    if period == 'Quarter':
        df['quarter'] = df['datetime'].dt.to_period('Q')
        df['quarter_label'] = df['quarter'].apply(lambda x: f"Quarter {x.quarter} {x.year}")

        quarterly_revenue = df.groupby('quarter')['price'].sum().reset_index()
        quarterly_revenue = quarterly_revenue.merge(df[['quarter', 'quarter_label']].drop_duplicates(), on='quarter', how='left')

    
        fig = px.line(quarterly_revenue, x='quarter_label', y='price', title='Quarterly Revenue Trend',
                  labels={'quarter_label': 'Quarter', 'price': 'Total Revenue'},
                  markers=True, text='price')
    
        fig.update_layout(xaxis=dict(tickformat="%Y-Q%q"))
        fig.update_traces(texttemplate='%{text:,.2f}', textposition='top center', 
                      hovertemplate='Quarter: %{x}<br>Total Revenue: %{y:,.2f}<extra></extra>')
    elif period == 'Month':
        df['month_name'] = df['datetime'].dt.strftime('%b %Y')
        df['month_num'] = df['datetime'].dt.to_period('M')
    
        monthly_revenue = df.groupby(['month_num', 'month_name'])['price'].sum().reset_index()
        monthly_revenue = monthly_revenue.sort_values('month_num')
    
        fig = px.line(monthly_revenue, x='month_name', y='price', title='Monthly Revenue Trend',
                  labels={'month_name': 'Month', 'price': 'Total Revenue'},
                  markers=True, text='price')
    
        fig.update_layout(xaxis=dict(tickformat="%b %Y"))
        fig.update_traces(texttemplate='%{text:,.2f}', textposition='top center', 
                      hovertemplate='Month: %{x}<br>Total Revenue: %{y:,.2f}<extra></extra>')
    elif period == 'Week':
        df['week'] = df['datetime'].dt.to_period('W').astype(str)
        weekly_revenue = df.groupby('week')['price'].sum().reset_index()
        fig = px.line(weekly_revenue, x='week', y='price', title='Weekly Revenue Trend',
                  labels={'week': 'Week', 'price': 'Total Revenue'},
                  markers=True, text='price')
    
        fig.update_layout(xaxis=dict(tickformat="%Y-Q%q"))
        fig.update_traces(textposition='top center')
        fig.update_traces(texttemplate='%{text:,.2f}', textposition='top center', 
                        hovertemplate='Week: %{x}<br>Total Revenue: %{y:,.2f}<extra></extra>')
    elif period == 'Day':
        df['date_label'] = df['datetime'].dt.strftime('%Y-%m-%d')
        daily_revenue = df.groupby('date_label')['price'].sum().reset_index()
        
        fig = px.line(daily_revenue, x='date_label', y='price', title='Daily Revenue Trend',
                    labels={'date_label': 'Date', 'price': 'Total Revenue'},
                    markers=True)
        fig.update_xaxes(tickangle=45, tickformat="%Y-%m-%d", dtick='M1')
        fig.update_traces(texttemplate='%{text:,.2f}', textposition='top center', 
                        hovertemplate='Date: %{x}<br>Total Revenue: %{y:,.2f}<extra></extra>')
    return fig
#---------------- end here ----------------
connectOpenAI()
df_pay  = connectMongo()

#---------------- start here ----------------
#ฝากจัด template 
time_selectbox = st.selectbox( "select time dimension" ,
    ("Quarter","Month", "Week","Day")
)

if  time_selectbox == "Quarter":
    lineChart_fig = plot_revenue_trend(df_pay ,"Quarter")
    st.plotly_chart(lineChart_fig)
elif time_selectbox == "Month":
    lineChart_fig = plot_revenue_trend(df_pay ,"Month")
    st.plotly_chart(lineChart_fig)
elif time_selectbox == "Week":
    lineChart_fig = plot_revenue_trend(df_pay ,"Week")
    st.plotly_chart(lineChart_fig)
elif time_selectbox == "Day":
    lineChart_fig = plot_revenue_trend(df_pay ,"Day")
    st.plotly_chart(lineChart_fig)
#---------------- end here ----------------
