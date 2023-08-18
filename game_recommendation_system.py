import pandas as pd
from matplotlib import pyplot as plt
from sklearn.neighbors import NearestNeighbors
import numpy as np
import _warnings
import warnings

# Settings the warnings to be ignored
warnings.filterwarnings('ignore')
# Load your dataset
df = pd.read_csv('steam.csv', encoding='latin')

# Extract the 'tags', 'median_playtime', and 'positive_ratings' columns
tags_col = df['steamspy_tags']
playtime_col = df['median_playtime']
ratings_col = df['positive_ratings']
negative_col = df['negative_ratings']

df['ratingDiff'] = ratings_col - negative_col

# Split the tags into separate strings
tags_list = tags_col.str.split(';')

# Explode the tags list into separate rows
exploded_tags = tags_list.explode()

# Finding all the unique tags
unique_tags = exploded_tags.unique()

# Find the number of unique tags
num_unique_tags = len(exploded_tags.unique())

# Create an empty dictionary to store the games and their features
games_dict = {}

# Iterate over each row in the dataset
for idx, tags in tags_list.items():
    # Get the name of the game and its features
    game = df.loc[idx, 'name']
    playtime = df.loc[idx, 'median_playtime']
    ratings = df.loc[idx, 'ratingDiff']

    # Iterate over each tag in the tags list
    for tag in tags:
        # If the tag is not in the dictionary, create a new key
        if tag not in games_dict:
            games_dict[tag] = []

        # Add the game and its features to the list for that tag
        games_dict[tag].append((game, playtime, ratings))

# Sort the values for each tag by playtime
for tag, games in games_dict.items():
    games_dict[tag] = sorted(games, key=lambda x: x[1], reverse=True)

# Print the games for each tag sorted by playtime
# for tag, games, playtime, ratings in games_dict.items():
#     print(f"{tag}: {games} : {playtime} : {ratings}")

# Load the user dataset
df2 = pd.read_csv('steam-200k.csv')

# Extract the 'user-id', 'game-title', 'behavior-name', and 'value' columns
user_col = df2['user-id'].astype(int)
user_col2 = user_col.unique()

game_col = df2['game-title']
value_col = df2['value']

user_num = len(user_col2)

# Iterate over each row in the user dataset
games_list = []

# Create an empty dictionary to store the games for each user
user_games_dict = {}
temp = user_col[0]

# Initialize a dictionary to store the frequency of each tag
tag_freq_dict = {}

# Initialize a dictionary to store top n tags of each user
user_tags = {}

counter = 0
stop = user_num
# Iterate over each row in the dataset
# for idx, user_id in user_col.items():
#
#     # Reset user_tag frequency if user iteration changes
#     if user_id != temp:
#         # Sort the tag frequency dictionary based on values
#         user_tags[temp] = sorted(tag_freq_dict.items(), key=lambda x: x[1], reverse=True)
#         counter += 1
#
#         print(f"User {temp} done:   {counter}/{user_num}")
#         # for tag, freq in user_tags[temp]:
#         #     print(f"\t{tag}: {freq}")
#         tag_freq_dict = {}
#
#     temp = user_id
#     if counter == stop:
#         break
#     # Get the game and behavior values for the row
#     game2 = game_col[idx]
#     value = value_col[idx]
#
#     for tag, games in games_dict.items():
#         for game in games:
#             if game2 == game[0]:
#                 if tag in tag_freq_dict:
#                     tag_freq_dict[tag] += 1
#                 else:
#                     tag_freq_dict[tag] = 1
#
#         user_games_dict[user_id] = []
#         user_games_dict[user_id].append((game2, value))
#
# # Sort the values for each user by their playtime
# for user, games in user_games_dict.items():
#     user_games_dict[user] = sorted(games, key=lambda x: int(x[1]), reverse=True)

# Dict for only tag values that are already sorted
# tag_list = {}
# counter = 0
# for user in user_col2:
#     counter += 1
#     if counter == stop:
#         break
#     v = len(user_tags[user])
#     tag_list[user] = []
#     for i in range(v):
#         tag_list[user].append(user_tags[user][i][0])
#
# # Print the games for each user sorted by their playtime
# max_len = max(len(v) for v in tag_list.values())
# for k, v in tag_list.items():
#     if len(v) < max_len:
#         tag_list[k] = v + [None] * (max_len - len(v))
#
# data = pd.DataFrame(tag_list)
# data.to_excel('output.xlsx', index=False)

# Group the data by user and game, and calculate the total playtime
grouped = df2.groupby(['user-id', 'game-title'])['value'].sum().reset_index()
grouped.rename(columns={'value': 'playtime'}, inplace=True)

# Pivot the data to get a matrix of users and games
matrix = grouped.pivot(index='user-id', columns='game-title', values='playtime').fillna(0)
game_titles = list(matrix.columns)

# Train the KNN model
model = NearestNeighbors(metric='cosine', algorithm='brute', n_neighbors=5, n_jobs=-1, leaf_size=50)
model.fit(matrix)

stop = 100
game_rec = {}
totalScore = 0
precision = []
k = 10
counter = 0
# Generate recommendations for each user
for user in user_col2:
    hit = 0
    if counter == stop:
        break

    user_data = matrix.loc[user, :]
    user_data = user_data.values.reshape(1, -1)
    distances, indices = model.kneighbors(user_data, k)
    neighbors = matrix.index[indices.flatten()].tolist()
    games_played = set(matrix.columns[user_data.flatten() > 0])
    recommended_games = []
    for neighbor in neighbors:
        neighbor_games = matrix.loc[neighbor, :]
        new_games = neighbor_games[neighbor_games > 0].index
        new_games = list(new_games)
        new_games_playtime = neighbor_games[new_games]
        new_games_ratings = [games_dict[tag][0][2] for tag in tags_col if tag in games_dict for game, playtime, ratings in games_dict[tag] if game in new_games]
        new_games = [(game, playtime, ratings) for game, playtime, ratings in zip(new_games, new_games_playtime, new_games_ratings)]
        new_games = sorted(new_games, key=lambda x: (x[1], x[2]), reverse=True)
        recommended_games.extend([game for game, _, _ in new_games])
        if len(recommended_games) >= 10:
            break
    total = len(recommended_games)
    for i in games_played:
        if i in recommended_games:
            hit += 1
    if total != 0:
        precision.append((hit/total))
    else:
        precision.append(0)

    recommended_games = list(set(recommended_games))
    totalScore += precision[counter]
    counter += 1
    print(f"\nRecommendations for user {user}: {', '.join(recommended_games)}")
    print(f"Score: {precision}")

totalScore /= stop
print(f"\nAverage Hit Score: {totalScore}")

plt.figure()
plt.plot(precision, label='Hit Score')
plt.title('Nearest Neighbours: {}'.format(k))
plt.xlabel('Users Iteration')
plt.ylabel('Score')
plt.legend()
plt.show()