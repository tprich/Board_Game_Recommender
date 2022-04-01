import numpy as np
import pandas as pd
import requests
import time
from bs4 import BeautifulSoup
from itertools import count
import os

api = 'https://api.geekdo.com/xmlapi2/thing'

bg_top = pd.read_csv('bg_top1000.csv')
bg_list = list(bg_top['id'])
bg_list

for game in bg_list:
    if not os.path.exists(f'{game}_ratings.csv'):
        user_ratings = []
        for i in count():
            page = i+1

            params = {
                'id': game,
                'ratingcomments': '1',
                'page': page,
                'pagesize': 100
            }

            res = requests.get(api, params)

            if res.status_code != 200:
                print(f'Error code {res.status_code} for game id: {game}')

            soup = BeautifulSoup(res.text, 'xml')

            if len(soup.find('comments').find_all('comment')) < 1:
                time.sleep(7)
                break

            for comment in soup.find('comments').find_all('comment'):
                user_rate ={
                    'user_id': comment['username'],
                'rating': comment['rating'],
                'game_id': game
                }

                user_ratings.append(user_rate)

            time.sleep(7)

        pd.DataFrame.from_dict(user_ratings).to_csv(f'{game}_ratings.csv')
        print(f'Done with {game}')

print('Done with all games')