'''
pip install SpeechRecognition
pip install pydub
pip install pyAudio
'''

'''
Simple speech to text

import speech_recognition as sr
filename = r'c:\work\Test.wav'
r=sr.Recognizer()
with sr.AudioFile(filename) as source:
    audio_data = r.record(source)
    text = r.recognize_google(audio_data)
    print(text)
'''

import speech_recognition as sr
import os
from pydub import AudioSegment
from pydub.silence import split_on_silence

r=sr.Recognizer()

def transcribe_audio(path):
    text = ''
    with sr.AudioFile(path) as source:
        audio_listened = r.record(source)
        text = r.recognize_google(audio_listened)
    return text

def get_large_audio_transcription_on_silence(path):
    sound = AudioSegment.from_file(path)
    chunks = split_on_silence(sound, min_silence_len=500, silence_thresh= sound.dBFS-14,keep_silence=500)
    folder_name = "audio-chunks"
    if not os.path.isdir(folder_name):
        os.mkdir(folder_name)
    whole_text = ''
    for i, audio_chunk in enumerate(chunks, start=1):
        chunk_filename = os.path.join(folder_name, f"chunk{1}.wav")
        audio_chunk.export(chunk_filename, format="wav")
        try:
            text=transcribe_audio(chunk_filename)
        except sr.UnknownValueError as e:
            print("Error :", str(e))
        else:
            text = f"{text.capitalize()}. "
            print(chunk_filename, ":", text)
            whole_text = whole_text + text
    return whole_text

# Do conversion if input is MP3
src = "audio.mp3"
dst = "audio.wav"
conv_sound = AudioSegment.from_mp3(src)
conv_sound.export(dst, format="wav")
#path = r'c:\work\Test.wav'
input = dst
print("\nFull text :", get_large_audio_transcription_on_silence(input))
