import requests
import re
from bs4 import BeautifulSoup
import random
import time


def extract_news(parser):
    """ Extract news from a given web page """
    news_list = []
    HeadsAndLinks = parser.find_all("a", class_="storylink")
    Scores = parser.find_all("span", class_="score")
    Authors = parser.find_all("a", class_="hnuser")
        
    
    for i in range(len(HeadsAndLinks)):
        d = {}
        str1 = re.split('<|>|"', str(HeadsAndLinks[i - 1]))
        
        if str1[8] == "nofollow":
            continue
        else:
            d['url'] = str1[4]
               
            d['title'] = str1[8]
            if str1[8] == '':
                d['title'] = str1[6]
            str2 = re.split('<|>|"', str(Scores[i - 1]))
            raw_score = str2[6].split()
            d['points'] = raw_score[0]
            str3 = re.split('<|>|"', str(Authors[i - 1]))
            d['author'] = str3[6]

            news_list.append(d)
    return news_list


def extract_next_page(parser):
    """ Extract next page URL """
    link = str(parser.find("a", class_="morelink"))
    Array = link.split()
    s = str(Array[2])
    next_page_and_amp = s[6:-1]
    next_page_url = next_page_and_amp[:next_page_and_amp.find('amp;')]+next_page_and_amp[next_page_and_amp.find('amp;')+4:]
    return next_page_url


def get_news(url, n_pages=1):
    """ Collect news from a given web page """
    news = []
    while n_pages:
        print("Collecting data from page {}".format(url))
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        news_list = extract_news(soup)
        next_page = extract_next_page(soup)
        url = "https://news.ycombinator.com/" + next_page
        news.extend(news_list)
        n_pages -= 1
        time.sleep(random.randint(5,10))
    return news




