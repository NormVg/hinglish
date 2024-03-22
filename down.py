from pytube import YouTube

yt = YouTube('http://youtube.com/watch?v=2nsAB11WP3g')
a = yt.streams.get_lowest_resolution().download()

import moviepy.editor as mp
 
# Insert Local Video File Path 
clip = mp.VideoFileClip(a)
 
# Insert Local Audio File Path
clip.audio.write_audiofile(r"main.wav")