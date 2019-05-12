# Mission to Mars
# University of Denver Data Analytics Bootcamp - Week 12
# Matthew Stewart
# May 12, 2019

# ------------------------------------------------------------------
# This python script represents a portion of the second half of the
# DU Data Analytics Bootcamp Week 12 homework.
# In this script, we will use a function called scrape() to
# scrape various information from the following sites:
#
# -- [NASA Mars News](https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest)
# -- [JPL Mars Space Images](https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars)
# -- [Mars Weather (Twitter)](https://twitter.com/marswxreport?lang=en)
# -- [Mars Facts](https://space-facts.com/mars/)
# -- [Mars Hemispheres](https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars)
#
# ------------------------------------------------------------------

# Dependencies
from bs4 import BeautifulSoup
import requests
import pandas as pd
from splinter import Browser
import time

def scrape():
    mars_data = {}

    # ---------------------------------------------------------------------
    # NASA Mars News
    # In this section, we will visit the NASA Mars News site and scrape the
    # title and paragraph text from the latest news story.
    #----------------------------------------------------------------------
    
    # URL
    mars_news_url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'

    # Make request to URL and create BeautifulSoup object
    mars_news_response = requests.get(mars_news_url)
    mars_news_soup = BeautifulSoup(mars_news_response.text, 'html.parser')

    # Scrape for title and paragraph text
    mars_news_latest = mars_news_soup.select('.slide')[0]
    mars_news_title = mars_news_latest.select('.content_title')[0].text.strip()
    mars_news_par = mars_news_latest.select('.rollover_description_inner')[0].text.strip()

    # Add to mars_data dictionary
    mars_data['news_title'] = mars_news_title
    mars_data['news_par'] = mars_news_par

    # ---------------------------------------------------------------------
    # JPL Mars Space Images
    # In this section, we will visit the JPL Mars Space Images site and
    # scrape the URL for the latest featured image.
    #----------------------------------------------------------------------

    # Splinter setup
    executable_path = {'executable_path': 'Resources/chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless = False)

    # URL
    jpl_space_images_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'

    # Use splinter to visit URL and navigate to "full image" page
    browser.visit(jpl_space_images_url)
    browser.click_link_by_partial_text('FULL IMAGE')

    # Further navigation to get to the full-sized image
    time.sleep(5)
    browser.click_link_by_partial_text('more info')

    # Create BeautifulSoup object
    html = browser.html
    jpl_soup = BeautifulSoup(html, 'html.parser')

    # Obtain endpoint for featured image URL (relative path)
    featured_image = jpl_soup.select('img.main_image')[0]
    featured_image_endpoint = featured_image['src']

    # Use slicing to concatentate the final URL
    featured_image_url = jpl_space_images_url.split('?')[0] + featured_image_endpoint[13:]

    # Add to mars_data dictionary
    mars_data['jpl_image_url'] = featured_image_url

    # ---------------------------------------------------------------------
    # Mars Weather (Twitter)
    # In this section, we will visit the Mars Weather Twitter site and
    # scrape the text of the latest Mars weather tweet.
    #----------------------------------------------------------------------

    # URL
    mars_weather_url = 'https://twitter.com/marswxreport?lang=en'

    # Make request to URL and create BeautifulSoup object
    mars_weather_response = requests.get(mars_weather_url)
    mars_weather_soup = BeautifulSoup(mars_weather_response.text, 'html.parser')

    # Scrape text
    mars_weather_tweet = mars_weather_soup.select('li.js-stream-item')[0]
    mars_weather = mars_weather_tweet.select('.js-tweet-text-container p')[0].text

    # Add to mars_data dictionary
    mars_data['weather_text'] = mars_weather

    # ---------------------------------------------------------------------
    # Mars Facts
    # In this section, we will visit the Mars Facts site and use pandas
    # to scrape the tabular data that includes diameter, mass, etc.
    #----------------------------------------------------------------------

    # URL
    mars_facts_url = 'https://space-facts.com/mars/'

    # Scrape tabular data
    mars_facts_tables = pd.read_html(mars_facts_url)

    # Create dataframe from tabular data (note that the above scraping yields only a single table)
    mars_facts_df = mars_facts_tables[0]
    mars_facts_df.columns = ['Description', 'Value']
    mars_facts_df.set_index('Description', inplace = True)

    # Export above dataframe to HTML table
    mars_facts_df.to_html('Resources/mars_table.html')

    # Convert above dataframe to dictionary for future storage
    mars_facts_dict = mars_facts_df.T.to_dict('list')

    # Iterate through each key/value pair and convert the value from a list to just the element in that list
    for k, v in mars_facts_dict.items():
        mars_facts_dict[k] = v[0]

    # Add to mars_data dictionary
    mars_data['facts'] = mars_facts_dict

    # ------------------------------------------------------------------------------
    # Mars Hemispheres
    # In this section, we will visit the Mars Hemispheres Enhanced Resolutions site
    # and scrape Title/Image URL information for the four Mars hemispheres.
    #-------------------------------------------------------------------------------

    # Four URLs
    mars_hem_cerberus_url = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/cerberus_enhanced'
    mars_hem_schiaparelli_url = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/schiaparelli_enhanced'
    mars_hem_syrtis_url = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/syrtis_major_enhanced'
    mars_hem_valles_url = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/valles_marineris_enhanced'

    # Four requests
    mars_hem_cerberus_response = requests.get(mars_hem_cerberus_url)
    mars_hem_schiaparelli_response = requests.get(mars_hem_schiaparelli_url)
    mars_hem_syrtis_response = requests.get(mars_hem_syrtis_url)
    mars_hem_valles_response = requests.get(mars_hem_valles_url)

    # Four BeautifulSoup objects
    mars_hem_cerberus_soup = BeautifulSoup(mars_hem_cerberus_response.text, 'html.parser')
    mars_hem_schiaparelli_soup = BeautifulSoup(mars_hem_schiaparelli_response.text, 'html.parser')
    mars_hem_syrtis_soup = BeautifulSoup(mars_hem_syrtis_response.text, 'html.parser')
    mars_hem_valles_soup = BeautifulSoup(mars_hem_valles_response.text, 'html.parser')

    # Cerberus scraping
    mars_hem_cerberus_content = mars_hem_cerberus_soup.select('.container')[0]

    # Cerberus title
    mars_hem_cerberus_title = mars_hem_cerberus_content.select('.content h2.title')[0].text.strip()[:-9]

    # Cerberus image URL
    mars_hem_cerberus_image = mars_hem_cerberus_content.select('img.wide-image')[0]['src']
    mars_hem_cerberus_image_url = mars_hem_cerberus_url[:29] + mars_hem_cerberus_image

    # Schiaparelli scraping
    mars_hem_schiaparelli_content = mars_hem_schiaparelli_soup.select('.container')[0]

    # Schiaparelli title
    mars_hem_schiaparelli_title = mars_hem_schiaparelli_content.select('.content h2.title')[0].text.strip()[:-9]

    # Schiaparelli image URL
    mars_hem_schiaparelli_image = mars_hem_schiaparelli_content.select('img.wide-image')[0]['src']
    mars_hem_schiaparelli_image_url = mars_hem_schiaparelli_url[:29] + mars_hem_schiaparelli_image

    # Syrtis Major scraping
    mars_hem_syrtis_content = mars_hem_syrtis_soup.select('.container')[0]

    # Syrtis Major title
    mars_hem_syrtis_title = mars_hem_syrtis_content.select('.content h2.title')[0].text.strip()[:-9]

    # Syrtis Major image URL
    mars_hem_syrtis_image = mars_hem_syrtis_content.select('img.wide-image')[0]['src']
    mars_hem_syrtis_image_url = mars_hem_syrtis_url[:29] + mars_hem_syrtis_image

    # Valles Marineris scraping
    mars_hem_valles_content = mars_hem_valles_soup.select('.container')[0]

    # Valles Marineris title
    mars_hem_valles_title = mars_hem_valles_content.select('.content h2.title')[0].text.strip()[:-9]

    # Valles Marineris image URL
    mars_hem_valles_image = mars_hem_valles_content.select('img.wide-image')[0]['src']
    mars_hem_valles_image_url = mars_hem_valles_url[:29] + mars_hem_valles_image

    # Create list of dictionaries using above titles and image URLs
    hemisphere_image_urls = [
        {
            'title': mars_hem_cerberus_title,
            'img_url': mars_hem_cerberus_image_url
        },
        
        {
            'title': mars_hem_schiaparelli_title,
            'img_url': mars_hem_schiaparelli_image_url
        },
        
        {
            'title': mars_hem_syrtis_title,
            'img_url': mars_hem_syrtis_image_url
        },
        
        {
            'title': mars_hem_valles_title,
            'img_url': mars_hem_valles_image_url
        }
    ]

    # Add to mars_data dictionary
    mars_data['hemisphere_image_url'] = hemisphere_image_urls

    # Function output
    return mars_data