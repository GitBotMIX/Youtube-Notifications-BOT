import requests
from bs4 import BeautifulSoup
import re


async def check(url):
    try:
        title_text = title_textF(url)
    except:
        return False
    if 'https://www.youtube.com/c/' not in url and 'https://www.youtube.com/channel/' not in url\
            and 'https://www.youtube.com/user/' not in url:
        return False
    if 'https://www.youtube.com/' in url:
        if '404 Not Found' not in title_text:
            return title_text.replace(' - YouTube', '')
    return False


def title_textF(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    search = soup.find('title').text
    key = '"videoId":"'
    #data = parse_filter(re.findall(key +r'([^*]{11})', str(search)))
    return search


def parse_filter(data_list):
    filter_list = []
    for i in data_list:
        if i not in filter_list:
            filter_list.append(i)
    return filter_list

async def url_corrector(url):
    print(url)
    url = url.replace('featured', 'videos')
    if 'featured' not in url and 'videos' not in url:
        url = url + '/videos'
    print(url)
    return url

async def parse_videos(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    search = soup.find_all('script')
    key = '"videoId":"'
    data = re.findall(key +r'([^*]{11})', str(search))
    return data[0]

def parse_videos_test(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    search = soup.find_all('script')
    key = '"videoId":"'
    data = re.findall(key +r'([^*]{11})', str(search))
    return data

#print(parse_videos_test('https://www.youtube.com/c/stayugly_/videos'))