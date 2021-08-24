import requests
from bs4 import BeautifulSoup
from requests.models import Response
import textstat

site = 'https://academy.pega.com/challenge/adding-optional-actions-workflow/v3'

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
    return len(soup.find_all(attrs={'class': 'media media--type-image media--view-mode-embedded ds-1col clearfix'}))

#h5p factor
def h5p_count(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    return len(soup.find_all(attrs={'class':'h5p-iframe'}))

#video factor
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

#Download the latest chrome from https://chromedriver.chromium.org/downloads and update the location
chrome_driver_path = "C:\\Users\\rncal\\Downloads\\chromedriver"
url = site

#chrome options to run it in headless
chrome_options = Options()
chrome_options.add_argument('--headless')
webdriver = webdriver.Chrome(
  executable_path=chrome_driver_path, options=chrome_options
)

#Opens Chrome in headless mode to get page source
with webdriver as driver:
    driver.get(url)
    driver.implicitly_wait(5)
    #print(driver.page_source)
    soup = BeautifulSoup(driver.page_source, 'lxml')
    #print(soup)
    driver.close()

#Search the code for video durations
divs = soup.find("div", { "class" : "video-meta__item video-meta__item--duration" })
time=divs.text
timetotal = (sum(x * int(t) for x, t in zip([3600, 60, 1], time.split(":"))))

#if you have multiple videos in a single url, use for loop
#for div in divs:
    #print(div.text)

#Technical Page Score formula
tps = ((readability) + (image_count(site)*2) +(h5p_count(site)*3.5) + (int(timetotal/60)/10))

#crawl the challenge or topic title
title = soup.find(attrs={'class': 'u-bolt-inline c-bolt-text c-bolt-text--bold c-bolt-text--normal c-bolt-text--small'})
titletext = title.text   

#uncomment print statements to verify output
print ('==================================')
print ('Gunning Fog Index =',(readability)) 
print ('Total images =', image_count(site))
print ('Total H5Ps =', h5p_count(site)) 
print ('Total Video Duration =', timetotal/60)
print ('----------------------------------')
print ('Technical Page Score for', titletext,'=', tps)
print ('==================================')
