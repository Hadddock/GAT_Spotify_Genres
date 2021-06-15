#!/usr/bin/env python
# coding: utf-8

# ### Imports

# In[1]:


import spotipy
import scipy
import numpy as np
from scipy import sparse
from scipy.sparse import csr_matrix
from scipy.sparse import lil_matrix
import json
import os
import re
import pickle
import numpy
from spotipy.oauth2 import SpotifyClientCredentials


# ### Pickle helper method

# In[2]:


def pickle_object(output_file_name, object):
    dbfile = open(output_file_name, 'ab')   
    pickle.dump(object, dbfile)                     
    dbfile.close()


# ### Establish credentials

# In[7]:


# Replace cid and secret id with your corresponding Spotify credentials

cid = os.environ.get("SPOTIPY_CLIENT_ID")
secret = os.environ.get("SPOTIPY_CLIENT_SECRET")

client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
spotify = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


#spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())
#print(spotify)


# ### Retrive track audio features

# In[13]:


def retrive_audio_features(trackid):
    return spotify.audio_features(trackid)


# ### Retrive track name

# In[16]:


def retrive_track_name(trackid):
    results = spotify.track(trackid)
    return results['name']


# ### Build dictionary of track neighbors

# In[14]:


with open("data/mpd.slice.0-999.json", "r") as read_file:
    data = json.load(read_file)


# In[16]:


#dict where keys are track_uri and elements are dictionaries, each of which has a key of
#the track's neighbor with an element of how many times the track appears as its neighbor
track_dict = {}
track_playlist_occurences = {}#dict of how many playlists each track occurs in
# for filename in os.listdir("data"):
#     data = json.load(open( os.getcwd() + os.path.sep + "data" + os.path.sep + filename, "r"))
for playlist in data.get('playlists'):
    playlist_tracks = []
    for track in playlist.get('tracks'):
        playlist_tracks.append(track.get("track_uri"))#retrive this track's uri
        #print(track.get("track_uri"))
        #print(track.get("track_name"))
    playlist_tracks = set(playlist_tracks) # set of all tracks in the current playlist
    for track in playlist_tracks:
        if track in track_dict:
            track_playlist_occurences[track] += 1
        else:
            track_dict[track] = {}
            track_playlist_occurences[track] = 0

        for neighboring_track in playlist_tracks:
            if neighboring_track in track_dict[track]:
                track_dict[track][neighboring_track] += 1 
            else:
                track_dict[track][neighboring_track] = 1
for track in track_dict.keys():
    print(track)
    track_dict[track] = (track_dict[track], track_playlist_occurences[track], spotify.audio_features(track))


# ### Test track entries

# In[53]:


print(len(track_dict))
tracks_list = track_dict.keys()

print(track_dict[x])
for key in track_dict.keys():
    print("Number of track occurences: " + str(track_dict[key][1]))
    print("Number of neighboring tracks: " + str(len(track_dict[key][0])))
    print("Audio features: " + str(track_dict[key][1]))
    print(track_dict[key])
    i+=1
    if i > 2:
        break


# ### Keep spare copy of dictionary

# In[55]:


x = list(track_dict.keys())[13533]
track_dict_copy = track_dict


# ### Dump Dictionary

# In[132]:


dbfile = open('sparse_adjacency_matrix.pickle', 'ab')   
# source, destination
pickle.dump(adjacency_matrix, dbfile)                     
dbfile.close()


# In[2]:


with open("trimmed_dataset.pickle", "rb") as input_file:
    track_dict = pickle.load(input_file)


# ### Clean dataset
# 1. remove unprocessed tracks
# 2. remove neighborless tracks
# 3. remove edges to unprocessed tracks
# 

# In[95]:


tracks_list = list(track_dict.keys())
x = tracks_list[13535]

#for all unprocessed tracks

#for each processed track

for j in range(0,13535):
    current_track_uri = tracks_list[j]
    #remove edges to unprocessed tracks
    for i in range (13535,len( tracks_list)):
        removal_track_uri = tracks_list[i]
        if removal_track_uri in track_dict[current_track_uri][0]:
            new_track_neighbors = track_dict[current_track_uri][0]
            del new_track_neighbors[removal_track_uri]
            track_dict[current_track_uri] = new_track_neighbors, track_dict[current_track_uri][1],track_dict[current_track_uri][2]
#remove track entry entirely        
for i in range (13535,len( tracks_list)):
    removal_track_uri = tracks_list[i]
    del track_dict[removal_track_uri]


# ### Create Adjacency Matrix
# 1. Create sparse lil_matrix
# 2. Populate adjacency matrix
# 3. Convert to compressed sparse row matrix
# 4. pickle adjacency matrix

# In[124]:


print(len(track_dict))
current_track_uri = tracks_list[13534]

adjacency_matrix = lil_matrix((13535,13535))
adjacency_matrix[0][0] = 1
print(adjacency_matrix.shape)
track_dict_list = list(track_dict.keys())

#ainsert into adjacency matrix
current_index = 0
for track in track_dict.keys():
    max_cooccurrences = max(track_dict[track][0].values())
    for neighbor in track_dict[track][0].keys():
        neighbor_index = track_dict_list.index(neighbor)
        print(neighbor_index)
        adjacency_matrix[current_index, neighbor_index] = track_dict[track][0][neighbor]/max_cooccurrences
    
    current_index += 1  
#convert to compressed sparse row matrix


adjacency_matrix = csr_matrix(adjacency_matrix)
#export pickle of adjacency_matrix    
pickle_object('sparse_adjacency_matrix.pickle', adjacency_matrix)


# ### Create node features

# In[130]:


node_features = np.empty(shape=(13535,13) ,dtype='float')
print(node_features.shape)
i = 0
for track in track_dict.keys():
    features = track_dict[track][2][0]
    current_node_features = np.array(
        [features['danceability'],
        features['energy'],
        features['key'],
        features['loudness'],
        features['mode'],
        features['speechiness'],
        features['acousticness'],
        features['instrumentalness'],
        features['liveness'],
        features['valence'],
        features['tempo'],
        features['duration_ms'],
        features['time_signature']
        ],
        dtype = 'float'                   
        )
    print(current_node_features)
    node_features[i] = current_node_features
    #np.put_along_axis(arr=node_features, indices=i,values=current_node_features,axis=0 )
    i+=1
pickle_object("node_features.pickle", node_features)


# In[128]:


print(node_features[13534])
#x = track_dict['spotify:track:1AWQoqb9bSvzTjaLralEkT'][2][0]

#print(x)

