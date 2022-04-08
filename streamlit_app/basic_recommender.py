import streamlit as st
import numpy as np
import pandas as pd
import pickle

# Load Recommender
st.cache
def get_recommender():
    with open('streamlit_app/recommender.pkl', 'rb') as f:
        recommender = pickle.load(f)
    return recommender

recom = get_recommender()

games = pd.read_csv('streamlit_app/top1000_updated.csv', index_col='rank')

# QUERY TOOL
@st.cache
def query_tool(query):
    for title in recom.columns:
        if query.lower() in title.lower():
            recs = pd.DataFrame(recom[title].sort_values(ascending=False)[1:11])
            return pd.merge(recs, games, left_on=recs.index, right_on='title', how='left')

# START OF APP
st.title('Board Game Recommender')

st.markdown("""Welcome! This board game recommender uses the top 1,000 board games according to [boardgamegeek.com](https://boardgamegeek.com/) (as of March 16th, 2022) and provides you with the top 10 recommended boardgames to try. This recommender is based on user reviews to give the best matches for you.""")

st.header('Enter a board game:')

option = st.selectbox(label = 'Type or select a board game:', options=games['title'])
res = query_tool(option)

if st.button('Recommendations Please!'):
    st.markdown(f"""[{res['title'][0]}](https://boardgamegeek.com/boardgame/{res['id'][0]})""")
    st.markdown(f"""[{res['title'][1]}](https://boardgamegeek.com/boardgame/{res['id'][1]})""")
    st.markdown(f"""[{res['title'][2]}](https://boardgamegeek.com/boardgame/{res['id'][2]})""")
    st.markdown(f"""[{res['title'][3]}](https://boardgamegeek.com/boardgame/{res['id'][3]})""")
    st.markdown(f"""[{res['title'][4]}](https://boardgamegeek.com/boardgame/{res['id'][4]})""")
    st.markdown(f"""[{res['title'][5]}](https://boardgamegeek.com/boardgame/{res['id'][5]})""")
    st.markdown(f"""[{res['title'][6]}](https://boardgamegeek.com/boardgame/{res['id'][6]})""")
    st.markdown(f"""[{res['title'][7]}](https://boardgamegeek.com/boardgame/{res['id'][7]})""")
    st.markdown(f"""[{res['title'][8]}](https://boardgamegeek.com/boardgame/{res['id'][8]})""")
    st.markdown(f"""[{res['title'][9]}](https://boardgamegeek.com/boardgame/{res['id'][9]})""")


st.markdown("""Thanks to BoardGameGeek for providing the games, reviews, and all related data under the [Attribution-NonCommercial-ShareAlike 3.0 Unported license](https://creativecommons.org/licenses/by-nc-sa/3.0/).""")