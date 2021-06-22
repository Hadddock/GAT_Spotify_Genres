#!/usr/bin/env python
# coding: utf-8

# ## Imports

# In[2]:


import os
import pandas as pd
import spotipy
import json
from collections import Counter
from spotipy.oauth2 import SpotifyClientCredentials
import pickle
import numpy as np
from scipy.sparse import csr_matrix
from scipy.sparse import lil_matrix


# ## Spotify Credentials
# Set environment variables for your Spotify credentials

# In[6]:


cid = os.environ.get("SPOTIPY_CLIENT_ID")
secret = os.environ.get("SPOTIPY_CLIENT_SECRET")
client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
spotify = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


# ## Collect information from Spotify Million Playlist Dataset
# 
# Download dataset from: https://www.aicrowd.com/challenges/spotify-million-playlist-dataset-challenge

# In[8]:


tracks_info = {}#key = track uri, value = list of information about the track
tracks_neighbors = {}#key = track uri, value = Counter of tracks neighbors
track_playlist_count = {} #key = track uri, value = total playlist appearences

with open("data/mpd.slice.0-999.json", "r") as read_file:
    data = json.load(read_file)
for playlist in data.get('playlists'):
    playlist_track_uris = set() #all track uris appearing in this playlist
    for track in playlist.get('tracks'):
        track_info = []
        track_uri = track.get("track_uri")
        if not track_uri in tracks_info.keys():#only retrive track info once
            tracks_info[track_uri] = [
                track.get('track_name'),
                track.get("artist_uri"),
                track.get("artist_name"),
                track.get("album_uri"),
                track.get("album_name")
                ]
        if not track_uri in playlist_track_uris:#do not count multiple entries of same song in playlist twoards track_playlist_count
            if not track_uri in track_playlist_count.keys():#keep track of total playlist occurences
                track_playlist_count[track_uri] = 0
            track_playlist_count[track_uri] += 1
        playlist_track_uris.add(track_uri)
        
    for track in playlist.get('tracks'):#update neighbors for each track in the playlist
        track_uri = track.get("track_uri")
        if not track_uri in tracks_neighbors.keys():
            tracks_neighbors[track_uri] = Counter()
        tracks_neighbors[track_uri].update(playlist_track_uris)


# ## Get track features from Spotify api
# Spotify limits retriving track info to 100 tracks per query

# In[77]:


track_features = []
total_track_count =len(tracks_info.keys())
for i in range(0, total_track_count, 100):
    end_index = min(i + 100, total_track_count)
    track_features.extend(spotify.audio_features(list(tracks_info.keys())[i:end_index]))


# ## Create dataframe

# In[146]:


df = pd.DataFrame.from_dict(data=tracks_info, orient = 'index', columns=['title', 'artist uri', 'artist', 'album uri', 'album title'])
df.reset_index(inplace=True)
df.rename(columns={'index': 'uri'}, inplace=True)
df['total playlist appearences'] = track_playlist_count.values()
df['neighboring tracks'] = tracks_neighbors.values()
df = pd.merge(df, pd.DataFrame.from_dict(data=track_features), on="uri")


# ## Pickle Helper Functions

# In[149]:


def pickle_object(output_file_name, object):
    dbfile = open(output_file_name, 'ab')   
    pickle.dump(object, dbfile)                     
    dbfile.close()
    
def unpickle_object(pickle_file_name):
    with open('track_dataframe.pickle', "rb") as input_file:
        unpickled_object = pickle.load(input_file)
    return unpickled_object


# pickle the dataframe

# In[151]:


pickle_object('track_dataframe.pickle',df)


# load the dataframe

# In[15]:


df = unpickle_object('track_dataframe.pickle')


# In[17]:


display(df)

