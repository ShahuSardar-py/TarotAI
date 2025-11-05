import pandas as pd
import streamlit as st
import random 
import datetime 
import os
import json 
from google import genai
from dotenv import load_dotenv
import base64
load_dotenv()
client = genai.Client(api_key=os.getenv("GAPI"))
#UI setup 
st.set_page_config(page_icon='🔮', 
                   page_title='Celestia',
                   layout='centered')
# Background image setup
def set_bg(image_file):
    with open(image_file, "rb") as f:
        img_data = f.read()
    b64_img = base64.b64encode(img_data).decode()
    bg_css = f"""
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{b64_img}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    </style>
    """
    st.markdown(bg_css, unsafe_allow_html=True)

set_bg("D:/TarotReaderAI/images/bg.jpg")


@st.cache_data
def load_cards():
    with open('cardData.json',mode='r', encoding='utf-8') as f:
              return json.load(f)
    
cards= load_cards()

def Magic():
      today= datetime.date.today().isoformat()
      random.seed(today)
      random.shuffle(cards)
      card= random.choice(cards)
      ori= random.choice(["upright", 'reversed'])
      return card, ori

def GenMeaning(card_name, category):
    card_name = card["name"]
    prompt=f"""You are a seasoned tarot reader with lot of expirince. The user has drawn the "{card_name}"
        for a question about {category}.
        Give a short, insightful tarot reading based on this  (5-6 sentences), be raw and real about it. based on the category, keep the reading genric but personalized. 
        
        """
    response = client.models.generate_content(
         model="gemini-2.0-flash",
         contents=prompt
        )
    return response.text.strip()



st.title("Celestia 🔮")
st.caption("Your personalized daily tarot reader")
st.divider()

st.write("Select what type of reading you need from the drop down given below. Keep the question in mind and click :red[Choose Card].")
focus= st.selectbox(
       "Reading about:",
        ["General", "Relationship", "Career", "Decisions", "Health"]
)
DOR= datetime.date.today().isoformat()
if st.button("Pick My Tarot Card"):
       card, ori= Magic()
       st.toast("You've picked your card!")
       st.subheader(card["name"])

       with st.expander(f"Get your reading for {DOR}"):
        with st.spinner("Connecting to the universe..."):
             reading = GenMeaning(card, focus)
             st.write(reading)

st.caption("Its best to pick only one card in a day as its based on your first intution and thus the first reading is the one universe has chosen :) ")