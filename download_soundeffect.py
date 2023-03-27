import requests
from bs4 import BeautifulSoup
import os
import re
import time

home = "https://soundeffect-lab.info/sound/anime/"

def extract_text_between_parentheses(text):
    pattern = r'\((.*?)\)'
    matches = re.findall(pattern, text)
    return matches

def extract_text_between_backtick(text):
    pattern = r'`(.*?)`'
    matches = re.findall(pattern, text)
    return matches    

def extract_text_between_lessthen(text):
    pattern = r'>(.*?)<'
    matches = re.findall(pattern, text)
    return matches    

def extract_text_between_quotes(text):
    pattern = r'"(.*?)"'
    matches = re.findall(pattern, text)
    return matches    

def download_file(url, save_directory):
    response = requests.get(url, verify=False)
    
  
    filename = url.split('/')[-1]
    filename = filename +'.mp3'
    _save_directory = save_directory.replace("/", "_")
    print(_save_directory)
    if not os.path.exists(_save_directory):
        os.makedirs(_save_directory)

    with open(os.path.join(_save_directory, filename), 'wb') as file:
        file.write(response.content)

def listToString(str_list):
    result = ""
    for s in str_list:
        result += s + " "
    return result.strip()

url = "https://soundeffect-lab.info/sound/anime/"
save_directory = 'mp3'

page_response = requests.get(url, verify=False)
soup = BeautifulSoup(page_response.content, 'html.parser')


page = []

a_tag = soup.select('a[href^="mp3/"]') 
for item in a_tag:
    print("============")
    filename = item.get('href')
    url = home + filename

    download_file(url, save_directory)
