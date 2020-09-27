from bs4 import BeautifulSoup
import requests
import pandas as pd
from flask import Flask
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager


def init_browser():
    executable_path = {"executable_path": ChromeDriverManager().install()}
    return Browser('chrome', **executable_path, headless=False)

mars_dict = {}

def scrape():
    browser=init_browser()
        
    #article + paragraph
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    html=browser.html
    soup = BeautifulSoup(html,'html.parser')
    title = soup.find_all('div',class_='content_title')[0].text
    paragraph = soup.find_all('div',class_='rollover_description_inner')[0].text
    mars_dict['news_title'] = title
    mars_dict['news_paragraph'] = paragraph


    #image 
    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)
    html=browser.html
    soup = BeautifulSoup(html,'html.parser')
    image_url = soup.find('article')['style'].replace('background-image: url(','').replace(');', '')[1:-1]
    base_url = 'https://www.jpl.nasa.gov'
    featured_image_url = base_url + image_url
    mars_dict['featured_image_url'] = featured_image_url


    #facts
    url = 'https://space-facts.com/mars/'
    browser.visit(url)
    html=browser.html
    soup = BeautifulSoup(html,'html.parser')
    table = pd.read_html(url)
    mars_table_df = table[0]
    mars_table_html = mars_table_df.to_html(classes='table table-striped')
    mars_dict['mars_facts'] = mars_table_html


    #hemispheres
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    hemispheres = soup.find_all('div', class_='item')
    hemispheres_list = []
    base_url = 'https://astrogeology.usgs.gov'

    for data in hemispheres:
        title = data.find('h3').text
        hemisphere_url = data.find('a', class_='itemLink product-item')['href']
        browser.visit(base_url + hemisphere_url)
        page2_html = browser.html
        soup = BeautifulSoup(page2_html, 'html.parser')
        image_url = soup.find('img',class_='wide-image')['src']
        full_image_url = base_url + image_url
        hemispheres_list.append({"title":title,"img_url":full_image_url})

    mars_dict['hemispheres'] = hemispheres_list

    return mars_dict
