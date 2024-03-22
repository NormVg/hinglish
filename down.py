from pytube import YouTube
from pydub import AudioSegment


yt = YouTube('http://youtube.com/watch?v=2nsAB11WP3g')
a = yt.streams.get_lowest_resolution().download()



def convert_mp4_to_wav(mp4_file, wav_file):
    # Load the MP4 file
    audio = AudioSegment.from_file(mp4_file, format="mp4")
    
    # Convert the audio to WAV format
    audio.export(wav_file, format="wav")

# Replace 'input.mp4' and 'output.wav' with your input and output file paths
convert_mp4_to_wav(a, 'main.wav')
