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




st.markdown("<h5 style='font-weight: bold;'>Result</h5>",unsafe_allow_html=True)

