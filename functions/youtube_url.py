import requests
from bs4 import BeautifulSoup
import re


async def get_channel_url_by_short_url(channel_id):
    channel_url = f'https://www.youtube.com/{channel_id}'
    return channel_url

async def get_channel_title(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    search = soup.find('title').text
    return search.replace(' - YouTube', '')


def parse_filter(data_list):
    filter_list = []
    for i in data_list:
        if i not in filter_list:
            filter_list.append(i)
    return filter_list

async def url_corrector(url):
    url = url.replace('featured', 'videos')
    if 'videos' not in url:
        url = url + '/videos'
    return url

async def parse_videos(url):
    correct_url = await url_corrector(url)
    response = requests.get(correct_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    search = soup.find_all('script')
    key = '"videoId":"'
    data = re.findall(key +r'([^*]{11})', str(search))
    return data[0]


async def get_channel_url_id_by_url(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    search = soup.find(href=re.compile("https://www.youtube.com/"), rel="canonical")['href']
    return search


async def get_video_url_by_id(video_id: str) -> str:
    return f'https://www.youtube.com/watch?v={video_id}'

def parse_videos_test(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    search = soup.find(href=re.compile("https://www.youtube.com/"), rel="canonical")['href']
    return search

#print(parse_videos_test('https://www.youtube.com/@StarGameWF'))
#print(parse_videos_test('https://www.youtube.com/c/stayugly_/videos'))