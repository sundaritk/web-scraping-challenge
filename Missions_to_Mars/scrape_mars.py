from bs4 import BeautifulSoup as bs
import requests
import pymongo
from splinter import Browser
import pandas as pd
import time

def scrape():
    executable_path={'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)

###  NASA Mars News ---
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    tlts=[]
    bdys=[]
    html = browser.html
    soup = bs(html, 'html.parser')

    results = soup.find_all(class_='slide')
    print("---Scraping Begins---")
    for result in results[:20]:
        tlt = result.find(class_='content_title').text.strip()
        bdy = result.find(class_='article_teaser_body').text.strip()
        tlts.append(tlt)
        bdys.append(bdy)
        #print(tlt)
        #print(bdy)
        print("---scraping---")
        try:
            #browser.click_link_by_partial_text('more')
            browser.links.find_by_partial_text('more')
        except:
            print("---Scraping Complete---")

# new title and details
    news_title=tlts[0]
    news_p=bdys[0]
    print(news_title)
    print(news_p)

### JPL Mars Space Images - Featured Image ---
    url2 = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url2)

#Find the full_image id and clicking on it 
    full_image_click = browser.find_by_id('full_image')
    full_image_click.click()

#Setting a wait time before clicking on more info
    more_info = browser.is_element_present_by_text('more info', wait_time=10)
    more_info = browser.links.find_by_partial_text('more info')
    more_info.click()

#Using Beautiful Soup to parse the html
    image_html = browser.html
    image_soup = bs(image_html, 'html.parser')

#Selecting html tag
    featured_image = image_soup.select_one('figure.lede a img').get('src')

#Making a long url
    featured_image_url = 'https://www.jpl.nasa.gov' + featured_image
    print(featured_image_url)


### Mars Weather ---

    url3 = 'https://twitter.com/marswxreport?lang=en'
    response_twtr = requests.get(url3)
    soup = bs(response_twtr.text, 'html.parser')
    mars_weathers = soup.find_all('p', class_="TweetTextSize")
    for tweet in mars_weathers:
        tweet.find('a').extract()
        if 'InSight sol' in tweet.text:
            mars_weather = tweet.text
            break

    print(f'Mars weather:\n{mars_weather}')

                                                                                                                                                                                                                                                   
### Mars Facts ---
                                                                                                                                                                                                                                        
    url4='https://space-facts.com/mars/'
    table = pd.read_html(url4)
    mars_facts = table[0]
    mars_fact = []
    for i in range(len(mars_facts[0])):
        mars_fact.append([mars_facts[0][i], mars_facts[1][i]])
    mars_fact

### Mars Hemispheres ---

    url4= 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url4)
    soup = bs(browser.html, 'html.parser')

    hemispheres_image_urls = []

    results_hemis = soup.find_all('div', class_='item')

    for item in results_hemis:
        title_hemis = item.h3.text
        first_url = url4[:30] + item.find('a', class_='itemLink')['href']
        browser.visit(first_url)
        soup = bs(browser.html, 'html.parser')
        time.sleep(1)
        final_url = url4[:30] + soup.find('img', class_='wide-image')['src']
        hemispheres_image_urls .append({'title': title_hemis, 'img_url':final_url})
    
    hemispheres_image_urls

    result = {
      'news_title': news_title,
      'news_paragraph': news_p,
      'featured_image': featured_image_url,
      'mars_weather' : mars_weather,
      'mars_table': mars_fact,
      'mars_hemispheres': hemispheres_image_urls
    }

    return result
