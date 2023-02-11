import requests
from pytube import YouTube
from bs4 import BeautifulSoup
from moviepy.editor import *
from pydub import AudioSegment
from mutagen.mp3 import MP3
import streamlit as st
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import re
import json
def check(search,n_video,StrtSec,out,mailid):
    error=True
    if(out[-4:]!=".mp3"):
            st.error('Output file format not supported please enter ".mp3"')   
            flag=False
    testEmail = mailid
    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'    
    if(re.search(regex,testEmail)):   
        print("valid") 
    else:   
        error="Invalid email address"

    if type(n_video)=='int' and type(StrtSec)=='int':
        error="Audio duration and number of videos must be an integer"

    if StrtSec<20:
        error='Audio duration to cut must be greater than 20'

    if(n_video==0):
        error='Enter valid no of videos greater or equal to 2'  

    return error  

def proceed(search,n_video,StrtSec,out,mailid):
        print(search)
        print(n_video)
        print(StrtSec)
        print(out)  
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


        for i in range(len(video_id)):
            url.append(f"https://www.youtube.com/watch?v={video_id[i]}")
 
        try:
            for link in url:
                if(count==n_video):
                    break
                
                vid = YouTube(link)
                if vid.length>360 or vid.length<120:
                    continue
                Yvideo = vid.streams.filter(file_extension='mp4').order_by('resolution').desc()
                v_name.append(vid.title)
                Yvideo.get_lowest_resolution().download(output_path='./',filename=f"{count}.mp4")
                count=count+1
        except:
            st.error("Connection problem please check your connection and try again")    


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

        fromaddr = "gsingh102003@gmail.com"
        toaddr = mailid
        msg = MIMEMultipart()
        msg['From'] = fromaddr
        msg['To'] = toaddr
        msg['Subject'] = "Mashup file"
        body = "Your mashup"
        msg.attach(MIMEText(body, 'plain'))
        attachment = open(out, "rb")
        p = MIMEBase('application', 'octet-stream')
        p.set_payload((attachment).read())
  
        # encode into base64
        encoders.encode_base64(p)
   
        p.add_header('Content-Disposition', "attachment; filename= %s" % out)
  
        # attach the instance 'p' to instance 'msg'
        msg.attach(p)
  
        # creates SMTP session
        s = smtplib.SMTP('smtp.gmail.com',587)
  
        # start TLS for security
        s.starttls()
  
        # Authentication
        s.login(fromaddr, "erbaazraounsrsqp")
  
        # Converts the Multipart msg into a string
        text = msg.as_string()
  
        # sending the mail
        s.sendmail(fromaddr, toaddr, text)
  
        # terminating the session
        s.quit()
        os.remove(out)
        st.success("Mashup successfully sent on mail")
    
st.title("MASHUP")
with st.form("my_form"):
    search=st.text_input("Enter name of singer") 
    n_video=st.number_input("Enter number of videos",format="%d")
    StrtSec = st.number_input("Enter audio duration to cut",format="%d")
    out=st.text_input("Enter name of output file", "output.mp3") 
    mailid=st.text_input("Enter sender address") 
    submitted = st.form_submit_button("Submit")
    
    if submitted:
        st.write("text_input", search, "number_input", n_video,"number_input",StrtSec,"text_input",out,"text_input",mailid)
        n_video=int(n_video)
        with st.spinner('Your mashup is in processing..It may take few minutes'):

            flag=check(search,n_video,StrtSec,out,mailid)
            if(flag==True):
                proceed(search,n_video,StrtSec,out,mailid)
            else:
                st.error(flag)
        st.success('Done!')    
    