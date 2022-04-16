# Board Game Recommender

#### [Click here to go directly to the app.](https://share.streamlit.io/tprich/board_game_recommender/main/streamlit_app/recommender_app.py)


## Do You Like Games?

One of my favorite activities is playing board games with friends and family. From cooperative games like [Betrayal at House on the Hill]( https://boardgamegeek.com/boardgame/10547/betrayal-house-hill) to everyone for themselves games like [Ticket to Ride](https://boardgamegeek.com/boardgame/9209/ticket-ride), we play them all. The problem is that after playing the same games over and over again, we want to try something new but don’t always know where to start. Do we want to choose a game based on how many people we have for the game session, or do we want to try something like what we already have played? That led me to working on this project, a board game recommender app that can give recommendations based on user reviews or by categories and features. If you like board games and want to get some ideas on what to play next, check out the app at the link above. 


## Where the Data Came From

All of the data for this project comes from [BoardGameGeek](https://boardgamegeek.com). Thank you BoardGameGeek for providing all of the data for use under the [Attribution-NonCommercial-ShareAlike 3.0 Unported license](https://creativecommons.org/licenses/by-nc-sa/3.0/). There is an API specifically for use with BoardGameGeek and it's sister sites, [RPGGeek](https://rpggeek.com/) and [VideoGameGeek](https://videogamegeek.com/). The API link is `https://api.geekdo.com/xmlapi2/thing`. Note that the link uses `xmlapi2`, which is the latest version of BoardGameGeek's API. To use it yourself, follow the instructions found [here](https://boardgamegeek.com/wiki/page/BGG_XML_API2). Make sure to follow all rules in the [terms of use](https://boardgamegeek.com/wiki/page/XML_API_Terms_of_Use#) and check out the related articles to make the API work for you. The only data that was scrapped without using the API was the name, id, and rank of the top 1,000 games. To obtain this information, a simple webscrap using Python on the [Browse](https://boardgamegeek.com/browse/boardgame) pages. Please look at [1_Data_Gathering notebook](./code/1_Data_Gathering.ipynb) for more details on the data gathering for this project.


## How the User-Based Recommender was Built

















##### Thanks again to BoardGameGeek for providing the games, reviews, and all related data under the [Attribution-NonCommercial-ShareAlike 3.0 Unported license](https://creativecommons.org/licenses/by-nc-sa/3.0/).