import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
import csv

# Load gameData and userTags csv files into dataframes
df = pd.read_csv('gameData.csv', encoding='latin')
df2 = pd.read_csv('userTags.csv')
user_col = df['user-id']
rating = df['rating']

avg_hit = [0.92, 0.4497, 0.3638, 0.3328, 0.3139]
avg_hit2 = [0.79, 0.7339, 0.699, 0.6756, 0.6420]
x = [1, 3, 5, 7, 10]
plt.figure()
plt.plot(x,avg_hit, label='System 1')
plt.plot(x, avg_hit2, label='System 2')
plt.title('Average Step Score ')
plt.xlabel('Nearest Neighbour K')
plt.ylabel('Score')
plt.legend()
plt.show()
user_col = user_col.unique()

# Delete 128470551 from user_col because doesn't exist in userTags dataset
user_col = np.delete(user_col, np.where(user_col == 128470551))

# create an empty dictionary to store the normalized values
data_dict = {}

values = df['value']

# normalize the values using MinMaxScaler
scaler = MinMaxScaler()
values_norm = scaler.fit_transform(values.values.reshape(-1, 1))

# convert the normalized data back to the original scale
values_orig = scaler.inverse_transform(values_norm)

# populate the dictionary with the normalized values
for i, user_id in enumerate(user_col):
    data_dict[user_id] = values_orig[i][0]

# Picking the top 5 tags
n = 5
game_tags_dict = {}

with open('userTags.csv', 'r') as csv_file:
    cv = csv.reader(csv_file)
    next(cv)  # skip the first row
    for row in cv:
        user_id = int(row[0])
        game_tags = tuple(filter(None, row[1:n+1]))
        game_tags_dict[user_id] = game_tags

user_preferences = {}

import csv

data_dict = {}

with open('user_pref.csv') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)  # skip header row

    for row in reader:
        user_id = int(row[0])
        top_categories = eval(row[1])
        most_played_publisher = row[2]
        most_played_platform = row[3]
        average_spending = float(row[4])
        favorite_tags = eval(row[5])

        user_data = {
            'top_categories': top_categories,
            'most_played_publisher': most_played_publisher,
            'most_played_platform': most_played_platform,
            'average_spending': average_spending,
            'favorite_tags': favorite_tags
        }

        data_dict[user_id] = user_data
# print the preferences for all users in the dictionary
# for user_id, preferences in user_preferences.items():
#     print(f"User ID: {user_id}")
#     print(f"Top 3 most played categories: {preferences['top_categories']}")
#     print(f"Top 3 most played publishers: {preferences['most_played_publisher']}")
#     print(f"Average price paid: {preferences['avg_price']}")
#     print(f"Top 5 preferred game tags: {game_tags_dict[user_id]}\n")

# Use this if user_pref.csv hasn't been created
# loop through each user's history
# for user_id in df['user-id'].unique():
#
#     if user_id == 128470551:
#         continue
#     # create a subset of the data for this user
#     user_data = df[df['user-id'] == user_id]
#
#     # calculate the top 3 most played categories for this user
#     categories_count = user_data['categories'].str.split(';').apply(pd.Series).stack().value_counts()
#     top_categories = categories_count.head(3).index.tolist()
#
#     # calculate the most played publisher for this user
#     if not user_data.groupby('publisher')['name'].count().empty:
#         most_played_publisher = user_data.groupby('publisher')['name'].count().idxmax()
#     else:
#         most_played_publisher = None
#
#     # calculate the most played platform for this user
#     if not user_data.groupby('platforms')['name'].count().empty:
#         most_played_platform = user_data.groupby('platforms')['name'].count().idxmax()
#     else:
#         most_played_platform = None
#
#     # calculate the average price paid by this user
#     avg_price = user_data['price'].mean()
#
#     # add this user's preferences to the dictionary
#     user_preferences[user_id] = {'top_categories': top_categories,
#                                  'most_played_publisher': most_played_publisher,
#                                  'most_played_platform': most_played_platform,
#                                  'avg_price': avg_price,
#                                  'game_tags': game_tags_dict[user_id]}
#
# with open('user_pref.csv', 'w', newline='') as csvfile:
#     # Create a CSV writer object
#     writer = csv.writer(csvfile)
#
#     # Write the header row
#     writer.writerow(['User ID', 'Top Categories', 'most_played_publisher', 'most_played_platform', 'Average Price', 'Game Tags'])
#
#     # Write the data rows
#     for user_id, data in user_preferences.items():
#         writer.writerow([user_id, data['top_categories'], data['most_played_publisher'], data['most_played_platform'], data['avg_price'], data['game_tags']])





