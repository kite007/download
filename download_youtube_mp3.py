from pytube import YouTube

import requests
from bs4 import BeautifulSoup
import os
import re
import time
import json

import ssl
ssl._create_default_https_context = ssl._create_stdlib_context

def extract_text_between_quotes(text):
    pattern = r'"(.*?)"'
    matches = re.findall(pattern, text)
    return matches  

#무료 효과음 다운로드 Free Sound Effects Download
url = 'https://youtube.com/playlist?list=PLyrrhz0LjbCLJme1-s3QFTHwXC_E81MO8'


with open('test2.html', 'r') as f:
    html = f.read()

soup = BeautifulSoup(html, 'html.parser')
ul_tag = soup.find_all('a', {'class':'yt-simple-endpoint style-scope ytd-playlist-video-renderer'}) 

pages = []
for item in ul_tag:
    result = extract_text_between_quotes(str(item))
    pages.append((url+result[1], result[3]))

for page in pages: 
    file_name = ".mp3"
    video = YouTube(page[0])
    audio_stream = video.streams.filter(only_audio=True).first()

    file_name = page[1].replace("/", "_")+ file_name
    audio_stream.download(output_path='./youtube', filename=file_name)


