import requests
from bs4 import BeautifulSoup
from requests.models import Response
import textstat


site = ('https://this-is-a-webpage-url')

#readability factor
def CleanText(text):
    text = str(text)
    forbidden = [r'\n', r'.', r'?', r'!', r'(', r')']
    for i in forbidden:
        text.replace(i, '')
    return text

def pagetext(url):
    r = requests.get(url, allow_redirects=False)
    soup = BeautifulSoup(r.content, 'html.parser')
    words = CleanText(soup.text.lower())
    return words

target = pagetext(site)
readability = textstat.gunning_fog(target)

#image factor
def image_count(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    return len(soup.find_all('img'))

#h5p factor
def h5p_count(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    return len(soup.find_all(attrs={'class':'h5p-iframe'}))

#video factor

#outputs 
print ('Gunning Fog Index =',(readability))
print ('Total images =', image_count(site))
print ('Total H5Ps =', h5p_count(site))


#--[
# Page Density = (total number of words on page) x (Gunning Fog index) x 
# ((#image * .25)+(#h5p * .5)) x (video duration in s * .15) / 100 
# ]
