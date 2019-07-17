from bs4 import BeautifulSoup as bs
from splinter import Browser
import pandas as pd
import time 

def scrape_all():
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)

    news_title, paragraph_text= mars_news(browser)
    
    data = {
        "news_title": news_title,
        "news_paragraph": paragraph_text,
        "featured_image": featured_image(browser),
        "mars_weather": mars_weather_tweet(browser),
        "mars_facts": mars_facts(),
        "mars_hemispheres": mars_hemispheres(browser)
    }

    return data

def mars_news(browser):
    url = "https://mars.nasa.gov/news/" 
    browser.visit(url)
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)
    html = browser.html
    soup = bs(html, 'html.parser')
    news_title = soup.find("div", class_="content_title").text
    paragraph_text = soup.find("div", class_="rollover_description_inner").text
    
    
    return news_title, paragraph_text

def featured_image(browser):
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    full_image_elem = browser.find_by_id('full_image')
    browser.is_element_present_by_text('more info', wait_time=2)
    more_info_elem = browser.find_link_by_partial_text('more info')
    html = browser.html
    soup = bs(html, "html.parser")
    img_url_rel = soup.select_one('figure.lede a img').get("src")
    
    return img_url

def mars_weather(browser):
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)
    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)
    html = browser.html
    soup = bs(html, "html.parser")
    mars_weather_tweet = soup.find('div', class_="js-tweet-text-container").text
    
    return mars_weather_tweet

def mars_facts():
    url = "https://space-facts.com/mars/"
    mars_facts = pd.read_html(url)
    mars_facts_df = tables[0]
    mars_facts_df.columns = ['Category', 'Mars Facts', 'vs. Earth']

    return mars_facts_df

def mars_hemispheres(browser):
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    html = browser.html
    soup = bs(html, 'html.parser')
    mars_hemisphere = []
    links = soup.find_all('div', class_='item')
    for link in links:
        mars_hemisphere.append(link.text)
    image_urls = []
    mars_url = 'https://astrogeology.usgs.gov'
    for image in links:  
        title = image.find('h3').text
        partial_img =image.find('a', class_='itemLink product-item')['href']
        browser.visit(mars_url + partial_img)
        img_html = browser.html
        soup = bs(img_html, 'html.parser')
        image_url = mars_url + soup.find('img', class_='wide-image')['src']
        image_urls.append({"title" : title, "image_url" : image_url})
       
    return mars_hemispheres