import streamlit as st
import numpy as np
import pandas as pd

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
