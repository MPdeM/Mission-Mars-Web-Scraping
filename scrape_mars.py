from bs4 import BeautifulSoup as bs
import requests
from splinter import Browser
import time
import pandas as pd

def init_browser():
    # Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "./chromedriver"}
    return Browser("chrome", **executable_path, headless=False)

def scrape_info():
    browser = init_browser()
    # collecting the latest news from Nasa webpage
    url='https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    time.sleep(1)
    
    browser.visit(url)
    
    # import ipdb; ipdb.set_trace()

    soup = bs(browser.html, "html.parser")

    # results = soup.find_all('div', class_='slide')
    # titles = results.find('div', class_="content_title" ).a.text
    # parr =results.find_all('div', class_="rollover_description_inner")[0].text

    titles = soup.find('div', class_="content_title" ).a.text
    parr =soup.find_all('div', class_="rollover_description_inner")[0].text
    news_title= titles[1]
    news_p= parr[1]
    
# #scrap the link for the Featured Image from https://www.jpl.nasa.gov/spaceimages.
    url= 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    time.sleep(1)
    browser.visit(url)
    full_image_elem = browser.find_by_id('full_image')
    full_image_elem.click()
    time.sleep(2)
    soup = bs(browser.html, 'html.parser')
    img_element = soup.find('img', "fancybox-image")

    featured_image_url = 'https://www.jpl.nasa.gov'+ img_element['src']
    
# #scrap the latest tweet with Mars weather
    url= 'https://twitter.com/marswxreport?lang=en'

    response = requests.get(url)
    soup = bs(response.content, 'html.parser')
    #access the data inside the descendents from tweet class
    tweet_elem = soup.find_all('div', "tweet")
    mars_weather = tweet_elem[0].find('p', class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text

# use Pandas to scrape table containing facts about the planet

    url = 'https://space-facts.com/mars/'
    tables = pd.read_html(url)
    df=tables[2]
    df.columns = ['description', 'value']
    df.set_index('description', inplace=True)
    html_table = df.to_html()
    #df.to_html('table.html')

    # USGS Astrogeology obtain high resolution images for each of Mar's hemisphere

    url= 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    html = browser.html
    soup = bs(html, 'html.parser')
    elements = soup.find_all('div', class_="item")
    titles=[]
    urls = []
    for element in elements:
        
        title=element.h3.text
        partial_url =element.a['href']
        titles.append(title)
        urls.append('https://astrogeology.usgs.gov'+partial_url)

    #scrapeing the high resolution picture for the 4 elements using the bove URLs 

    url_hi_res =[]

    for eachURL in urls:
        browser.visit(eachURL)
        time.sleep(2)
        soup = bs(browser.html, 'html.parser')
        img_url = soup.find('div', 'downloads')
        pic=img_url.a['href']
        url_hi_res.append(pic)

    #dictionary with both title and image

    # data = {'titles': titles, 'imag_HR': url_hi_res}
    # hemi_image_urls= pd.DataFrame(data)
    hemi_image_urls=[]
    for key, val in zip(titles, url_hi_res):
        hemi_image_urls.append({key: val})


      # Store data in a dictionary
    mars_data = {
        "news_title": news_title,
        "news_p ": news_p,
        "featured_image_url": featured_image_url ,
        "mars_weather": mars_weather,
        "hemi_image_urls":hemi_image_urls,
        "html_table": html_table
    }
    print()
    # Close the browser after scraping
    browser.quit()

    # Return results
    return mars_data




