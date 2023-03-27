import requests
from bs4 import BeautifulSoup
import os
import re
import time


def extract_text_between_parentheses(text):
    pattern = r'\((.*?)\)'
    matches = re.findall(pattern, text)
    return matches

def extract_text_between_backtick(text):
    pattern = r'`(.*?)`'
    matches = re.findall(pattern, text)
    return matches    

def download_file(url, save_directory):
    response = requests.get(url, verify=False)
    
    filename = url.split('/')[-1]
    filename = filename +'.mp3'

    if not os.path.exists(save_directory):
        os.makedirs(save_directory)

    with open(os.path.join(save_directory, filename), 'wb') as file:
        file.write(response.content)


#url = 'https://jinstale.tistory.com/category/효과음%20모음/특수효과음1070개'
url = 'https://jinstale.tistory.com/category/효과음%20모음/유용한효과음557개'
save_directory = 'downloaded_files'

page_response = requests.get(url)
soup = BeautifulSoup(page_response.content, 'html.parser')

ul_tag = soup.find_all('a', {'href':'javascript:;'})

page = []
for item in ul_tag:
    result = extract_text_between_backtick(str(item))
    page.append((result[2], result[3]))

pages = set(page)
for save_directory, url in pages:
    print(save_directory, url)
   
    page_response = requests.get(url)
    soup = BeautifulSoup(page_response.content, 'html.parser')

    pattern = r'"(.*?)"'
    file_list =[]
    file_links = soup.find_all('source')
    for item in file_links:
        result = re.search(pattern, str(item))
        file_list.append(result.group(1))
        if result:
            print(result.group(1))
            file_list.append(result.group(1))
        else:
            print("따옴표 사이의 문자열을 찾을 수 없습니다.")

        file_lists = set(file_list)
        for link in file_lists:
            print(link)
            download_file(link, save_directory)
            

