import os
import moviepy.editor as mp

# Some cars will not able to play the mp4 
# This program converts the mp4 player to mp3 so that it can be played in cars

# Folder path where the videos or mp4 available
dir_path1 = r'C:\Users\email\OneDrive\Desktop\Download\Theme'

# list to store files
res = []

# Iterate directory and convert the file in to audio and write the file in same path under Audio folder

for path in os.listdir(dir_path1):
    if os.path.isfile(os.path.join(dir_path1, path)):
        res.append(path)

for filename in res:
    print(filename.split('.')[0])
    print("{}\{}".format(dir_path1,filename))
    clip = mp.AudioFileClip("{}\{}".format(dir_path1,filename))
    clip.write_audiofile("{}\Audio\{}.mp3".format(dir_path1,filename.split('.')[0]))

# when songs need to be for longer trip in usb