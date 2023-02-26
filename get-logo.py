
from bs4 import BeautifulSoup
import requests

def get_url(url):
    if not url.startswith("https://"):
        url="https://"+url
    html = requests.get(url).text
    soup = BeautifulSoup(html, 'html.parser')

    tags = soup.findAll('link')
    for tag in tags:
        href = ""
        if tag.has_attr('href'):
            href = tag['href']
        if "favicon" in href:
            if "http" not in href:
                href = url+href
            #print(href)
            return(href)
    tags=soup.findAll('img')
    count = 0
    for tag in tags:
        alt = ""
        src = ""
        if tag.has_attr('alt'):
            alt = tag['alt']
        if tag.has_attr('src'):
            src = tag['src']
        if "logo" in src.lower() or "logo" in alt.lower():
            if "http" not in src:
                src = url+src
            #print(src)
            return(src)
