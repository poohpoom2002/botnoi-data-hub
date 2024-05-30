import os
import streamlit as st
from streamlit_option_menu import option_menu
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import pandas as pd
from pandasai import SmartDataframe, SmartDatalake
import cv2
import hashlib
import plotly.express as px
import plotly.graph_objects as go
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

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
        df_message = pd.DataFrame(paymentdb.message.find())

        df_pay_droped = df_pay.drop(columns=['qrcode' ,'transactionid', 'actual_time'	,'sale_code_name'	, 'package_sub','ref1',	'action'	,'subscription',	'sub_id'])
        df_message_droped = df_message.drop(columns=[ 'url', 'audio_id', 'page'])

        df_pay_droped = df_pay_droped.astype(str)
        df_message_droped = df_message_droped.astype(str) 

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

        df_message_droped['datetime'] = pd.to_datetime(df_message_droped['datetime'])
        df_message_droped['count'] = df_message_droped['count'].astype(float)

        df_message_droped = df_message_droped[(df_message_droped.datetime > '2024-01-01 00:00:00') & (df_message_droped.channel == 'download')]
        df_message_droped.rename(columns={'count': 'point'}, inplace=True)
        df_message_droped['provider'].fillna('web', inplace=True)

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

        return df_pay_droped.astype(str), df_message_droped.astype(str)
    
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
        fig.update_layout(
            plot_bgcolor='white',
            paper_bgcolor='white',
            xaxis=dict(
                showgrid=True,
                gridcolor='rgba(200, 200, 200, 0.5)',
                title=dict(font=dict(color='black'))
            ), 
            yaxis=dict(
                showgrid=True,
                gridcolor='rgba(200, 200, 200, 0.5)',
            ),
            margin=dict(l=40, r=40, t=40, b=40)
        )
                          
    elif period == 'Today Income' :
        current_datetime = pd.Timestamp.now()
        daily_date = current_datetime.strftime("%Y-%m-%d")
        current_day = pd.to_datetime(daily_date)
        df['datetime'] = pd.to_datetime(df['datetime'])
        df_today = df[df['datetime'].dt.date == current_day.date() - pd.Timedelta(days=1)]
        df_today['hour'] = df_today['datetime'].dt.hour
        hourly_income = df_today.groupby('hour')['price'].sum().reset_index()
        fig = px.line(hourly_income, x='hour', y='price', markers=True, title=f'Hourly Income for {(current_day - pd.Timedelta(days=1)).date()}', labels={'hour': 'Hour of the Day', 'price': 'Income'})
        fig.update_traces(text=hourly_income['price'], textposition='top center', line_color = "#1474cd")
        fig.update_layout(
            plot_bgcolor='white',
            paper_bgcolor='white',
            xaxis=dict(
                showgrid=True,
                gridcolor='rgba(200, 200, 200, 0.5)',
                title=dict(font=dict(color='black'))
            ),
            yaxis=dict(
                showgrid=True,
                gridcolor='rgba(200, 200, 200, 0.5)',
                title=dict(font=dict(color='black'))
            ),
            margin=dict(l=40, r=40, t=40, b=40)
        )
        
    elif period == 'Yesterday Income' :
        current_datetime = pd.Timestamp.now()
        daily_date = current_datetime.strftime("%Y-%m-%d")
        current_day = pd.to_datetime(daily_date)
        df['datetime'] = pd.to_datetime(df['datetime'])
        df_today = df[df['datetime'].dt.date == current_day.date()]
        df_today['hour'] = df_today['datetime'].dt.hour
        hourly_income = df_today.groupby('hour')['price'].sum().reset_index()
        fig = px.line(hourly_income, x='hour', y='price', markers=True, title=f'Hourly Income for {(current_day).date()}', labels={'hour': 'Hour of the Day', 'price': 'Income'})
        fig.update_traces(text=hourly_income['price'], textposition='top center', line_color = "#1474cd")
        fig.update_layout(
            plot_bgcolor='white',
            paper_bgcolor='white',
            xaxis=dict(
                showgrid=True,
                gridcolor='rgba(200, 200, 200, 0.5)',
                title=dict(font=dict(color='black'))
            ),
            yaxis=dict(
                showgrid=True,
                gridcolor='rgba(200, 200, 200, 0.5)',
                title=dict(font=dict(color='black'))
            ),
            margin=dict(l=40, r=40, t=40, b=40)
        )

    return fig

def to_smartDataLake(df_pay, df_message) :
    df_lake = SmartDatalake([df_pay, df_message])
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

    return fig

def VisualizeTransaction(user_id, df_pay):
      # Filter for the specific user
    user_transactions = df_pay[df_pay['user_id'] == user_id]

  # Group by year, month, and package_id to get the count of packages and sum of prices
    package_counts = user_transactions.groupby(['Year', 'Month', 'package_id']).size().reset_index(name='package_count')
    monthly_transactions = user_transactions.groupby(['Year', 'Month']).agg(
        total_price=('price', 'sum'),
        unique_packages=('package_id', 'nunique')
    ).reset_index()

  # Create a DataFrame with all months of the year
    years = monthly_transactions['Year'].unique()
    all_months = pd.DataFrame([(year, month) for year in years for month in range(1, 13)], columns=['Year', 'Month'])

  # Merge with monthly transactions to fill missing months
    user_transactions_filled = all_months.merge(monthly_transactions, on=['Year', 'Month'], how='left').fillna({'total_price': 0, 'unique_packages': 0})
    user_transactions_filled['user_id'] = user_id  # Add user_id column

  # Create a new column for easier plotting
    user_transactions_filled['YearMonth'] = user_transactions_filled['Year'].astype(str) + '-' + user_transactions_filled['Month'].astype(str).str.zfill(2)

  # Plotting the total price using Plotly
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=user_transactions_filled['YearMonth'],
        y=user_transactions_filled['total_price'],
        marker=dict(
            color=user_transactions_filled['total_price'],
            colorscale='deep'  # Use the built-in Viridis colorscale
        ),
        name='Total Price'
    ))

  # Update layout for better visuals
    fig.update_layout(
        title=f'Monthly Total Transaction of User {user_id}',
        xaxis_title='Year-Month',
        yaxis_title='Total Price',
        xaxis_tickangle=-45,
        xaxis=dict(
            tickmode='array',
            tickvals=user_transactions_filled['YearMonth'],
            ticktext=user_transactions_filled['YearMonth']
        ),
        template='plotly_white'
    )

    return fig

def ShowBoughtPack(user_id, df_pay):
    user_transactions = df_pay[df_pay['user_id'] == user_id]
    package_counts = user_transactions.groupby('package_id').size().reset_index(name='package_count')

  # Assign numerical values for color mapping
    package_counts['color_value'] = package_counts['package_id'].factorize()[0]

  # Enhanced Plotly Visualization with 'deep' colorscale
    fig = px.bar(package_counts, x='package_id', y='package_count',
                title=f'Packages Bought by User {user_id}',
                labels={'package_id': 'Package ID', 'package_count': 'Number Purchased'},
                color='color_value',                   # Use numerical color values
                color_continuous_scale='deep',         # Apply 'deep' colorscale
                text='package_count')

  # Remove the color bar (not needed for categorical data)
    fig.update_layout(coloraxis_showscale=False)

  # Customization (Optional)
    fig.update_layout(xaxis_title='Package ID', yaxis_title='Number Purchased')

    return fig

def VisualizePointUsage(user_id, df_msg):
    user_point = df_msg[df_msg['user_id'] == user_id]

  # Group by user, year, and month to get the sum of points
    monthly_point = user_point.groupby(['user_id', 'Year', 'Month'])['point'].sum().reset_index()

  # Create a DataFrame with all months of the year
    years = user_point['Year'].unique()
    all_months = pd.DataFrame([(year, month) for year in years for month in range(1, 13)], columns=['Year', 'Month'])

  # Merge with user transactions to fill missing months
    user_point_filled = all_months.merge(monthly_point, on=['Year', 'Month'], how='left').fillna({'point': 0})
    user_point_filled['user_id'] = user_id  # Add user_id column

  # Create a new column for easier plotting
    user_point_filled['YearMonth'] = user_point_filled['Year'].astype(str) + '-' + user_point_filled['Month'].astype(str).str.zfill(2)

  # Plotting the total points using Plotly
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=user_point_filled['YearMonth'],
        y=user_point_filled['point'],
        marker=dict(color=user_point_filled['point'], colorscale='Deep'),
        name='Total Points'
    ))

  # Update layout for better visuals
    fig.update_layout(
        title=f'Monthly Point Usage of User {user_id}',
        xaxis_title='Year-Month',
        yaxis_title='Total Points',
        xaxis_tickangle=-45,
        xaxis=dict(
            tickmode='array',
            tickvals=user_point_filled['YearMonth'],
            ticktext=user_point_filled['YearMonth']
        ),
        template='plotly_white'
    )

    return fig

def feature_eng(df_pay,df_msg) :
    datetime_Jan_24 = '2024-01-01 00:00:00'
    true_transac = df_pay[(df_pay['status'] == True)& ((df_pay.datetime >= datetime_Jan_24))]
    true_transac.price = pd.to_numeric(true_transac.price, errors='coerce')

    sum_transac = true_transac.groupby('user_id')['price'].sum().reset_index().rename(columns={'price': 'sum_price'})
    msg_count = pd.DataFrame(df_msg[df_msg['datetime'] >= datetime_Jan_24]['user_id'].value_counts()).astype(int)
    msg_count.drop('guest', inplace = True)

    merged_df = pd.merge(sum_transac, msg_count,  on='user_id', how='left')
    merged_df.fillna(0, inplace=True)
    merged_df.columns = ['user_id', 'sum_price', 'number_of_uses']

    true_transac['price'] = pd.to_numeric(true_transac['price'])
    average_payout = true_transac.groupby('user_id')['price'].mean().reset_index()
    average_payout.columns = ['user_id', 'avg_price']
    average_payout['avg_price'] = average_payout['avg_price'].round(2)

    freq_tranc = pd.DataFrame(true_transac['user_id'].value_counts()).reset_index()
    frequency_df = true_transac.groupby('user_id').size().reset_index(name='Frequency')
    frequency_df['Frequency'].max()
    freq_tranc.columns = ['user_id', 'freq_tranc']

    true_transac['datetime'] = pd.to_datetime(true_transac['datetime'])
    first_last_transactions = true_transac.groupby('user_id')['datetime'].agg(['min', 'max']).reset_index()
    first_last_transactions.columns = ['user_id', 'first_transaction', 'last_transaction']

    min_max = true_transac.groupby('user_id')['price'].agg(['min', 'max']).reset_index()

    current_datetime = pd.Timestamp.now()

    formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
    today = pd.to_datetime(formatted_datetime)
    first_last_transactions['recency'] = (today - first_last_transactions['last_transaction']).dt.days

    merge_frequen = pd.merge(merged_df, freq_tranc,  on='user_id', how='left')
    merge_avg = pd.merge(merge_frequen, average_payout,  on='user_id', how='left')
    merge_date = pd.merge(merge_avg, first_last_transactions,  on='user_id', how='left')
    cdp = pd.merge(merge_date, min_max,  on='user_id', how='left')

    cdp['Sum_Score'] = pd.qcut(cdp['sum_price'], q=4, labels=False) + 1
    cdp['Mean_Score'] = pd.qcut(cdp['avg_price'], q=4, labels=False) + 1
    cdp['Min_Score'] = pd.qcut(cdp['min'], q=4, labels=False) + 1
    cdp['Max_Score'] = pd.qcut(cdp['max'], q=4, labels=False) + 1

    cdp['M_Score'] = (cdp['Sum_Score'] + cdp['Mean_Score'] + cdp['Min_Score'] + cdp['Max_Score']) / 4
    cdp['R_Score'] = pd.qcut(cdp['recency'], q=4, labels=False) + 1
    cdp['F_Score'] = pd.qcut(cdp['freq_tranc'], q=4, labels=False, duplicates='drop') + 1

    return cdp

def quartile_cdp(cdp) :
    X = cdp[['M_Score', 'R_Score']]

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    pca = PCA(n_components=2)
    X_pca = pca.fit_transform(X_scaled)

    n_clusters = 4
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    cdp['Cluster'] = kmeans.fit_predict(X_scaled)

    cdp['Cluster'] = cdp['Cluster'].replace({ 0 : 'ลูกค้าประจำ ใช้งานบ่อย แต่เติมไม่เยอะมาก', 1 : 'ลูกค้าชั้นดี เติมเยอะและยังใช้งานอยู่ ', 2 : 'ลูกค้าที่หายไปนาน ยอดเติมเงินน้อย', 3 : 'ลูกค้าที่มียอดเติมเงินเยอะ แต่หายไปนาน'})

    return cdp

def cdp_searcher(cdp, user_id) :
    cluster = cdp[cdp['user_id'] == user_id]['Cluster']
    return cluster
  
connectOpenAI()
df_pay, df_message = connectMongo()
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
    ("Quarter","Month", "Week", "Daily income for this year", "Daily income for this month", "Today Income", "Yesterday Income")
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

st.markdown("<h1 class='Top_title'>Heatmap</h1>", unsafe_allow_html=True)
df_lake = to_smartDataLake(df_pay  , df_message)

# UI
st.title("Test show Graphs")

#import data form mongoDB test checked !
#st.dataframe(df_pay.head(10))
#st.dataframe(df_personalForm.head(10))
#st.dataframe(df_message.head(10))

heatmap_fig = create_heatmap(df_pay, 2024)
st.plotly_chart(heatmap_fig)

st.markdown("<h1 class='Top_title'>Visualize User Data</h1>", unsafe_allow_html=True)
chart_selectbox = st.selectbox( "Select visualization you interested in" ,
    ("Transaction", "Packages_Bought", "Point_Usage")
)
visualization_user_id = st.text_area("Enter user id")

if  chart_selectbox == "Transaction":
    transaction_chart = VisualizeTransaction(visualization_user_id ,df_pay)
    st.plotly_chart(transaction_chart)
elif  chart_selectbox == "Packages_Bought":
    package_bought_chart = ShowBoughtPack(visualization_user_id ,df_pay)
    st.plotly_chart(package_bought_chart)
elif  chart_selectbox == "Point_Usage":
    point_usage_chart = VisualizePointUsage(visualization_user_id ,df_pay)
    st.plotly_chart(point_usage_chart)

st.markdown("<h1 class='Top_title'>User Clustering</h1>", unsafe_allow_html=True)

user_id = st.text_area("Enter ID")
cdp = feature_eng(df_pay, df_message)
cluster = cdp_searcher(cdp, user_id)
st.write(cluster)

prompt = st.text_area("Enter your prompt")

st.markdown("<h1 class='Top_title'>Let’s explore Insights with PandasAI</h1>", unsafe_allow_html=True)
st.write("PandasAI is an advanced tool that integrates artificial intelligence capabilities with the Pandas library, enabling users to analyze data more efficiently. Users can prompt in natural language to analyze data directly !")
st.markdown("<h5 style='font-weight: bold;'>Enter your prompt</h5>",unsafe_allow_html=True)

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