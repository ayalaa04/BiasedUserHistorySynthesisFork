'''
    This program defines the interactions of the users to each item.
    The interactions are defined as each user's liked songs.
    With this final dataset filtering program, we now have the basic data of 
    the two-tower model.
'''
import pandas as pd

# Read both csvs
df_user = pd.read_csv('user.csv')
df_apple_music = pd.read_csv('items.csv')

# Assign an id to the music and user dataframes
df_apple_music['id'] = range(1, len(df_apple_music) + 1)
df_user['id'] = range(1, len(df_user) + 1)

id_to_trackname = pd.Series(df_apple_music['trackName'].values, index=df_apple_music['id']).to_dict()


id_lst = []
index_count = {}
df_lst = []

# For every 
for i in range(len(df_user)):
    start_marker = "'track_name': '"
    end_marker = "',"
    loved_tracks_str = df_user.loc[i, 'loved_tracks'] 
    
    track_names = []
    start_pos = 0
    while True:
        start_pos = loved_tracks_str.find(start_marker, start_pos)
        if start_pos == -1:
            break
        start_pos += len(start_marker)
        end_pos = loved_tracks_str.find(end_marker, start_pos)
        if end_pos == -1:
            break
        track_name = loved_tracks_str[start_pos:end_pos]
        track_names.append(track_name)
        start_pos = end_pos + len(end_marker)

    for name in track_names:
        if name in df_apple_music['trackName'].values:
            index = df_apple_music.index[df_apple_music['trackName'] == name].tolist()[0]
            id_lst.append(i)
            id_lst.append(index)

            if index in index_count:
                index_count[index] += 1
            else:
                index_count[index] = 1

            df_lst.append(id_lst.copy())
            id_lst.clear()


df_result = pd.DataFrame(df_lst, columns=['user_id', 'track_id'])


# Filter out the low interaction users (users with < 5 interactions)
while True:
    print(len(df_result))

    song_lst = [key for key, value in index_count.items() if value < 5]
    df_result = df_result[~df_result['track_id'].isin(song_lst)]


    user_interaction_count = df_result['user_id'].value_counts()
    low_interaction_users = user_interaction_count[user_interaction_count < 5].index


    print("User IDs to be removed:", low_interaction_users.tolist())

    df_result = df_result[~df_result['user_id'].isin(low_interaction_users)]


    updated_track_count = df_result['track_id'].value_counts()
    song_lst = [track for track in song_lst if updated_track_count.get(track, 0) >= 5]


    if len(song_lst) == 0 and len(low_interaction_users) == 0:
        break

df_result.reset_index(drop=True, inplace=True)
df_result.to_csv('final_interactions.csv', index=False)