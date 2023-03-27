from pytube import YouTube

import requests
from bs4 import BeautifulSoup
import os
import re
import time
import json

import ssl
ssl._create_default_https_context = ssl._create_stdlib_context

# def extract_text_between_parentheses(text):
#     pattern = r'\((.*?)\)'
#     matches = re.findall(pattern, text)
#     return matches

# def extract_text_between_backtick(text):
#     pattern = r'`(.*?)`'
#     matches = re.findall(pattern, text)
#     return matches    

def extract_text_between_quotes(text):
    pattern = r'"(.*?)"'
    matches = re.findall(pattern, text)
    return matches  

# def download_file(url, save_directory):
#     response = requests.get(url, verify=False)
    
#     filename = url.split('/')[-1]
#     filename = filename +'.mp3'

#     if not os.path.exists(save_directory):
#         os.makedirs(save_directory)

#     with open(os.path.join(save_directory, filename), 'wb') as file:
#         file.write(response.content)



# #url = 'https://jinstale.tistory.com/category/효과음%20모음'
# #url = 'https://jinstale.tistory.com/category/효과음%20모음/특수효과음1070개'
url = 'https://youtube.com/playlist?list=PLyrrhz0LjbCLJme1-s3QFTHwXC_E81MO8'


with open('test2.html', 'r') as f:
    html = f.read()

# Parse the HTML using BeautifulSoup
soup = BeautifulSoup(html, 'html.parser')
ul_tag = soup.find_all('a', {'class':'yt-simple-endpoint style-scope ytd-playlist-video-renderer'}) 

pages = []
for item in ul_tag:
    #print(item)
    result = extract_text_between_quotes(str(item))
    pages.append((url+result[1], result[3]))
    #print(url+result[1], result[3])


# Create a YouTube object

for page in pages: 
    file_name = ".mp3"
    #print(page[0], page[1])
    video = YouTube(page[0])

    # Get the audio stream of the video
    audio_stream = video.streams.filter(only_audio=True).first()

    #Download the audio stream as an MP3 file
    file_name = page[1].replace("/", "_")+ file_name
    #print(page[0], file_name)
    #print("===")
    audio_stream.download(output_path='./youtube', filename=file_name)


