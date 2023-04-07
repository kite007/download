import pytube

from pytube import YouTube
from pytube.exceptions import VideoUnavailable

import requests
from bs4 import BeautifulSoup
import os
import re
import time
import json

import ssl

import os

from urllib.parse import urlparse

import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By


chrome_driver_path = "/Users/a07874/Downloads/chromedriver_mac_arm64/chromedriver"
driver = webdriver.Chrome(executable_path=chrome_driver_path)

ssl._create_default_https_context = ssl._create_stdlib_context


def extract_text_between_quotes(text):
    pattern = r'"(.*?)"'
    matches = re.findall(pattern, text)
    return matches


# 무료 효과음 다운로드 Free Sound Effects Download
url = 'https://research.google.com/audioset/dataset/index.html'

url_info = 'https://research.google.com/audioset/dataset/'
url_eval = "https://research.google.com/audioset/eval/"
url_balanced = "https://research.google.com/audioset/balanced_train/"
url_unbalanced = "https://research.google.com/audioset/unbalanced_train/"

yt_url = "https://youtu.be/"

save_directory = 'audioset'


page_response = requests.get(url)
# print(page_response.content)
soup = BeautifulSoup(page_response.content, 'html.parser')
ul_tag = soup.find_all('a', {'class': 'db'})

pages = []
for item in ul_tag:
    # print(item)
    result = extract_text_between_quotes(str(item))
    url_list0 = url_eval + result[1]
    url_list1 = url_balanced + result[1]
    url_list2 = url_unbalanced + result[1]
    # print(url_list0, url_list1, url_list2)
    pages.append((url_list0, url_list1, url_list2))


for page in pages:
    # URL에서 파일명을 추출
    parsed_url = urlparse(page[0])
    file_path = parsed_url.path

# 파일명에서 확장자를 제거
    parent_directory = os.path.splitext(os.path.basename(file_path))[0]

    print(parent_directory)

    if not os.path.exists(parent_directory):
        os.mkdir(parent_directory)

    #print(page)

    for item in page:
        # URL을 '/'로 분할
        url = item
        parts = url.split('/')

        # 필요한 부분을 선택
        part1 = parts[-2]
        part2 = parts[-1].split('.')[0]

        # 문자열 합치기
        child_directory = f"{part1}_{part2}"
        print(child_directory)

        child_path = os.path.join(parent_directory, child_directory)
        if not os.path.exists(child_path):
            os.mkdir(child_path)

        
        driver.get(url)

        # 웹 페이지의 HTML 소스 얻기
        html = driver.page_source
    
        # Beautiful Soup 객체 생성
        soup = BeautifulSoup(html, 'html.parser')

        # 웹 페이지에서 <div class="u" 부분 추출
        div_u_elements = soup.find_all('div', class_='u')


        file_list = []
        for div in div_u_elements:
            html = div.prettify()
            soup = BeautifulSoup(html, "html.parser")
  
            data_labels = soup.find('div', {'class': 'u'})['data-labels']
            data_ytid = soup.find('div', {'class': 'u'})['data-ytid']

            
            file_list.append((data_labels, yt_url+data_ytid, data_ytid+'.mp3'))

        #print(file_list)

        for _file in file_list:
            file_name = _file[2]
            if not os.path.exists(child_path+'/'+file_name):
                try: 
                    video = YouTube(_file[1])
                    audio_stream = video.streams.filter(only_audio=True).first()

                    audio_stream.download(output_path=child_path, filename=file_name)
                except VideoUnavailable:
                    print("VideoUnavailable!!! ", child_path, file_name)
                    continue
            else:
                print("이미 다운로드 받았음!! ", child_path, file_name)