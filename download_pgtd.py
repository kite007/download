# https://pgtd.tistory.com/


import requests
from bs4 import BeautifulSoup
import os
import re
import time

home = "https://pgtd.tistory.com"

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

#url = 'https://jinstale.tistory.com/category/효과음%20모음'
#url = 'https://jinstale.tistory.com/category/효과음%20모음/특수효과음1070개'
url = 'https://pgtd.tistory.com/'
save_directory = 'downloaded_pgtd'

page_response = requests.get(url)
#print(page_response.content)
soup = BeautifulSoup(page_response.content, 'html.parser')


page = []

ul_tag = soup.find_all('a', {'class':'link-article'}) #ul_tag = soup.find_all('a', {'class':'link-article'})
#print(ul_tag)
for item in ul_tag:
    print("============")
    print(item)
    result = extract_text_between_quotes(str(item))
    file_page = home + result[1]
    print(file_page)
    descriptions = item.find_all('strong', {'class':'title'})
    description= extract_text_between_lessthen(str(descriptions))
    descr = listToString(description)
    print(descr, file_page)
    if len(descr)!=0 :
        page.append((descr, file_page))


pages = set(page)
for save_directory, url in pages:
    print(save_directory, url)
   
    page_response = requests.get(url)
    soup = BeautifulSoup(page_response.content, 'html.parser')


    pattern = r'"(.*?)"'
    file_list =[]
    file_links = soup.find_all('source')
    for item in file_links:
        #print(item)
        result = re.search(pattern, str(item))
        file_list.append(result.group(1))
        if result:
            print(result.group(1))
            file_list.append(result.group(1))
        else:
            print("따옴표 사이의 문자열을 찾을 수 없습니다.")

 
        file_lists = set(file_list)
        for link in file_lists:

            print(save_directory)
            download_file(link, save_directory)
            



