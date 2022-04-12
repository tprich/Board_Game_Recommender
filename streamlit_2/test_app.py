import streamlit as st
import pandas as pd

df = pd.read_csv('test.csv')

# Create recommender
@st.cache
def category_filter(yr, play, ptime, age, comp, rate):
    res = df.copy()
    if yr != 'N/A':
        res = res[res['game_yr_pub'] == yr]
    if play != 0:
        res = res[(res['min_players'] <= play) & (res['max_players'] >= play)]
    if ptime != 'Any':
        if ptime == '0 - 15':
            res = res[res['min_play_time'] <= 15]
        elif ptime == '15 - 30':
            res = res[(res['min_play_time'] > 15) & (res['min_play_time'] <= 30)]
        elif ptime == '30 - 45':
            res = res[(res['min_play_time'] > 30) & (res['min_play_time'] <= 45)]
        elif ptime == '45 - 60':
            res = res[(res['min_play_time'] > 45) & (res['min_play_time'] <= 60)]
        else:
            res = res[res['min_play_time'] > 60]
    if age != None:
        res = res[res['min_age'] <= age]
    if rate != None:
        res = res[res['avg_rating'] >= rate]
    if comp != None:
        res = res[(res['complexity'] >= (comp - .5)) & (res['complexity'] <= (comp + .5))]
    return res

# Create App
st.title('This is a test')

# Select year
yr = st.selectbox(
     'Select A Year?',
     ['N/A']+list(sorted(set(df['game_yr_pub']), reverse=True)))

# Select number of players
play = st.number_input('Specific number of players in mind? Leave at 0 for any number of players.', step=1, min_value=0)

# Set length of game
ptime = None

# Age constraint
age = None

# Complexity range
comp = None

# Rating minimum
rate = None

recom = category_filter(yr, play, ptime, age, comp, rate)