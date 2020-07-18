#Import dependencies
from bs4 import BeautifulSoup
import requests
import pandas as pd
import time
from urllib.request import urlopen
import re

def scrape():
    mars_info = {}

    # MARS NEWS
    url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    response = requests.get(url)

    #Create object
    soup = BeautifulSoup(response.content, 'html.parser')

    #Extract content titles from html
    title_results = soup.find_all("div", class_="content_title")

    #Loop through extracted titles to get the stripped text
    titles = []
    for title_result in title_results:
        text_titles = title_result.find('a').text.strip("\n")
        titles.append(text_titles)
    title = titles[0]

    mars_info.update({"Title": title})

    #Extract description paragraphs from html
    p_results = soup.find_all("div", class_="rollover_description_inner")

    paragraphs = []
    for p_result in p_results:
        text_paragraphs = p_result.text.strip("\n")
        paragraphs.append(text_paragraphs)
    paragraph = paragraphs[0]

    mars_info.update({"Description": paragraph})

    # FEATURED IMAGE

    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    img_response = requests.get(url)

    #Create object
    img_soup = BeautifulSoup(img_response.content, 'html.parser')


    #Extract base URL for site
    base_url = img_soup.find_all("div", class_="jpl_logo")
    base_url = str(base_url[0].a["href"].strip("//"))

    #Extract article from html to access image url
    img_results = img_soup.find_all("article")

    #Extract url path for featured imagee
    url = str(img_results[0]["style"].split(" ")[1].strip("url(';')"))
    
    #Concantenatet base url and featured image to get final path
    featured_image_url = f"http://{base_url}{url}"
    mars_info.update({"featured_url": featured_image_url})
    
    # MARS WEATHER NOT DONE
    # MARS FACTS
    
    url = "https://space-facts.com/mars/"
    #Read url as pandas tables
    tables = pd.read_html(url)
    mars_facts = tables[0]
    #Rename columns 
    mars_facts = mars_facts.rename(columns = {0: "Criteria", 1: "Value"})
    #Reset index
    mars_facts = mars_facts.set_index("Criteria")
    
    #Convert pandas table to html and update mars info dictionary
    html_table = mars_facts.to_html()
    mars_info.update({"Mars_Facts": html_table})
    
    # MARS HEMISPHERES

    h_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    h_response = requests.get(h_url)

    #Create object
    h_soup = BeautifulSoup(h_response.content, 'html.parser')
    
    #Scrape to get th base URL 
    base_url = h_soup.find_all("div", class_="left")
    base = base_url[0].a["href"].strip("/search")
    base_url = "h"+ base

    #Get item "class" to gather the location of all images
    imgs_count = h_soup.find_all("div", class_="item")
    
    #Loop through extracted class to get the image names
    links = []
    img_names = []
    for img in imgs_count:
        img_names.append(img.h3.text)
        links.append(img.a["href"])

    #Loop through concantenated base url and link extract to then scrape
    results_list = []
    for link in links:
        url = base_url+link
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        results = soup.find_all("div", class_="downloads")
        results_list.append(results)

    #Loop through the results to get each image url
    img_urls = []
    for result in results_list:
        lists = result[0].find_all("li")
        for l in lists:
            if l.a.text == "Sample":
                img_urls.append(l.a["href"])
    
    #Make a list of the keys I will need to make the dictionary
    keys =["title", "img_url"] 

    #Set all values in one list through a loop
    values = []
    for i in range(0,len(img_names)):
        values.append(img_names[i])
        values.append(img_urls[i])

    #Create dictionary by looping through values and keys lists previously created
    hemisphere_image_urls = []
    for v in zip(values[::2], values[1::2]):
        hemisphere_image_urls.append(dict(zip(keys, v)))
        
    mars_info.update({"Mars_Images": hemisphere_image_urls})

    return mars_info
