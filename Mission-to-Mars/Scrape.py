# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import datetime as dt

def scrape_all():
# Create executable path
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)
    news_title, news_paragraph = mars_news(browser)
    # Run all scraping functions and store results in dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now(),
        "hemispheres": mars_hemispheres(browser)
    }
    # Stop Webdriver and return data 
    browser.quit()
    return data 

# function to scrape mars news 
def mars_news(browser):
 # Scrape Mars News 
    url = 'https://redplanetscience.com'
    browser.visit(url)
        # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)
        # setting variables to parse the html
    html = browser.html
    news_soup = soup(html, 'html.parser')
            # Try and except Scrape Error handling 
    try:
        # parent element finder
        slide_elem = news_soup.select_one('div.list_text')
            #find title
        news_title=slide_elem.find('div',class_='content_title').get_text()
            #find description 
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
    except AttributeError:
        return None, None 
    return news_title, news_p
    

    # function for scraping images 
def featured_image(browser):
        #Visit URL
    url = 'https://spaceimages-mars.com'
    browser.visit(url)
        # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()
        # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')
        # add try/except for error handling to scrape 
    try:
            # Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
    except AttributeError:
        return None
            # Use the base URL to create an absolute URL
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'

    return img_url

 # function for scraping Mars Facts 
def mars_facts():
    try: 
        # read html into df
        df = pd.read_html('https://galaxyfacts-mars.com')[0]  
    except BaseException:
        return None 
        # Assign columns and set index of dataframe
    df.columns=['Description', 'Mars', 'Earth']
    df.set_index('Description', inplace=True)
        # create html codefor creating a table from a df
    return df.to_html()

# hemisphere urls

def mars_hemispheres(browser):

    # 1. Use browser to visit the URL 
    url = 'https://marshemispheres.com/'

    browser.visit(url)

    # 2. Create a list to hold the images and titles.
    hemisphere_image_urls = []

    # Convert the browser html to a soup object
    html = browser.html

    title_soup = soup(html, 'html.parser')

    # Titles are on the first page so get them first using the 'h3' tag.
    # The parent of each title element will be used to get the html page for the image.
    title_elems = title_soup.find_all('h3')

    # 3. Write code to retrieve the image urls and titles for each hemisphere.
    for title_elem in title_elems:
        
        # If title == 'Back' we are done with the list of titles.
        # Alternatively, we could use the parent to get the last href = '#'
        # We also need to skip elements that have blank titles.
        if title_elem.text == 'Back':
            break
        elif title_elem.text == '':
            continue

        # Get the html page to visit in order to find the image
        image_url = title_elem.parent['href']
        
        # Save the title
        image_title = title_elem.text

        # Get the full path to the html page
        image_url = f"{url}{image_url}"
        
        # Go to the url where the image info is located:
        browser.visit(image_url)
        
        # Convert the new html page to a soup object
        html = browser.html
        image_soup = soup(html, 'html.parser')

        # Get the 'a' tag where it's text = 'Sample':
        image_url = image_soup.find('a', text='Sample').get('href')

        # Get use the href to get the full url to the enhanced image:
        image_url = f"{url}{image_url}"

        # Create a key value pair in the hemisphere variable:
        hemisphere = {'img_url': image_url, 'title': image_title}

        # Add the hemisphere to the list of hemispheres:
        hemisphere_image_urls.append(hemisphere)

        # Navigate back to the beginning to get the next hemisphere title and image.
        browser.back()
   
    # 4. Return the list that holds the dictionary of each image url and title.
    return hemisphere_image_urls


if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all())




