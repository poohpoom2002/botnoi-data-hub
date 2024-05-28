import streamlit as st
from streamlit_option_menu import option_menu

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
st.sidebar.markdown("<h5 class='lower_title'>Website to help you analyze data from Botnoi Voice with ease and convenience. We have successfully connected to the database!</h5>", unsafe_allow_html=True)

# Custom option menu in the sidebar
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

st.markdown(page_style, unsafe_allow_html=True)
st.markdown("<h1 class='Top_title'>Get to know about Dataset </h1>", unsafe_allow_html=True)
st.write("The data used in the program comes exclusively from the prod-tts-payment database. You can read the variables within the table and find their definitions below.")


st.markdown("<h5 style='font-weight: bold;'>Payment</h5>",unsafe_allow_html=True)


st.markdown("<h5 style='font-weight: bold;'>Personal form</h5>",unsafe_allow_html=True)


st.markdown("<h5 style='font-weight: bold;'>Message</h5>",unsafe_allow_html=True)
