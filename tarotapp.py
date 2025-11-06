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

def set_bg(image_file):
    with open(image_file, "rb") as f:
        img_data = f.read()
    b64_img = base64.b64encode(img_data).decode()

    bg_css = f"""
    <style>
    .stApp {{
        background-image: url("data:image/jpg;base64,{b64_img}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
        position: relative;
    }}
    /* Blurred translucent overlay */
    .stApp::before {{
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0, 0, 0, 0.45); /* darkness level */
        backdrop-filter: blur(8px);
        z-index: 0;
    }}
    /* Keep actual app content above overlay */
    .stApp > div:first-child {{
        position: relative;
        z-index: 1;
    }}
    </style>
    """
    st.markdown(bg_css, unsafe_allow_html=True)

set_bg("/images/bg.jpg")


@st.cache_data
def load_cards():
    with open('cardData.json',mode='r', encoding='utf-8') as f:
              return json.load(f)
    
cards= load_cards()

#selction of card
def Magic():
      today= datetime.date.today().isoformat()
      random.seed(today + str(datetime.datetime.now().second))
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


#app ui
st.title("Celestia 🔮")
st.caption("Your personalized daily tarot reader")
st.divider()
st.caption("Its best to pick only one card in a day as its based on your first intution and thus the first reading is the one universe has chosen :) ")
st.write("Select what type of reading you need from the drop down given below. Keep the question in mind and click :red[Pick My Card].")
focus= st.selectbox(
       "Reading about:",
        ["General", "Relationship", "Career", "Life Decisions", "Health"]
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


#sponsor button
st.markdown(
    """
    <div style='text-align: center; margin-top: 30px;'>
        <a href="https://buymeacoffee.com/shahusardag" target="_blank"
           style="background-color:#FFDD00; color:#000; padding:10px 20px; 
                  border-radius:10px; text-decoration:none; font-weight:bold;">
           ☕ Buy me a coffee
        </a>
    </div>
    """,
    unsafe_allow_html=True
)

with st.expander("How this works"):
     st.write('''Celestia is built on the same deck of 78 traditional tarot cards that readers have used for centuries.
Each time you visit, the app shuffles the entire deck and then seeds the selection with today’s date — tying your draw to the day’s unique energies. The card you receive is your reading for this moment.

Once drawn, an AI tarot reader interprets your card in context with your chosen focus — be it love, career, or clarity — weaving meaning from both intuition and data.

🔮 Disclaimer: Celestia doesn’t claim absolute accuracy or predict the future. Think of it as a mirror — a small ritual to align your thoughts, lift your spirit, and tune in to your energy for the day.''')


