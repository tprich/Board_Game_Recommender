import streamlit as st
import pandas as pd
import pickle

# LOADING THE USER BASED RECOMMENDER AND GAMES DATAFRAME
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

# GAMES FILTER FUNCTION
@st.cache
def category_filter(yr='Any', play=0, ptime='Any',
                    age=0, comp=0, cat=[],
                    des=[], pubs=[], rate=6.5):
    res = games.copy()

    # Filter by categories
    if len(cat) != 0:
        for c in cat:
            res[c] = [1 if c in i else 0 for i in res['categories']]
        if len(cat) == 1:
            res = res[(res[cat[0]] == 1)]
        elif len(cat) == 2:
            res = res[(res[cat[0]] == 1) | (res[cat[1]] == 1)]
        else:
            res = res[(res[cat[0]] == 1) | (res[cat[1]] == 1) | (res[cat[2]] == 1)]

    # Filter by number of players
    if play != 0:
        if exact_play:
            res = res[(res['min_players'] == play) & (res['max_players'] == play)]
        else:
            res = res[(res['min_players'] <= play) & (res['max_players'] >= play)]
    
    # Filter by average rating
    res = res[res['avg_rating'] >= rate]
    
    # Filter by complexity
    if comp != 0:
        res = res[(res['complexity'] >= (comp - .5)) & (res['complexity'] <= (comp + .5))]
    
    # Filter by play time
    if ptime != 'Any':
        if ptime == '0 - 15 minutes':
            res = res[res['min_play_time'] <= 15]
        elif ptime == '15 - 30 minutes':
            res = res[(res['min_play_time'] > 15) & (res['min_play_time'] <= 30)]
        elif ptime == '30 - 45 minutes':
            res = res[(res['min_play_time'] > 30) & (res['min_play_time'] <= 45)]
        elif ptime == '45 - 60 minutes':
            res = res[(res['min_play_time'] > 45) & (res['min_play_time'] <= 60)]
        else:
            res = res[res['min_play_time'] > 60]
    
    # Filter by age constraint
    if age != 0:
        res = res[res['min_age'] <= age]
    
    # # Filter by year
    if yr != 'Any':
        res = res[res['game_yr_pub'] == yr]

    # Filter by designers
    if len(des) != 0:
        for c in des:
            res[c] = [1 if c in i else 0 for i in res['designers']]
        if len(des) == 1:
            res = res[(res[des[0]] == 1)]
        elif len(des) == 2:
            res = res[(res[des[0]] == 1) | (res[des[1]] == 1)]
        else:
            res = res[(res[des[0]] == 1) | (res[des[1]] == 1) | (res[des[2]] == 1)]
    
    # Filter by publishers
    if len(pubs) != 0:
        for c in pubs:
            res[c] = [1 if c in i else 0 for i in res['publishers']]
        if len(pubs) == 1:
            res = res[(res[pubs[0]] == 1)]
        elif len(pubs) == 2:
            res = res[(res[pubs[0]] == 1) | (res[pubs[1]] == 1)]
        else:
            res = res[(res[pubs[0]] == 1) | (res[pubs[1]] == 1) | (res[pubs[2]] == 1)]
            
    return res

# ESTABLISH LISTS FOR FILTER
@st.cache
def get_lists():
    categories = []
    for row in games['categories']:
        categories += row.split('|')
    
    designers = []
    for row in games['designers']:
        designers += row.split('|')

    publishers = []
    for row in games['publishers']:
        publishers += row.split('|')

    return list(sorted(set(categories))), list(sorted(set(designers))), list(sorted(set(publishers)))

cat_list, des_list, pubs_list = get_lists()

# START OF APP ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
st.title('Board Game Recommender')

st.markdown("""Welcome, and thank you for visiting my board game recommender! This app uses data on the top 1,000 board games from [boardgamegeek.com](https://boardgamegeek.com/) (as of March 16th, 2022) to give recommendations 3 different ways. Select an option from the side panel to get started!""")


recom_select = st.sidebar.radio(
    'Pick how you want to get your recommendations',
    ('Based on a game.', 'Explore by filtering features.')) # Add back in 'Choose a game and then filter by features.',

# Based on a game
if recom_select == 'Based on a game.':  # use or to show both?
    st.markdown("""For this option, select a board game and you will get recommendations based on over 11 million user reviews to give the best matches.""")

    st.header('Enter a board game:')

    option = st.selectbox(label = 'Type or select a board game:', options=games['game_name'].sort_values())
    res = query_tool(option)

    if st.button('Recommendations Please!'):
        st.markdown(f'##### People who enjoyed {option} also enjoyed:')
        for i in range(10):
            st.markdown(f"""[{res['game_name'][i]}](https://boardgamegeek.com/boardgame/{res['game_id'][i]})""")

# # Choose a game and then filter by features.
# elif recom_select == 'Choose a game and then filter by features.':
#     st.write('Update in Progress')

# Explore by filtering features.
elif recom_select == 'Explore by filtering features.':
    st.markdown('For this recommender, select the game features that you want to filter by. Please note that you will get games that match your selections exactly, so you may end up with no results. If that happens, try expanding your selection criteria.')

    # Select categories
    cat=[]
    if st.checkbox('Categories'): 
        cat = st.multiselect(
            'Select up to 3 Categories that you are interested in:',
            cat_list, key=str)
        if len(cat) > 3:
            st.warning('Only select 3 Categories.')

    # Number of players
    play=0
    if st.checkbox('Number of Players'):
        exact_play = st.checkbox('Only show games with exact number of players (i.e. 2-player only games, etc.)')
        play = st.number_input('Enter the minimum number of players:',
        step=1, min_value=1)
        

    # Select rating
    rate = 6.5
    if st.checkbox('Minimum Rating'):
        rate = st.number_input('Set the minimum rating for the game: ',
        step=.5, min_value=6.5)

    # Select Complexity
    comp = 0
    if st.checkbox('Weight'):
        comp = st.slider('''Select weight 
        (recommendations will be within 0.5 of weight):''',
        1.0, 5.0, 1.0, .1)
        if comp < 2.0:
            st.caption('Easy: Beginner friendly and easy to pick up and learn')
        if comp < 3.0 and comp >= 2.0:
            st.caption('Moderate: Getting more complex and can be mildly difficult to set up and play for new players.')
        if comp < 4.0 and comp >= 3.0:
            st.caption('Hard: Complex and can be difficult to pick up and learn. Usually more involved set up.')
        if comp <= 5.0 and comp >= 4.0:
            st.caption('Difficult: The most involved games that take some time to learn and set up. Also tend to be longer games.')

    # Select Play time
    ptime = 'Any'
    if st.checkbox('Minimum Play Time'):
        ptime = st.selectbox(
            'Specify a minimum play time range:',
            ('0 - 15 minutes', '15 - 30 minutes', '30 - 45 minutes',
            '45 - 60 minutes', 'More than 60 minutes'))

    # Select age constraint
    age = 0
    if st.checkbox('Age Constraint'):
        age = st.number_input('Select the max player age:',
        step=1, min_value=4, max_value=100)

    # Select year
    yr = 'Any'
    if st.checkbox('Year Published'):
        yr = st.selectbox('Specify a year:',
        list(sorted(set(games['game_yr_pub']), reverse=True)))

    # Select designers
    des = []
    if st.checkbox('Game Designer(s)'):
        des = st.multiselect(
            'Select up to 3 Designers that you are interested in:',
            des_list, key=str)
        if len(des) > 3:
            st.warning('Only select 3 Designers.')
    # Select publishers
    pubs = []
    if st.checkbox('Game Publisher(s)'):
        pubs = st.multiselect(
            'Select up to 3 Publishers that you are interested in:',
            pubs_list, key=str)
        if len(pubs) > 3:
            st.warning('Only select 3 Publishers.')

    if st.button('Recommendations Please!'):
        filtered = category_filter(yr, play, ptime, age, comp, cat, des, pubs, rate).reset_index()
        if len(filtered.index) == 0:
            st.warning('Sorry, no board games in this recommender match all of your selections. Please adjust your filters and try again.')
        elif len(filtered.index) < 10:
            st.markdown('##### Based on your selections, you may want to try:')
            for i in range(len(filtered.index)):
                st.markdown(f"""[{filtered['game_name'][i]}](https://boardgamegeek.com/boardgame/{filtered['game_id'][i]})""")
        else:
            st.markdown('##### Your top 10 results to try are:')
            for i in range(10):
                st.markdown(f"""[{filtered['game_name'][i]}](https://boardgamegeek.com/boardgame/{filtered['game_id'][i]})""")
            st.markdown('Your filters returned more than 10 results. Try using more filters to narrow down your results more.')

st.markdown('##')
st.markdown('##')
st.markdown("""Thanks to BoardGameGeek for providing the games, reviews, and all related data under the [Attribution-NonCommercial-ShareAlike 3.0 Unported license](https://creativecommons.org/licenses/by-nc-sa/3.0/).""")