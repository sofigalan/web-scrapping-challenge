from bs4 import BeautifulSoup as bs
from splinter import Browser
import requests
import pandas as pd


def init_browser(): 
    executable_path = {"executable_path": "chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)


def scrape():
    browser = init_browser()

    url = 'https://mars.nasa.gov/news/'
    response = requests.get(url)
    soup = bs(response.text,'html.parser')

    news_title = soup.find('div', class_= "content_title").find('a').text.strip()
    news_paragraph = soup.find('div', class_= "rollover_description_inner").text.strip()

    image_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(image_url)

    html_image = browser.html
    soup = bs(html_image, 'html.parser')

    featured_image_sub_url = soup.find('div',class_='carousel_items')('article')[0]['style'].\
        replace('background-image: url(','').replace(');','')[1:-1]

    main_url = 'https://www.jpl.nasa.gov'
    
    featured_image_url = main_url + featured_image_sub_url

    mars_weather_url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(mars_weather_url)
    
    mars_weather_html = browser.html
    
    mars_weather_soup = bs(mars_weather_html, 'lxml')
    
    mars_weather = mars_weather_soup.find('p', class_='tweet-text').text.split("pic")[0]
    
    mars_facts_url = 'https://space-facts.com/mars/'
    browser.visit(facts_url)

    mars_facts_table = pd.read_html(mars_facts_url)

    df = tables[1]

    df = df.rename(columns={0:'Fact',1:'Value'}).set_index('Fact').copy()

    mars_facts_html = df.to_html(index=False)
    
    hemi_base_url = 'https://astrogeology.usgs.gov'
    hemispheres_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemispheres_url)

    hemi_html = browser.html
    hemi_soup = bs(hemi_html, 'html.parser')
    items = hemi_soup.find_all('div', class_="item")
    hemi_img_dict = []

    for item in items:
        title = item.find('h3').text
        img_url = item.find('a', class_='itemLink product-item')['href']
        browser.visit(hemi_base_url + img_url)
        img_html = browser.html
        soup = bs(img_html, 'html.parser')
        img_url = hemi_base_url + soup.find('img', class_='wide-image')['src']
        hemi_img_dict.append(
            {
                "title":title,
                "img_url": img_url
            }
        )
    
    # Store data in a dictionary
    mars_data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image_url": featured_image_url,
        "mars_weather": mars_weather,
        "mars_facts_html": mars_facts_html,
        "hemi_img_dict": hemi_img_dict
    }

    # Close the browser after scraping
    browser.quit()

    # Return results
    return costa_data