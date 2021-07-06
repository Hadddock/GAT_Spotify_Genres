# GAT Spotify Genres
An unsupervised machine learning model to learn machine-made genres for Spotify tracks based on user playlists and track features.

The representations for each track are formed from
1. A list of tracks designated as their "neighbors". The "neighbors" for each track are other tracks included in the same playlist(s), with the playlists being taken from the [Spotify Million Playlist Dataset](https://www.aicrowd.com/challenges/spotify-million-playlist-dataset-challenge "Spotify Million Playlist Dataset")
2. A collection of audio features representing abstract features of the track (danceability,  energy,  instrumentalness, etc.) collected through Spotify's API

The goals of this project are:
1. To compare the genre clusters created based on audio features with human assigned genres.
2. To compare the genre clusters created based on the audio features for each song with the genre clusters created based on the audio features for each song after passing the tracks through GAT layers.
3. To use the genre clusters to create an alternative to Spotify's current track recommendation system.
