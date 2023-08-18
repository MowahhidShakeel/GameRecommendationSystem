import pandas as pd
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')
import seaborn as sns
import numpy as np
import json
import warnings
import xlsxwriter as xl
warnings.filterwarnings('ignore')
import base64
import io
from matplotlib.pyplot import imread
import codecs
from IPython.display import HTML


def binary(genre_list):
    binaryList = []

    for genre in genreList:
        if genre in genre_list:
            binaryList.append(1)
        else:
            binaryList.append(0)

    return binaryList


def binary2(categ_list):
    binaryList = []
    for direct in categList:
        if direct in categ_list:
            binaryList.append(1)
        else:
            binaryList.append(0)
    return binaryList


# Load the dataset
df = pd.read_csv('steam.csv', encoding='latin')
df2 = pd.read_csv('steam-200k.csv')
print(df2.describe())
# Drop all rows with value of "purchase" in the "behavior-name" column
df2 = df2[df2['behavior-name'] != 'purchase']

# Drop the last column of df2
df2 = df2.drop(columns=df2.columns[-1])

df = df.merge(df2, left_on='name', right_on='game-title', how='right')

# Drop all rows where "appid" is empty
df = df[df['appid'].notna()]

# Removing unnecessary columns
# Drop the "appid", "english", "required_age", and "achievements" columns
df = df.drop(columns=['appid', 'english', 'required_age', 'achievements', 'behavior-name', 'game-title'])

# Creating a rating difference column
df['rating_difference'] = df['positive_ratings'] - df['negative_ratings']
plt.subplots(figsize=(12, 10))
rating = df['rating_difference']

# Creating a seperate file with the newly created df which can be used in other codes as well
# filename = 'so58326392.xlsx'
# sheetname = 'mySheet'
# with pd.ExcelWriter(filename) as writer:
#     if not df.index.name:
#         df.index.name = 'Index'
#     df.to_excel(writer, sheet_name=sheetname)
#
# import openpyxl
#
# wb = openpyxl.load_workbook(filename=filename)
# tab = openpyxl.worksheet.table.Table(displayName="df", ref=f'A1:{openpyxl.utils.get_column_letter(df.shape[1])}{len(df) + 1}')
# wb[sheetname].add_table(tab)
# wb.save(filename)

ax = pd.Series(rating).value_counts()[:10].sort_values(ascending=True).plot.barh(width=0.9, color=sns.color_palette('hls', 10))
for i, v in enumerate(pd.Series(rating).value_counts()[:10].sort_values(ascending=True).values):
    ax.text(.8, i, v, fontsize=12, color='white', weight='bold')
plt.title('Most Liked Games')
plt.show()

df['steamspy_tags'] = df['steamspy_tags'].str.split(';')

# Finding out the most popular genre
plt.subplots(figsize=(12, 10))
list1 = []
for i in df['steamspy_tags']:
    list1.extend(i)
ax = pd.Series(list1).value_counts()[:10].sort_values(ascending=True).plot.barh(width=0.9, color=sns.color_palette('hls', 10))
for i, v in enumerate(pd.Series(list1).value_counts()[:10].sort_values(ascending=True).values):
    ax.text(.8, i, v, fontsize=12, color='white', weight='bold')
plt.title('Top Genres')
plt.show()

# Creating a list of unique genres
genreList = []
for index, row in df.iterrows():
    genres = row["steamspy_tags"]

    for genre in genres:
        if genre not in genreList:
            genreList.append(genre)

# Creating One Hot Encoding for genres
df['genres_bin'] = df['steamspy_tags'].apply(lambda x: binary(x))

df['categories'] = df['categories'].str.split(';')
# Finding out the most popular categories
plt.subplots(figsize=(12, 10))
list2 = []
for i in df['categories']:
    list2.extend(i)
ax = pd.Series(list2).value_counts()[:10].sort_values(ascending=True).plot.barh(width=0.9, color=sns.color_palette('hls', 10))
for i, v in enumerate(pd.Series(list2).value_counts()[:10].sort_values(ascending=True).values):
    ax.text(.8, i, v, fontsize=12, color='white', weight='bold')
plt.title('Popular Categories')
plt.show()

# Creating One Hot Encoding for categories

for index, row in df.iterrows():
    categories = row["categories"]
categList = []
for i in categories:
    if i not in categList:
        categList.append(i)

df['categ_bin'] = df['categories'].apply(lambda x: binary2(x))


# # Most Popular games
# plt.subplots(figsize=(12,10))
# list1=[]
# list1 = df['name']
# ax=pd.Series(list1).value_counts()[:15].sort_values(ascending=True).plot.barh(width=0.9,color=sns.color_palette('muted',40))
# for i, v in enumerate(pd.Series(list1).value_counts()[:15].sort_values(ascending=True).values):
#     ax.text(.8, i, v,fontsize=10,color='white',weight='bold')
# plt.title('Top 15 Most Downloaded Games')
#
# # Games with the highest average playtime
# game_playtime = df.groupby('name')['average_playtime'].mean()
# game_playtime_list = [(game, playtime) for game, playtime in game_playtime.items()]
#
# # Sort the game_playtime_list based on the second element (i.e., the playtime) in descending order
# game_playtime_list_sorted = sorted(game_playtime_list, key=lambda x: x[1], reverse=True)
#
# # Select the top N games with the highest average playtime
# top_n = 15
# top_games = [x[0] for x in game_playtime_list_sorted[:top_n]]
# top_playtimes = [x[1] for x in game_playtime_list_sorted[:top_n]]
#
# # Plot the top games and their average playtime using a bar plot
# plt.figure(figsize=(12, 8))
# plt.barh(top_games, top_playtimes, color=sns.color_palette('pastel', top_n))
# plt.xlabel('Average Playtime (minutes)')
# plt.title('Top {} Games with the Highest Average Playtime'.format(top_n))
# plt.show()
