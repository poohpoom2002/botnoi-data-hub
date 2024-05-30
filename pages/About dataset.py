import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd

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

# Custom styled title in the sidebar
st.sidebar.markdown("<h1 class='sidebar_title'>Botnoi <br> Data Hub</h1>", unsafe_allow_html=True)

# Custom text in the sidebar
st.sidebar.markdown("<h5 class='lower_title'>Website to help you analyze data from Botnoi Voice with ease and convenience!</h5>", unsafe_allow_html=True)

# Custom option menu in the sidebar
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
#     st.title("Dashboard and prompt")
# elif selected == "About Dataset":
#     st.title("About Dataset")

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

st.title("Get to know about Dataset ")
st.write("The data used in the program comes exclusively from the prod-tts-payment database. You can read the variables within the table and find their definitions below")

# payment
st.markdown("""
    <style>
    .big-font {
        font-size:25px !important;
        font-weight: bold;
    }
    </style>
    <p class="big-font">Payment data</p>
    """, unsafe_allow_html=True)
paymentData = {
    'feature name': ['_id','user_id','package_id','price','datetime','status','point','promotion'],
    'Description': ['Unique identifier from MongoDB','Unique identifier for the user','Identifier for the purchased packag','Amount paid','Date and time of the transaction','Status of the transaction','Points earned from the transaction','Promotion code used']
}
df = pd.DataFrame(paymentData)
st.write("The payment Data table is designed to store and describe essential details related to transactions. Each entry in the table includes a unique identifier, user information, package details, transaction specifics, and promotional data. This structure helps in tracking and analyzing payment activities and user interactions with different packages and promotions.")
st.dataframe(df)

# Personal form
st.markdown("""
    <style>
    .big-font {
        font-size:25px !important;
        font-weight: bold;
    }
    </style>
    <p class="big-font">Personal form data</p>
    """, unsafe_allow_html=True)

personalData = {
    'feature name': ['_id','user_id','fullname','age','gender','province','career','use_for','get_by'],
    'Description': ['Unique identifier for each record in the database','Unique identifier for the user','Full name of the user', 'Age of the user','Gender of the user','Province where the user resides','Career of the user','Purpose for which the service/product is used','Introduction Channel']
}
df = pd.DataFrame(personalData)
st.write("The personal Data table is intended to store user information collected from a form. Each entry includes unique identifiers, personal details such as full name, age, gender, and location, as well as career information and how the user learned about the product or service. This data helps in understanding the user demographics and their interaction with the product.")
st.dataframe(df)

# Message
st.markdown("""
    <style>
    .big-font {
        font-size:25px !important;
        font-weight: bold;
    }
    </style>
    <p class="big-font">Message data</p>
    """, unsafe_allow_html=True)
messageData = {
    'feature name': ['_id','user_id','message','datetime','channel','count','provider','language'],
    'Description': ['Unique identifier from MongoDB', 'Unique identifier for the user','Message content',' Date and time of the transaction','Communication channel',' Number of occurrences','Service provider','Language of the message']
}
df = pd.DataFrame(messageData)
st.write("The message Data table is used to track the messages and voice selections made by users. Each entry contains a unique identifier, user information, message content, timestamp, communication channel, number of occurrences, service provider, and the language of the message. This data helps in analyzing user preferences and interactions with the messaging system.")
st.dataframe(df)
