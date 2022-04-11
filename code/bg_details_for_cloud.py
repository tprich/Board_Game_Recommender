import numpy as np
import pandas as pd
import requests
import time
from bs4 import BeautifulSoup

# Import board game ids from cloud storage to save from uploading to virtual machine
games = pd.read_csv('https://storage.googleapis.com/bg_recommender_data/top1000_updated.csv', index_col='rank')
bg_list = list(games['id'])

api = 'https://api.geekdo.com/xmlapi2/thing'

game_dicts = []

for game in bg_list:
    params = {
        'id': game,
        'stats': 1,
        'page': 1
    }
        
    res = requests.get(api, params)
        
    if res.status_code != 200:
            print(res.status_code)
        
    soup = BeautifulSoup(res.text, 'xml')
    game_details ={
        'game_id': game,
        'game_name': soup.find('name', {'type': 'primary'})['value'],
        'game_des': soup.find('description').text,
        'game_yr_pub': int(soup.find('yearpublished')['value']),
        'min_players': int(soup.find('minplayers')['value']),
        'max_players': int(soup.find('maxplayers')['value']),
        'min_play_time': int(soup.find('minplaytime')['value']),
        'max_play_time': int(soup.find('maxplaytime')['value']),
        'min_age': int(soup.find('minage')['value']),
        'num_ratings': int(soup.find('usersrated')['value']),
        'avg_rating': float(soup.find('average')['value']),
        'bayes_avg_rating': float(soup.find('bayesaverage')['value']),
        'overall_rank_bayesavg': "|".join([soup.find('rank', {'name':'boardgame'})['value'],
                                           soup.find('rank', {'name':'boardgame'})['bayesaverage']]),
        'family_rank_bayes': '|'.join(['/'.join([row['name'], row['value'], row['bayesaverage']])
                                       for row in soup.find_all('rank', {'type':'family'})]),
        'complexity': float(soup.find('averageweight')['value']),
        'categories': '|'.join([row['value'] for row in soup.find_all('link', {'type':'boardgamecategory'})]),
        'mechanics': '|'.join([row['value'] for row in soup.find_all('link', {'type':'boardgamemechanic'})]),
        'families': '|'.join([row['value']for row in soup.find_all('link', {'type':'boardgamefamily'})]),
        'implementations': '|'.join([row['value']for row in soup.find_all('link', {'type':'boardgameimplementation'})]),
        'designers': '|'.join([row['value'] for row in soup.find_all('link', {'type':'boardgamedesigner'})]),
        'publishers': '|'.join([row['value'] for row in soup.find_all('link', {'type':'boardgamepublisher'})])
    }

    game_dicts.append(game_details)
        
    time.sleep(10)
        
    print(f'Done with {game}')

pd.DataFrame.from_dict(game_dicts).to_csv('game_details.csv', index=False)