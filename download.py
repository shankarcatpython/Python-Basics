
from pytube import YouTube

# This captures the link(url) and locates it from YouTube.

link_list =['https://www.youtube.com/watch?v=GKSRyLdjsPA','https://www.youtube.com/watch?v=AUvodoVurps']

# iterate the list 
# This captures the streams available for downloaded for the video i.e. 360p, 720p, 1080p. etc.
# filter out audio only but the format will be MP4

for link in link_list:
    url = YouTube(str(link))
    audio = url.streams.filter(only_audio=True, file_extension='mp4').first()
    audio.download(r'C:\Users\email\OneDrive\Desktop\Download\Audio')

# Commit can be done