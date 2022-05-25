import pytube
from csv import writer, reader
from youtubesearchpython import VideosSearch
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os

def append_list_as_row(file_name, list_of_elem):
    with open(file_name, 'a+', newline='', encoding='cp1252') as write_obj:
        csv_writer = writer(write_obj)
        csv_writer.writerow(list_of_elem)
        
def csv_read_rows(filename):
    rows=[]
    with open(filename, 'r', encoding='cp1252') as read_obj:
        csv_reader = reader(read_obj)
        for row in csv_reader:
            rows.append(row)
    return rows


downloaded_song = [i[0] for i in csv_read_rows('downloaded_song.csv')]

auth_manager = SpotifyClientCredentials(
    #<your credentials>
)
sp = spotipy.Spotify(auth_manager=auth_manager)

playlist = sp.user_playlist_tracks(
    #<playlist>
)


playlist = playlist['items']


songs = []
for song in playlist:
    song = song['track']
    name = ''
    for artist in song['artists']:
        name += artist['name'] + ', '
    name = name[:-2]
    name += ' - ' + song['name']
    songs.append(name)


# In[24]:


yt_watch="https://www.youtube.com/watch/{}"


# In[25]:


songs = list(filter(lambda x : x not in downloaded_song, songs))


# In[27]:


for song in songs:
    print(f'[downloading] {song}')
    videosSearch = VideosSearch(song, limit = 2)


    vid_id = videosSearch.result()['result'][0]['id']

    yt_vid=yt_watch.format(vid_id)

    youtube = pytube.YouTube(yt_vid)

    streams = youtube.streams

    audio = streams.filter(only_audio=True).first()
    
    out_file = audio.download('songs')
#     base, ext = os.path.splitext(out_file)
#     new_file = base + '.mp3'
#     os.rename(out_file, new_file)
    append_list_as_row('downloaded_song.csv', [song])
    


# In[ ]:





# In[ ]:





# In[ ]:




