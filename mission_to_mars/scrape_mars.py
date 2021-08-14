# Importing dependencies
from bs4 import BeautifulSoup as bs
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

def scrape():
    #Set up splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    # Visit URL
    url = "https://redplanetscience.com/"
    browser.visit(url)

    # Scrape data into Soup
    html = browser.html
    soup = bs(html, 'html.parser')

    # Scrape news title and paragraph
    news_title = soup.find('div', class_="content_title").get_text()
    news_p = soup.find('div', class_="article_teaser_body").get_text()

    # Visit another URL
    url2 = "https://spaceimages-mars.com/"
    browser.visit(url2)

    # Scrape data into Soup
    img_html = browser.html
    img_soup = bs(img_html, 'html.parser')

    # Grab url for featured image
    featured_img_url = url2 + img_soup.find('div', class_="header").find('img' , class_="headerimage fade-in").get('src')

    # Visit another url
    url3 = "https://galaxyfacts-mars.com/"

    # Use pandas to read html
    tables = pd.read_html(url3)

    # Use table 1 from the list of dataframes, drop columns and rows that are not required
    df = tables[0]
    df = df.drop(columns=[2])
    df = df.drop([0])
    df = df.rename(columns={0 : "Mars - Particulars", 1:"Details"})

    # Convert dataframe to html
    html_table = df.to_html(classes="table")

    # High resolution Images List
    hemisphere_img_urls = [
                            {"title":"Cerebus", "url":"https://marshemispheres.com/images/f5e372a36edfa389625da6d0cc25d905_cerberus_enhanced.tif_full.jpg"},
                            {"title":"Schiaparelli", "url":"https://marshemispheres.com/images/3778f7b43bbbc89d6e3cfabb3613ba93_schiaparelli_enhanced.tif_full.jpg"},
                            {"title":"Syrtis", "url":"https://marshemispheres.com/images/555e6403a6ddd7ba16ddb0e471cadcf7_syrtis_major_enhanced.tif_full.jpg"},
                            {"title":"Valles", "url":"https://marshemispheres.com/images/b3c7c6c9138f57b4756be9b9c43e3a48_valles_marineris_enhanced.tif_full.jpg"}
                        ]

    final_data = {
        'title' : news_title,
        'paragraph' : news_p,
        'feature_img': featured_img_url,
        'table': html_table, 
        'images': hemisphere_img_urls
    }

    
    # Close the browser after scraping
    browser.quit()

    # Return results
    return final_data
