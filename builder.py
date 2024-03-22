import speech_recognition as sr
import pydub
from pydub import AudioSegment
import os
from tqdm import tqdm
from langdetect import detect

def split_audio(audio_file, chunk_size_ms):
    audio = AudioSegment.from_file(audio_file)
    chunks = []
    for i in range(0, len(audio), chunk_size_ms):
        chunk = audio[i:i+chunk_size_ms]
        chunks.append(chunk)
    return chunks

def save_chunk_as_temp_file(chunk, temp_file_path):
    chunk.export(temp_file_path, format="wav")

def is_english(text):
    try:
        return detect(text) == 'en'
    except:
        return False

def extract_english_words(text):
    english_words = []
    for word in text.split():
        if is_english(word):
            english_words.append(word)
    return ' '.join(english_words)

def speech_recognition_chunks(audio_file, chunk_size_ms=10000):
    temp_folder = "./temp_chunks/"
    if not os.path.exists(temp_folder):
        os.makedirs(temp_folder)
    
    chunks = split_audio(audio_file, chunk_size_ms)
    recognizer = sr.Recognizer()
    
    with open('english_words.txt', 'w') as f:
        for i, chunk in enumerate(tqdm(chunks, desc="Processing", unit="chunk")):
            temp_file_path = os.path.join(temp_folder, f"chunk_{i}.wav")
            save_chunk_as_temp_file(chunk, temp_file_path)
            
            with sr.AudioFile(temp_file_path) as source:
                audio_data = recognizer.record(source)
                try:
                    text = recognizer.recognize_google(audio_data,language="en-us")
                    english_text = extract_english_words(text)
                    if english_text:
                        print(f"English word found: {english_text}")  # Print alert when an English word is found
                        f.write(english_text + '\n')
                        a = open("words.txt","+a")
                        for i in english_text.split():
                            a.write(i+"\n")
                        a.close()
                except sr.UnknownValueError:
                    print("Google Speech Recognition could not understand audio")
                except sr.RequestError as e:
                    print(f"Could not request results from Google Speech Recognition service; {e}")
            
            os.remove(temp_file_path)  # Remove temporary file

audio_file = 'main.wav'
speech_recognition_chunks(audio_file)
