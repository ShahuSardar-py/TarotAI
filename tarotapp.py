import pandas as pd
import streamlit as st
import random 
import datetime 
import os
import json 

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

if st.button("reveal"):
       card, ori= Magic()
       st.subheader(card["name"])
       st.write(f"**Arcana:** {card['arcana']}")
       st.write(f"**Meaning ({ori}):** {card[ori]}")