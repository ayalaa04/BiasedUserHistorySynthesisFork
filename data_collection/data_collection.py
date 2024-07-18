import requests
import pandas as pd
import random
import time
import os


API_KEY = '5fae7208288b136b5a2306d078847c4f'
BASE_URL = 'http://ws.audioscrobbler.com/2.0/'

# Fetch the user info using our API key
def get_user_info(username):
    api_url_user_info = f'{BASE_URL}?method=user.getinfo&user={username}&api_key={API_KEY}&format=json'
    response = requests.get(api_url_user_info)
    if response.status_code == 200:
        return response.json().get('user', {})
    else:
        return {}

# Fetch the loved tracks of the user
def get_loved_tracks(username):
    api_url_loved_tracks = f'{BASE_URL}?method=user.getlovedtracks&user={username}&api_key={API_KEY}&format=json&limit=50'
    response = requests.get(api_url_loved_tracks)
    if response.status_code == 200:
        return response.json().get('lovedtracks', {}).get('track', [])
    else:
        return []

# Function to check if a track is in the Apple Music dataset
def is_track_in_apple_music(artist, track_name):
    return ((apple_music_df['artistName'] == artist) & (apple_music_df['trackName'] == track_name)).any()

# Load the Apple Music dataset
apple_music_df = pd.read_csv('data_collection/DATASET/apple_music_dataset.csv')

# Fetch the info of the user’s friends, ensuring each friend is unique and has a country
def fetch_friends_info(username, seen_users, limit=200):
    friends_data = []
    page = 1
    while len(friends_data) < limit:
        api_url_user_info = f'{BASE_URL}?method=user.getfriends&user={username}&api_key={API_KEY}&format=json&limit=50&page={page}'
        response = requests.get(api_url_user_info)
        if response.status_code == 200:
            data = response.json()
            friends = data.get('friends', {}).get('user', [])
            for friend in friends:
                if len(friends_data) >= limit:
                    break
                friend_name = friend.get('name')
                real_name = friend.get('realname')
                country = friend.get('country')
                if None in (friend_name, real_name, country) or country == "None":
                    continue 
                elif friend_name not in seen_users:
                    loved_tracks = get_loved_tracks(friend_name)
                    valid_tracks = [track for track in loved_tracks if is_track_in_apple_music(track.get('artist', {}).get('name'), track.get('name'))]
                    if len(valid_tracks) >= 5:
                        friends_data.append({
                            'name': friend_name,
                            'realname': real_name,
                            'country': country,
                            'loved_tracks': valid_tracks[:5]  # Ensure only the first 5 valid tracks are stored
                        })
                        seen_users.add(friend_name)
            total_pages = int(data.get('friends', {}).get('@attr', {}).get('totalPages', 1))
            if page >= total_pages:
                break
            page += 1
        else:
            break
    return friends_data

# Initialize variables
initial_username = 'RJ'  # Initial user to start fetching data
user_data = []
seen_users = set()
num_users = 1000  # Number of users to fetch

# Fetch initial user’s info
initial_user_info = get_user_info(initial_username)
if initial_user_info:
    user_info = {
        'name': initial_user_info.get('name'),
        'realname': initial_user_info.get('realname'),
        'country': initial_user_info.get('country')
    }
    loved_tracks = get_loved_tracks(user_info['name'])
    valid_tracks = [track for track in loved_tracks if is_track_in_apple_music(track.get('artist', {}).get('name'), track.get('name'))]
    if user_info['name'] not in seen_users and len(valid_tracks) >= 5:
        user_info['loved_tracks'] = valid_tracks[:5]  # Ensure only the first 5 valid tracks are stored
        user_data.append(user_info)
        seen_users.add(user_info['name'])

# Fetch friends of the initial user
friends_data = fetch_friends_info(initial_username, seen_users, limit=200)
user_data.extend(friends_data)

# If less than 1000 users, fetch friends of friends
while len(user_data) < num_users and friends_data:
    random_friend = random.choice(friends_data)
    friends_data = fetch_friends_info(random_friend['name'], seen_users, limit=(num_users - len(user_data)))
    user_data.extend(friends_data)
    time.sleep(0.2)  # To avoid hitting rate limits

    # If friends_data is empty, it means we've exhausted all friends, need to pick another random user from the list
    if not friends_data and len(user_data) < num_users:
        # Fetching friends of any random user in the list if more users are needed
        remaining_users = [user['name'] for user in user_data if user['name'] not in seen_users]
        if remaining_users:
            next_user = random.choice(remaining_users)
            friends_data = fetch_friends_info(next_user, seen_users, limit=(num_users - len(user_data)))
            user_data.extend(friends_data)
            time.sleep(0.2)  # To avoid hitting rate limits

# Ensure we have exactly 1000 unique users
final_data = user_data[:num_users]

# Prepare data for CSV
expanded_data = []
for user in final_data:
    for track in user['loved_tracks']:
        expanded_data.append({
            'Username': user['name'],
            'Loved Track Name': track.get('name'),
            'Loved Track Artist Name': track.get('artist', {}).get('name'),
            'Time Loved': track.get('date', {}).get('uts')
        })

# Save expanded user data to CSV
interactions_df = pd.DataFrame(expanded_data)
interactions_df.to_csv('interactions.csv', index=False)
print(f"Found {len(final_data)} items.")
print(f"User info and loved tracks for {len(interactions_df)} entries have been written to 'items.csv'.")