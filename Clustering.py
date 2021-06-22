#!/usr/bin/env python
# coding: utf-8

# ## Imports

# In[7]:


import pickle
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans


# ## Helper Functions

# In[8]:


def unpickle_object(pickle_file_name):
    with open('track_dataframe.pickle', "rb") as input_file:
        unpickled_object = pickle.load(input_file)
    return unpickled_object


# ## Retrive Dataset

# In[10]:


df = unpickle_object('track_dataframe.pickle')


# In[16]:


track_features = df[["danceability", "energy",'instrumentalness', "liveness", 'valence']]
display(track_features)


# In[19]:


kmeans = KMeans(
    init="random",
    n_clusters=3,
    n_init=10,
    max_iter=300,
    random_state=42
)
kmeans.fit(track_features)
ymeans = kmeans.predict(track_features)
print(ymeans)


# ## Plot clusters

# In[ ]:




