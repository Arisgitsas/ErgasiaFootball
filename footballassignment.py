import sqlite3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sb




con = sqlite3.connect('C:/Users/arisg/Desktop/database.sqlite')

#check if connection works by asking for all tables
tables = pd.read_sql("""SELECT name
                        FROM sqlite_master
                        WHERE type='table';""", con)
tables
df_teams = pd.read_sql_query(
    "SELECT * FROM Team;", con)
df_teams.head()
df_teamattr = pd.read_sql_query(
    "SELECT * FROM Team_Attributes;", con)
df_teamattr.head()
df_matchscores = pd.read_sql_query(
    "SELECT id, country_id, league_id, season, match_api_id, home_team_api_id, away_team_api_id, home_team_goal, away_team_goal FROM Match;", con)
#pass the matchscore in a file
df_matchscores.head()
df_match_players = pd.read_sql_query(
    "SELECT id, season, home_team_api_id, away_team_api_id, home_player_1, home_player_2, home_player_3, home_player_4, home_player_5, home_player_6, home_player_7, home_player_8, home_player_9, home_player_10, home_player_11, away_player_1, away_player_2, away_player_3, away_player_4, away_player_5, away_player_6, away_player_7, away_player_8, away_player_9, away_player_10, away_player_11 FROM Match;", con)
df_match_players.tail()
#get players for home_teams per season
df_players_home_season = df_match_players[['home_team_api_id', 'season', 'home_player_1', 'home_player_2', 'home_player_3', 'home_player_4', 'home_player_5', 'home_player_6', 'home_player_7', 'home_player_8', 'home_player_9', 'home_player_10', 'home_player_11']]

#pivot the table and drop the null values for players
df_players_home_season = pd.melt(df_players_home_season, id_vars=['home_team_api_id', 'season'], var_name='position', value_name='player').dropna()

#change columnname
df_players_home_season.rename(columns={'home_team_api_id': 'team_api_id'}, inplace=True)
#drop column position
df_players_home_season.drop(columns=['position'], inplace=True)
#since players play more than one match in a season we need to remover duplicates
df_players_home_season=df_players_home_season.drop_duplicates(subset=['team_api_id', 'season', 'player'], keep='first')

df_players_home_season.shape
#get players for away_teams per season
df_players_away_season = df_match_players[['away_team_api_id', 'season', 'away_player_1', 'away_player_2', 'away_player_3', 'away_player_4', 'away_player_5', 'away_player_6', 'away_player_7', 'away_player_8', 'away_player_9', 'away_player_10', 'away_player_11']]

#pivot the table and drop the null values for players
df_players_away_season = pd.melt(df_players_away_season, id_vars=['away_team_api_id', 'season'], var_name='position', value_name='player').dropna()

#change columnname
df_players_away_season.rename(columns={'away_team_api_id': 'team_api_id'}, inplace=True)
#drop column position
df_players_away_season.drop(columns=['position'], inplace=True)
#since players play more than one match in a season we need to remover duplicates
df_players_away_season=df_players_away_season.drop_duplicates(subset=['team_api_id', 'season', 'player'], keep='first')

df_players_away_season.shape
#Now combine the two to get a list of all players
df_team_season_players = df_players_home_season.append(df_players_away_season, ignore_index=True)
#remove duplicates
df_team_season_players=df_team_season_players.drop_duplicates(subset=['team_api_id', 'season', 'player'], keep='first')

df_team_season_players.head()
df_players = pd.read_sql_query(
    "SELECT * FROM Player;", con)
df_players.head()
df_playerattr = pd.read_sql_query(
    "SELECT * FROM Player_Attributes;", con)
df_playerattr.head()
df_teams.info()
df_teams[df_teams.duplicated(['team_api_id'])]
df_teamattr.info()
pd.read_sql_query("SELECT buildUpPlayDribblingClass, buildUpPlayDribbling FROM Team_Attributes WHERE buildUpPlayDribbling IS NULL GROUP BY buildUpPlayDribblingClass;", con)
df_dribbling = df_teamattr[['buildUpPlayDribblingClass', 'buildUpPlayDribbling']]
df_dribblinglittle = df_dribbling[df_dribbling.buildUpPlayDribblingClass == 'Little']
df_dribblinglittle['buildUpPlayDribbling'].describe()
df_teamattr['buildUpPlayDribbling'].fillna(30, inplace=True)
df_teamattr.info()
df_teamattr.team_api_id.value_counts().describe()
df_match_players.info()
df_matchscores.info()
df_matchscores[df_matchscores.duplicated(['match_api_id'])]
df_players.info()
df_players[df_players.duplicated(['id'])]
#Calculation based on winning we can change after or modify to give as the letters as a result
df_matchscores.loc[df_matchscores['home_team_goal'] - df_matchscores['away_team_goal'] > 0, 'points_home_team'] = 3
df_matchscores.loc[df_matchscores['home_team_goal'] - df_matchscores['away_team_goal'] == 0, 'points_home_team'] = 1
df_matchscores.loc[df_matchscores['home_team_goal'] - df_matchscores['away_team_goal'] < 0, 'points_home_team'] = 0
df_matchscores.loc[df_matchscores['home_team_goal'] - df_matchscores['away_team_goal'] > 0, 'points_away_team'] = 0
df_matchscores.loc[df_matchscores['home_team_goal'] - df_matchscores['away_team_goal'] == 0, 'points_away_team'] = 1
df_matchscores.loc[df_matchscores['home_team_goal'] - df_matchscores['away_team_goal'] < 0, 'points_away_team'] = 3
df_matchscores.head()
df_points_season_home = df_matchscores.groupby(['home_team_api_id', 'season'])['points_home_team'].agg(['sum','count']).reset_index()
#rename columns
df_points_season_home.columns = ['team_api_id', 'season', 'points', 'matches']
df_points_season_home.head()
df_points_season_away = df_matchscores.groupby(['away_team_api_id', 'season'])['points_away_team'].agg(['sum','count']).reset_index()
#rename columns
df_points_season_away.columns = ['team_api_id', 'season', 'points', 'matches']
df_points_season_away.head()
df_points_season_both = pd.concat([df_points_season_home, df_points_season_away])

#and sum points and matches for each team as home_team and away_team
df_team_season_points = df_points_season_both.groupby(['team_api_id', 'season']).sum().reset_index()

#add a column points per match to calculate the average points per match
df_team_season_points['points_per_match'] = df_team_season_points['points']/df_team_season_points['matches']

#add columns for season start en end date assuming that the seasons start on July 1st and end on June 30th. We will need these columns to compare with the team attributes later.
df_team_season_points['seasonstart'] = df_team_season_points['season'].str[:4] + '-07-01'
df_team_season_points['seasonend'] = df_team_season_points['season'].str[5:] + '-06-30'

#merge with the team dataframe to add names to the teams
df_teamname_season_points = pd.merge(df_teams[['team_api_id', 'team_long_name']] , df_team_season_points, how='right', on='team_api_id')

#sort descending by points_per_match
df_teamname_season_points.sort_values(by='points_per_match', ascending=False).head(10)
df_teamname_season_points.sort_values(by='points_per_match', ascending=True).head(10)
print("---------------------------------------------------------------------------------------------------------------------------")
print(tables)
print("---------------------------------------------------------------------------------------------------------------------------")
print(df_teams)
print("---------------------------------------------------------------------------------------------------------------------------")
print(df_matchscores)
print("---------------------------------------------------------------------------------------------------------------------------")
print(df_team_season_players)
print("---------------------------------------------------------------------------------------------------------------------------")
print(df_teamname_season_points)
print("---------------------------------------------------------------------------------------------------------------------------")
print(df_teamname_season_points.sort_values(by='points_per_match', ascending=True).head(10))
print("---------------------------------------------------------------------------------------------------------------------------")
