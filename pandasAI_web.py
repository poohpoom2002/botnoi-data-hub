import os
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import pandas as pd
import streamlit as st
from pandasai import SmartDataframe
from pandasai.llm.openai import OpenAI
import matplotlib.pyplot as plt

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
  
connectOpenAI()
sdf = connectMongo()

st.title("Your Data Analysis")
''' We are connected with voicebot data from mongoDB already !!'''
prompt = st.text_area("Enter your prompt")

if st.button("Generate"):
    if prompt:
        with st.spinner("Generating Response..."):
            response = sdf.chat(prompt)
            #st.success(response)
            st.write(response)
            
            if "plot" in response:
                fig, ax = plt.subplots()
                # Generate plot (assuming the response object has the required data and method)
                sdf.plot(ax=ax)
                st.pyplot(plt.gcf())
    else:
        st.warning("Please enter a prompt")

