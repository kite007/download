import requests
from bs4 import BeautifulSoup
import os
import re

url = 'https://jinstale.tistory.com/category/효과음%20모음'
save_directory = 'downloaded_files'

def download_file(url, save_directory):
    response = requests.get(url, verify=False)
    filename = url.split('/')[-1]

    if not os.path.exists(save_directory):
        os.makedirs(save_directory)

    with open(os.path.join(save_directory, filename), 'wb') as file:
        file.write(response.content)

page_response = requests.get(url)
#print(page_response.content)
soup = BeautifulSoup(page_response.content, 'html.parser')


pattern = r'"(.*?)"'
file_list =[]
file_links = soup.find_all('source')
for item in file_links:
    print(item)
    result = re.search(pattern, str(item))
    file_list.append(result.group(1))
    if result:
        print(result.group(1))
        file_list.append(result.group(1))
    else:
        print("따옴표 사이의 문자열을 찾을 수 없습니다.")

#print(file_list)

for link in file_list:
    print(link)
    #file_url = link.get('href')
    download_file(link, save_directory)