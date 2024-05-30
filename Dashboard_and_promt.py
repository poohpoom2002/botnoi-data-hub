import os
import streamlit as st
from streamlit_option_menu import option_menu
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import pandas as pd
from pandasai import SmartDataframe
import cv2
import hashlib

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
        df = pd.DataFrame(paymentdb.payment.find())
        df_str = df.astype(str)
        sdf = SmartDataframe(df_str)
        return sdf
    except Exception as e:
        print(e)

    paymentdb = client['prod-tts-payment']

def connectOpenAI() :
    os.environ["PANDASAI_API_KEY"] = "$2a$10$vdsfzU0rvW1vs8v1G/aMjebe.k5HuuOi3tftrf0E7c.XWH9wknn4a"

def calculate_file_hash(file_path):
    with open(file_path, "rb") as f:
        file_hash = hashlib.sha256(f.read()).hexdigest()
    return file_hash
  
connectOpenAI()
sdf = connectMongo()

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
st.sidebar.markdown("<h5 class='lower_title'>Website to help you analyze data from Botnoi Voice with ease and convenience. We have successfully connected to the database!</h5>", unsafe_allow_html=True)

selected = st.sidebar.selectbox(
    "Choose an option",
    ["Dashboard and prompt", "About Dataset"],
    key="sidebar_option",
    format_func=lambda x: x.replace("_", " ").title(),
)

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

st.markdown(page_style, unsafe_allow_html=True)
st.markdown("<h1 class='Top_title'>Botnoi Voice Dashboard</h1>", unsafe_allow_html=True)
st.write("This dashboard showcases key data on Botnoi Voice, including revenue trends and voice download statistics, providing a clear view of financial performance and user engagement.")


# dashboard




st.subheader("Our most recent top 10 highest paying customers")


# 10 highest paying customers

st.subheader("Dashboard showing customer behavior")



# customer behavior



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