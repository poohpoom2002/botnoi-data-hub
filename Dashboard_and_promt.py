import os
import streamlit as st
from streamlit_option_menu import option_menu
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import pandas as pd
from pandasai import SmartDataframe
import cv2
import hashlib
import plotly.express as px

@st.cache_resource
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

        return df_pay_droped.astype(str)
    
    except Exception as e:
        print(e)

def connectOpenAI() :
    os.environ["PANDASAI_API_KEY"] = "$2a$10$vdsfzU0rvW1vs8v1G/aMjebe.k5HuuOi3tftrf0E7c.XWH9wknn4a"

def calculate_file_hash(file_path):
    with open(file_path, "rb") as f:
        file_hash = hashlib.sha256(f.read()).hexdigest()
    return file_hash

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
  
connectOpenAI()
df_pay  = connectMongo()
sdf = SmartDataframe(df_pay)

sidebar_style = """
    <style>
    [data-testid="stSidebar"] {
        background-color: #532457;
    }
    .sidebar_title {
        font-size: 50px !important;
        font-weight: bold;
        color: white;
        text-shadow: 
            -2px -2px 0 #000,  
             2px -2px 0 #000,
            -2px  2px 0 #000,
             2px  2px 0 #000;
        padding: 20px;
    }
    .lower_title {
        font-size: 16px !important;
        font-weight: thin !important;
        color: white;
        padding: 10px;
    }
    .sidebar-option {
        padding: 10px;
        background-color: #754a6b;
        color: white;
        text-align: center;
        border-radius: 5px;
        margin-bottom: 5px;
        font-weight: bold;
        cursor: pointer;
    }
    .sidebar-option:hover {
        background-color: #86567b;
    }
    .sidebar-option-selected {
        background-color: #3f1f45 !important;
    }
    </style>
"""

st.markdown(sidebar_style, unsafe_allow_html=True)
st.sidebar.markdown("<h1 class='sidebar_title'>Botnoi <br> Data Hub</h1>", unsafe_allow_html=True)
st.sidebar.markdown("<h5 class='lower_title'>Website to help you analyze data from Botnoi Voice with ease and convenience!</h5>", unsafe_allow_html=True)

# selected = st.sidebar.selectbox(
#     "Choose an option",
#     ["Dashboard and prompt", "About Dataset"],
#     key="sidebar_option",
#     format_func=lambda x: x.replace("_", " ").title(),
# )

selectbox_style = """
    <style>
    .stSelectbox [data-baseweb="select"] {
        background-color: #532457;
        color: white;
        font-weight: bold;
    }
    .stSelectbox [data-baseweb="select"] .css-1g6gooi {
        color: white;
    }
    .stSelectbox [data-baseweb="select"] .css-14el2xx {
        background-color: #3f1f45;
    }
    .stSelectbox [data-baseweb="select"] .css-1inwz65 {
        background-color: #3f1f45;
    }
    .stSelectbox [data-baseweb="select"]:hover .css-1inwz65 {
        background-color: #86567b;
    }
    </style>
"""
st.markdown(selectbox_style, unsafe_allow_html=True)

# if selected == "Dashboard and prompt":
#     # st.title("Dashboard and prompt")
# elif selected == "About Dataset":
#     # st.title("About Dataset")

page_style = """
    <style>
    [data-testid="stSidebar"]={
        background-color = white;
    }
    .Top_title{
        font-size: 50px !important;
        font-weight: thin;
        color: black;
        padding: -100px;
    }
    </style>
"""

st.markdown("<h1 class='Top_title'>Data Visualization</h1>", unsafe_allow_html=True)
st.write("Transforms your data into interactive visualizations, allowing you to select time ranges and create a variety of graph types for detailed analysis and presentation.")
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

st.markdown("<h1 class='Top_title'>Let’s explore Insights with PandasAI</h1>", unsafe_allow_html=True)
st.write("PandasAI is an advanced tool that integrates artificial intelligence capabilities with the Pandas library, enabling users to analyze data more efficiently. Users can prompt in natural language to analyze data directly !")
st.markdown("<h5 style='font-weight: bold;'>Enter your prompt</h5>",unsafe_allow_html=True)
prompt = st.text_area("Enter your prompt")

if st.button("Generate"):
    if prompt:
        last_graph = calculate_file_hash('./exports/charts/temp_chart.png')
        with st.spinner("Generating Response..."):
            response = sdf.chat(prompt)
            #st.success(response)
            st.markdown("<h5 style='font-weight: bold;'>Result</h5>",unsafe_allow_html=True)
            new_graph = calculate_file_hash('./exports/charts/temp_chart.png')
    
            if last_graph != new_graph:
                try:
                    graph = cv2.imread('./exports/charts/temp_chart.png')
                    st.image(graph, caption=response)
                except FileNotFoundError:
                    st.error("The plot image was not found.")
            else:
                st.write(response)
    else:
        st.warning("Please enter a prompt")