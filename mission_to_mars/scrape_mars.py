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
    title = ["cerberus","schiaparelli","syrtis","valles"]
    url4 = "https://marshemispheres.com/"
    hempishere_urls = []
    for x in range(0, len(title)):
        browser.visit(f"{url4}{title[x]}.html")
        hem_img_html = browser.html
        hem_img_soup = bs(hem_img_html, 'html.parser')
        hem_img_url = hem_img_soup.find('div', attrs={'id':'wide-image'}).find('img', class_="wide-image").get('src')
        hempishere_urls.append(f"{url4}{hem_img_url}")

    hemisphere_img_urls = []
    for x in range(0,len(title)):
        each_dict = {'title':title[x], 'url':hempishere_urls[x]}
        hemisphere_img_urls.append(each_dict)

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
