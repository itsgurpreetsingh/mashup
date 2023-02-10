import requests
from pytube import YouTube
from bs4 import BeautifulSoup
from moviepy.editor import *
from pydub import AudioSegment
from mutagen.mp3 import MP3
import streamlit as st
import re
import json
import sys

st.title("MASHUP")
search=st.text_input("Enter name of singer", "Type Here ...") 
n_video=st.number_input("Enter no of videos")
StrtSec = st.number_input("Enter audio duration to cut")
out=st.text_input("Enter name of output file", "output.mp3") 
EndSec = 20
StrtTime = StrtSec*1000
v_name=[]
count=0
video_id=[]
audio_clip_paths=[]
url=[]
query='+'.join(str(x) for x in search)

response=requests.get(f"https://www.youtube.com/results?search_query={query}").text
soup=BeautifulSoup(response,'lxml')
script=soup.find_all("script")[33]

json_text=re.search('var ytInitialData = (.+)[,;]{1}',str(script)).group(1)
json_data=json.loads(json_text)
content=(
    json_data['contents']['twoColumnSearchResultsRenderer']['primaryContents']['sectionListRenderer']['contents'][0]['itemSectionRenderer']['contents']
)
for data in content:
    for key,value in data.items():
        if(type(value) is dict):
            for k,v in value.items():
                if k=="videoId" and len(v)==11:
                    video_id.append(v)


for i in range(n_video):
    url.append(f"https://www.youtube.com/watch?v={video_id[i]}")
 
try:
    for link in url[0:n_video]:
        vid = YouTube(link)
        Yvideo = vid.streams.filter(file_extension='mp4').order_by('resolution').desc()
        v_name.append(vid.title)
        Yvideo.get_lowest_resolution().download(output_path='./',filename=f"{count}.mp4")
        count=count+1
except:
    sys.exit("Connection problem please check your connection and try again")        

for j in range(count):
    video = VideoFileClip(f"{j}.mp4")
    audio = video.audio
    audio.write_audiofile(f"{j}.mp3")

for k in range(count):
    file=f"{k}.mp3"
    sound = AudioSegment.from_file(file)
    audFile = MP3(file)
    audio_info = audFile.info    
    duration = int(audio_info.length)
    EndTime=duration*1000
    p1 = sound[StrtTime: EndTime]
    p1.export(f'{k}.mp3', format='mp3')
for p in range(count):
    audio_clip_paths.append(f'{p}.mp3')

print(audio_clip_paths)
clips = [AudioFileClip(c) for c in audio_clip_paths]
final_clip = concatenate_audioclips(clips)
final_clip.write_audiofile(out)

for f in range(count):
    os.remove(f'{f}.mp3')
    os.remove(f'{f}.mp4')

