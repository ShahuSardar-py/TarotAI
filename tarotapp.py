import pandas as pd
import streamlit as st
import random 
import datetime 
import os
import json 
from google import genai
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv("GAPI"))
st.set_page_config(page_icon='🔮', 
                   page_title='TarotAI',
                   layout='centered')

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
    prompt=f"""You are a tarot reader. The user has drawn the "{card_name}"
        for a question about {category}.
        Give a short, insightful tarot reading based on this  (3–4 sentences),
        mystical in tone but meaningful and personal.
        """
    response = client.models.generate_content(
         model="gemini-2.0-flash",
         contents=prompt
        )
    return response.text.strip()

focus= st.selectbox(
       "Area of focus:",
        ["General", "Relationship", "Career", "Decisions", "Health"]
)
if st.button("reveal"):
       card, ori= Magic()
       st.subheader(card["name"])
       st.write(f"**Arcana:** {card['arcana']}")
       st.write(f"**Meaning ({ori}):** {card[ori]}")
       st.write(f"YOU READING FOR {focus}")
       with st.spinner("Connecting to the universe..."):
        reading = GenMeaning(card, focus)
        st.write(reading)
