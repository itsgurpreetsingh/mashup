import requests
from pytube import YouTube
from bs4 import BeautifulSoup
from moviepy.editor import *
from pydub import AudioSegment
from mutagen.mp3 import MP3
import streamlit as st
from zipfile import *
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import re
import json
def check(search,n_video,EndSec,out,mailid):
    error=True
    if(out[-4:]!=".mp3"):
            st.error('Output file format not supported please enter ".mp3"')   
            flag=False
    testEmail = mailid
    testEmail=testEmail.strip()
    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'    
    if(re.search(regex,testEmail)):   
        print("valid") 
    else:   
        error="Invalid email address"

    if type(n_video)=='int' and type(EndSec)=='int':
        error="Audio duration and number of videos must be an integer"

    if(n_video==0):
        error='Enter valid no of videos greater or equal to 2'  

    return error  

def proceed(search,n_video,EndSec,out,mailid):
        print(search)
        print(n_video)
        print(EndSec)
        print(out)  
        StrtTime = 1*1000
        EndTime=EndSec*1000
        v_name=[]
        count=0
        video_id=[]
        audio_clip_paths=[]
        url=[]
        content=[]
        scrip=[]
        words=["songs","new+songs","old+songs",f"top{n_video}+songs",f"startup+songs"",hit+songs","beat+songs","best+songs","dance+songs","famous+songs"]
        query='+'.join(str(x) for x in search)
        for i in words:
            response=requests.get(f"https://www.youtube.com/results?search_query={query}+{i}").text
            soup=BeautifulSoup(response,'lxml')
            scrip.append(soup.find_all("script")[33])
        for script in scrip:
            json_text=re.search('var ytInitialData = (.+)[,;]{1}',str(script)).group(1)
            json_data=json.loads(json_text)
            content.append((
            json_data['contents']['twoColumnSearchResultsRenderer']['primaryContents']['sectionListRenderer']['contents'][0]['itemSectionRenderer']['contents']
            ))
        for k in content:    
            for data in k:
                for key,value in data.items():
                    if(type(value) is dict):
                        for k,v in value.items():
                            if k=="videoId" and len(v)==11:
                                if v in video_id:
                                    continue
                                video_id.append(v)
        for i in range(len(video_id)):
            url.append(f"https://www.youtube.com/watch?v={video_id[i]}")
        for link in url:
                try:
                    if(count==n_video):
                        break
                    link=link.strip()
                    vid = YouTube(link)
                    if vid.length>360 or vid.length<120:
                        continue
                    Yvideo = vid.streams.filter(file_extension='mp4')
                    v_name.append(vid.title)
                    Yvideo.get_lowest_resolution().download(output_path='./',filename=f"{count}.mp4")
                    count=count+1
                    st.write(f"link : {link}")
                    st.write(f'downloaded : {vid.title}')
                except:
                    pass
            ## st.write(f"break : {link}")
            ## url.remove(link)
            ##st.error("Connection problem please check your connection and try again")    
            ## st.stop()

        for j in range(count):
            video = VideoFileClip(f"{j}.mp4")
            audio = video.audio
            audio.write_audiofile(f"{j}.mp3")

        for k in range(count):
            file=f"{k}.mp3"
            sound = AudioSegment.from_file(file)
            audFile = MP3(file)
            p1 = sound[StrtTime: EndTime]
            p1.export(f'{k}.mp3', format='mp3')
        for p in range(count):
            audio_clip_paths.append(f'{p}.mp3')

        print(audio_clip_paths)
        clips = [AudioFileClip(c) for c in audio_clip_paths]
        final_clip = concatenate_audioclips(clips)
        final_clip.write_audiofile(out)
        
        with ZipFile(f'Mashup.zip','w',compression= ZIP_BZIP2 , allowZip64=True, compresslevel=9) as zip:
            zip.write(out)
        for f in range(count):
            os.remove(f'{f}.mp3')
            os.remove(f'{f}.mp4')
        try:
            fromaddr = "gsingh102003@gmail.com"
            toaddr = mailid
            msg = MIMEMultipart()
            msg['From'] = fromaddr
            msg['To'] = toaddr
            msg['Subject'] = "Mashup file"
            body = "Your mashup"
            msg.attach(MIMEText(body, 'plain'))
            attachment = open('Mashup.zip', "rb")
            p = MIMEBase('application', 'octet-stream')
            p.set_payload((attachment).read())
  
            # encode into base64
            encoders.encode_base64(p)
   
            p.add_header('Content-Disposition', "attachment; filename= %s" % "Mashup.zip")
  
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
            os.remove('Mashup.zip')
            st.success("Mashup successfully sent on mail")
        except:
            st.error("Mashup size exceeds the allowed size by Email please decrease number of videos or duration")
st.title("MASHUP GENERATOR")
with st.form("my_form"):
    search=st.text_input("Enter name of singer") 
    n_video=st.number_input("Enter number of videos",0,step= 1,format='%d')
    EndSec = st.number_input("Enter duration of each video (in seconds)",0,step= 1,format='%d')
    out=st.text_input("Enter name of output file", "output.mp3") 
    mailid=st.text_input("Enter Email Id") 
    submitted = st.form_submit_button("Submit")
    
    if submitted:
        st.write("text_input", search, "number_input", n_video,"number_input",EndSec,"text_input",out,"text_input",mailid)
        n_video=int(n_video)
        with st.spinner('Your mashup is in processing..It may take few minutes'):

            flag=check(search,n_video,EndSec,out,mailid)
            if(flag==True):
                proceed(search,n_video,EndSec,out,mailid)
            else:
                st.error(flag)
        st.success('Done!')    
    