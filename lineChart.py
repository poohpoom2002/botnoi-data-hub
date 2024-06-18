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
    elif period == 'Daily income for this year':
        df['date_label'] = df['datetime'].dt.strftime('%Y-%m-%d')
        daily_revenue = df.groupby('date_label')['price'].sum().reset_index()
        
        fig = px.line(daily_revenue, x='date_label', y='price', title='Daily Revenue Trend',
                    labels={'date_label': 'Date', 'price': 'Total Revenue'},
                    markers=True)
        fig.update_xaxes(tickangle=45, tickformat="%Y-%m-%d", dtick='M1')
        fig.update_traces(texttemplate='%{text:,.2f}', textposition='top center', 
                        hovertemplate='Date: %{x}<br>Total Revenue: %{y:,.2f}<extra></extra>')
        
    elif period == 'Daily income for this month' :
        current_datetime = pd.Timestamp.now()
        this_month = int(current_datetime.strftime("%m"))
        df['datetime'] = pd.to_datetime(df['datetime'])
        df_month = df[df['datetime'].dt.month == this_month]
        df_month['day'] = df_month['datetime'].dt.day
        daily_income = df_month.groupby('day')['price'].sum().reset_index()
        fig = px.line(daily_income, x='day', y='price', markers=True, title='Daily Income Over Time', labels={'day': 'Date', 'price': 'Income'})
        fig.update_traces(text=daily_income['price'], textposition='top center', line_color = "#1474cd")
        fig.update_layout(plot_bgcolor='white',paper_bgcolor='white', xaxis=dict(showgrid=True, gridcolor='rgba(200, 200, 200, 0.5)', title=dict(font=dict(color='black'))), 
                          yaxis=dict(showgrid=True,gridcolor='rgba(200, 200, 200, 0.5)', margin=dict(l=40, r=40, t=40, b=40)))
                          
    elif period == 'Today Income' :
        current_datetime = pd.Timestamp.now()
        daily_date = current_datetime.strftime("%Y-%m-%d")
        current_day = pd.to_datetime(daily_date)
        df['datetime'] = pd.to_datetime(df['datetime'])
        df_today = df[df['datetime'].dt.date == current_day.date() - pd.Timedelta(days=1)]
        df_today['hour'] = df_today['datetime'].dt.hour
        hourly_income = df_today.groupby('hour')['price'].sum().reset_index()
        fig = px.line(hourly_income, x='hour', y='price', markers=True, title=f'Hourly Income for {(current_day - pd.Timedelta(days=1)).date()}', labels={'hour': 'Hour of the Day', 'price': 'Income'})
        fig.update_traces(text=daily_income['price'], textposition='top center', line_color = "#1474cd")
        fig.update_layout(plot_bgcolor='white',paper_bgcolor='white',xaxis=dict(showgrid=True, gridcolor='rgba(200, 200, 200, 0.5)', title=dict(font=dict(color='black'))),
                          yaxis=dict(showgrid=True, gridcolor='rgba(200, 200, 200, 0.5)', title=dict(font=dict(color='black'))),margin=dict(l=40, r=40, t=40, b=40))
        
    elif period == 'Yesterday Income' :
        current_datetime = pd.Timestamp.now()
        daily_date = current_datetime.strftime("%Y-%m-%d")
        current_day = pd.to_datetime(daily_date)
        df['datetime'] = pd.to_datetime(df['datetime'])
        df_today = df[df['datetime'].dt.date == current_day.date()]
        df_today['hour'] = df_today['datetime'].dt.hour
        hourly_income = df_today.groupby('hour')['price'].sum().reset_index()
        fig = px.line(hourly_income, x='hour', y='price', markers=True, title=f'Hourly Income for {(current_day).date()}', labels={'hour': 'Hour of the Day', 'price': 'Income'})
        fig.update_traces(text=daily_income['price'], textposition='top center', line_color = "#1474cd")
        fig.update_layout(plot_bgcolor='white',paper_bgcolor='white',xaxis=dict(showgrid=True, gridcolor='rgba(200, 200, 200, 0.5)', title=dict(font=dict(color='black'))),
                          yaxis=dict(showgrid=True, gridcolor='rgba(200, 200, 200, 0.5)', title=dict(font=dict(color='black'))),margin=dict(l=40, r=40, t=40, b=40))
    return fig
#---------------- end here ----------------
connectOpenAI()
df_pay  = connectMongo()

#---------------- start here ----------------
#ฝากจัด template 
time_selectbox = st.selectbox( "select time dimension" ,
    ("Quarter","Month", "Week","Daily income for this year","Daily income for this month","Today Income", "Yesterday Income")
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
elif time_selectbox == "Daily income for this year":
    lineChart_fig = plot_revenue_trend(df_pay ,"Daily income for this year")
    st.plotly_chart(lineChart_fig)
elif time_selectbox == "Daily income for this month":
    lineChart_fig = plot_revenue_trend(df_pay ,"Daily income for this month")
    st.plotly_chart(lineChart_fig)
elif time_selectbox == "Today Income":
    lineChart_fig = plot_revenue_trend(df_pay ,"Today Income")
    st.plotly_chart(lineChart_fig)
elif time_selectbox == "Yesterday Income":
    lineChart_fig = plot_revenue_trend(df_pay ,"Yesterday Income")
    st.plotly_chart(lineChart_fig)


#---------------- end here ----------------