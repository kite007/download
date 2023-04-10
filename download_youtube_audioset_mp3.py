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
import csv

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
soup = BeautifulSoup(page_response.content, 'html.parser')
ul_tag = soup.find_all('a', {'class': 'db'})

pages = []
for item in ul_tag:

    result = extract_text_between_quotes(str(item))
    url_list0 = url_eval + result[1]
    url_list1 = url_balanced + result[1]
    url_list2 = url_unbalanced + result[1]

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

    # print(page)

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

        # 스크롤을 끝까지 내리기
        last_height = driver.execute_script(
            "return document.body.scrollHeight")
        while True:
            driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(0.1)  # 로딩 대기
            new_height = driver.execute_script(
                "return document.body.scrollHeight")

            if new_height == last_height:
                break

            last_height = new_height

        # 웹 페이지의 HTML 소스 얻기
        html = driver.page_source

        # Beautiful Soup 객체 생성
        soup = BeautifulSoup(html, 'html.parser')

        # 웹 페이지에서 <div class="u" 부분 추출
        div_u_elements = soup.find_all('div', class_='u')

        # 정규표현식을 사용하여 두 번째 요소를 추출하기 위한 패턴
        pattern = re.compile(r'\"\w+\",(\"[\w\s,]+\")')

        file_list = []
        for div in div_u_elements:
            html = div.prettify()
            soup = BeautifulSoup(html, "html.parser")

            data_labels = soup.find('div', {'class': 'u'})['data-labels']
            second_elements = pattern.findall(data_labels)
            # 따옴표를 제거한 결과를 저장할 리스트
            
            # 따옴표를 제거한 결과를 저장할 리스트
            result = []

            # 각 요소에서 따옴표 제거
            for element in second_elements:
                result.append(element.strip("\""))

            data_ytid = soup.find('div', {'class': 'u'})['data-ytid']

            #clean_str = data_labels.replace('[', '').replace(']', '').replace('"', '').replace(',', '')
            
            file_list.append((result, yt_url+data_ytid, data_ytid+'.mp3'))
        
        _fielname = child_path+'.csv'
        
        with open(_fielname, 'w', newline='', encoding='utf-8') as csvfile:
            csv_writer = csv.writer(csvfile)
            for row in file_list:
                csv_writer.writerow(row)

        # print(file_list)

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
