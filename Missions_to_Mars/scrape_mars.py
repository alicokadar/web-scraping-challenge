from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import time

def scrape():
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)

    news_p,news_title=news(browser)

    all_data={
        "news_title":news_title,
        "news_p":news_p,
        "featured_image":featured_image(browser),
        "weather":weather(browser),
        "facts":facts(),
        "hemispheres":hemispheres(browser),
    }

    browser.quit()
    return all_data

def news(browser):
    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    news = soup.find("li", class_="slide")
    news_title = news.find('div', class_='content_title').text
    news_p = news.find('div', class_='article_teaser_body').text

    return news_p, news_title

def featured_image(browser):
    image_url="https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(image_url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    imgitems =soup.find("div",class_="img")
    path=imgitems.find("img")["src"]
    featured_image_url=f"https://www.jpl.nasa.gov{path}"
    return featured_image_url

def weather(browser):
    w_url="https://twitter.com/marswxreport?lang=en"
    browser.visit(w_url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    weather=soup.find("p",class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text
    return weather

def facts():
    fact_url="https://space-facts.com/mars/"
    fact_tables=pd.read_html(fact_url)

    fact_df=fact_tables[1]
    fact_df.columns=["","Value"]
    fact_html=fact_df.to_html(index=False,justify="center",classes="table table-striped table-hover table-dark table-bordered table-sm")
    return fact_html

def hemispheres(browser):
    hem_url="https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hem_url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    hemisphere_image_urls=list()

    num=0

    while num < 4:
        browser.is_text_present('Hemisphere', wait_time=5)
        xpath = '//div[@class="collapsible results"]/div[@class="item"]/a/img'
        hems=browser.find_by_xpath(xpath)
        hems[num].click()
        time.sleep(0.5)
        browser.is_text_present('Download', wait_time=5)
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        hem_img_dict=dict()
        hem_img_dict["title"]=soup.find("h2",class_="title").text.strip()
        hem_img_dict["url"]=soup.find("div",class_="downloads").a["href"]
        hemisphere_image_urls.append(hem_img_dict)
        num=num+1
        browser.back()
    return hemisphere_image_urls

if __name__ == "__main__":
    
     print(scrape())