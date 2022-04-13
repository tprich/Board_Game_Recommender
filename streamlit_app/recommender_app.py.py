import streamlit as st
import pandas as pd
import pickle

# Loading User Review Based Recommender and Games Data Frame
@st.cache
def get_recommender():
    with open('streamlit_app/recommender.pkl', 'rb') as f:
        recommender = pickle.load(f)
    games = pd.read_csv('streamlit_app/games_final.csv', index_col='rank')
    return recommender, games

user_rec, games = get_recommender()

# QUERY TOOL
@st.cache
def query_tool(query):
    for title in user_rec.columns:
        if query.lower() in title.lower():
            recs = pd.DataFrame(user_rec[title].sort_values(ascending=False)[1:11])
            return pd.merge(recs, games, left_on=recs.index, right_on='game_name', how='left')


st.title('Board Game Recommender')

st.markdown("""Welcome, and thank you for visiting my board game recommender! This app uses data on the top 1,000 board games from [boardgamegeek.com](https://boardgamegeek.com/) (as of March 16th, 2022) to give recommendations 3 different ways. Select an option from the side panel to get started!""")


option = st.sidebar.radio(
    'Pick how you want to get your recommendations',
    ('Based on a game.', 'Choose a game and then filter by features.', 'Explore by filtering features.'))

# Based on a game
if option == 'Based on a game.':
    st.markdown("""For this option, select a board game and you will get recommendations based on over 11 million user reviews to give the best matches.""")

    st.header('Enter a board game:')

    option = st.selectbox(label = 'Type or select a board game:', options=games['game_name'].sort_values())
    res = query_tool(option)

    if st.button('Recommendations Please!'):
        for i in range(10):
            st.markdown(f"""[{res['game_name'][i]}](https://boardgamegeek.com/boardgame/{res['game_id'][i]})""")

# Choose a game and then filter by features.
elif option == 'Choose a game and then filter by features.':
    st.write('Update in Progress')

# Explore by filtering features.
elif option == 'Explore by filtering features.':
    st.write('Update in Progress')











st.markdown("""Thanks to BoardGameGeek for providing the games, reviews, and all related data under the [Attribution-NonCommercial-ShareAlike 3.0 Unported license](https://creativecommons.org/licenses/by-nc-sa/3.0/).""")