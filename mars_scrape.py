# Importing dependancies 
import pandas as pd
import requests
from splinter import Browser
from bs4 import BeautifulSoup as bs
import time

# Creating a function to use the browser in the main function
def init_browser():
    executable_path = {"executable_path": "chromedriver.exe"}
    return Browser('chrome', **executable_path, headless=False)

# Scraping function
def scrape():
    
    #*******************Scraping the NASA Mars News Website***********************************************************************************
    browser = init_browser()
    
    # Go to NASA URL
    news_url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser.visit(news_url)
    time.sleep(4)

    # Getting the HTML and the Soup object
    html = browser.html
    news_soup = bs(html, "html.parser")

    # Retrieve the most recent article 
    result = news_soup.find('div', class_='list_text')
    latest_article = result.find('div', class_='content_title').text
    latest_article_paragraph = result.find('div', class_='article_teaser_body').text

    # Quit browser
    browser.quit()

    #***********************************Scraping the JPL Images*********************************************************************************
    browser = init_browser()

    # Go the Mars Space image URL and visit the website
    image_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    
    browser.visit(image_url)
    time.sleep(2)
    browser.click_link_by_partial_text('FULL IMAGE')
    time.sleep(2) 
    browser.click_link_by_partial_text('more info')
    
    # HTML and Soup object
    html = browser.html
    jpl_soup = bs(html, "html.parser")
    
    # Finding the image and link of the image
    featured_image = jpl_soup.find('figure', class_='lede').find(class_='main_image')['src']
    featured_image_url = "https://www.jpl.nasa.gov"+featured_image 
    
    print(featured_image_url)
    
    browser.quit()
    #***********************************Mars Twitter - Table**********************************************************************
    browser = init_browser()
    twitter_url = 'https://twitter.com/marswxreport?lang=en'
    
    browser.visit(twitter_url)
    time.sleep(4)
    twitter_html = browser.html
    
    twitter_soup = bs(twitter_html, 'html.parser')
    results = twitter_soup.find_all('span')
    lines = [span.get_text() for span in results]
    weather = []

    for line in lines:
        if "InSight" in line:
            weather.append(line)
    mars_weather = weather[0]
    print(mars_weather)
    
    browser.quit()
    
    #***********************************Mars Facts - Table*********************************************************************************
    # Go the Mars Space image URL and visit the website
    mars_fact_url = 'https://space-facts.com/mars/' 
    
    mars_facts = pd.read_html(mars_fact_url)

    # Setting up the dataframe
    mars_df = mars_facts[0]
    mars_df.columns = ['Description', 'Value']
    mars_df.set_index('Description', inplace=True)

    # Converting the DataFrame to HTML
    mars_html_table = mars_df.to_html(header=True, index=True)
    

    #***********************************Mars Hemisphere********************************************************************************
    browser = init_browser()

    # Go the Mars Space image URL and visit the website
    hemisphere_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemisphere_url)

    # HTML and Soup object
    html = browser.html
    hemisphere_soup = bs(html, "html.parser")

    # Empty list to populate with dictionaries
    hemisphere_urls = []
    hemisphere_results = hemisphere_soup.find_all('div', class_='item')

    base_url = 'https://astrogeology.usgs.gov'

    for result in hemisphere_results:
        title = result.find('h3').text
        small_image_url = result.find('a', class_='itemLink product-item')['href']
        browser.visit(base_url + small_image_url)

        # Get the URL for the small-sized image
        small_image_url = browser.html

        # Parse the URL
        hemisphere_soup = bs(small_image_url, "html.parser")

        img_url = base_url + hemisphere_soup.find('img', class_='wide-image')['src']

        # Populating the list wth dictionaries
        hemisphere_urls.append({'Title':title, 'Image': img_url})

    # Mars Data Dictionary - MongoDB********************************************************************************
    mars_data = {
        "news_title":latest_article,
        "news_paragraph":latest_article_paragraph,
        "featured_image":featured_image,
        "featured_image_url":featured_image_url,
        "mars_weather": mars_weather,
        "mars_facts":mars_html_table,
        "hemisphere_urls": hemisphere_urls
    }
    print('Finished Scraping')
    browser.quit()
    return mars_data
