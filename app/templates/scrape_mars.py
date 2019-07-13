from bs4 import BeautifulSoup as bs
from splinter import Browser

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
    try:
        news_title = soup.find("div", class_="content_title").text
        paragraph_text = soup.find("div", class_="rollover_description_inner").text
    except: AttributeError:
        return None, None
    
    return news_title, paragraph_text

def featured_image(browser):
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    full_image_elem = browser.find_by_id('full_image')
    browser.is_element_present_by_text('more info', wait_time=2)
    more_info_elem = browser.find_link_by_partial_text('more info')
    html = browser.html
    soup = bs(html, "html.parser")
    try:
        img_url_rel = soup.select_one('figure.lede a img').get("src")
    except: 
        AttributeError:
        return None, None
    return img_url

def mars_weather(browser):
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)
    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)
    html = browser.html
    soup = bs(html, "html.parser")
    try:
        mars_weather_tweet = soup.find('div', class_="js-tweet-text-container").text
    except: 
        AttributeError:
        return None, None
    return mars_weather_tweet

def mars_facts():
    url = "https://space-facts.com/mars/"
    mars_facts = pd.read_html(url)
    mars_facts_df = tables[0]
    mars_facts_df.columns = ['Category', 'Mars Facts', 'vs. Earth']

    return mars_facts_df

