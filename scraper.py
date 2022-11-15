# scrape the posts from wirecutter and save each post as a text file in the posts folder
from bs4 import BeautifulSoup
import os
import time

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.chrome import ChromeDriverManager


# get the list of posts
def get_posts():
    # get the html from the wirecutter homepage
    url = 'https://www.nytimes.com/wirecutter/everything/'
    links = []
    # use selenium to get the html
    browser_options = Options()
    browser_options.add_argument("--window-size=1920x1080")
    browser_options.binary_location = '/Applications/Brave Browser.app/Contents/MacOS/Brave Browser'
    #os.chmod('/opt/homebrew/Cellar/geckodriver/0.32.0/bin/geckodriver', 0o755)
    os.chmod('/opt/homebrew/Caskroom/chromedriver/107.0.5304.62/chromedriver', 0o755)
    browser = webdriver.Chrome(service=Service(
        ChromeDriverManager().install()), options=browser_options)
    #driver = webdriver.Firefox(service = Service(GeckoDriverManager().install()), options=browser_options)
    browser.get(url)
    time.sleep(5)
    html = browser.page_source
    soup = BeautifulSoup(html, 'html.parser')

    # keep clicking the load more button until there are no more posts to load
    while True:
        # click the load more button
        try:
            print('Loading more posts... And clicking the button...')
            button = browser.find_element(
                By.XPATH, '//button[.="Show more..."]')
            button.location_once_scrolled_into_view

            # get the links to the posts, where element a id contains 'post', also skip the links that are already in the list
            for link in soup.find_all('a', id=lambda x: x and 'group-title' in x):
                if link['href'] not in links:
                    links.append(link['href'])
                else:
                    continue

            print('Number of posts: ' + str(len(links)))
            # save the links to a file
            with open('links.txt', 'w') as f:
                for link in links:
                    f.write(link + '\n')

            button.click()
            print('Show More button clicked')
            time.sleep(5)
            html = browser.page_source
            soup = BeautifulSoup(html, 'html.parser')
        except:
            print('No more Show More button')
            # if there are no more posts to load, break out of the while loop and continue with the rest of the program
            break

    # close the browser
    browser.quit()
    return links


# loop through the links and save each post as a text file
def save_posts(links):
    print('Saving posts...')
    # use selenium to get the html
    browser_options = Options()
    # browser_options.add_argument("--headless")
    browser_options.add_argument("--window-size=1920x1080")
    browser_options.binary_location = '/Applications/Brave Browser.app/Contents/MacOS/Brave Browser'
    #os.chmod('/opt/homebrew/Cellar/geckodriver/0.32.0/bin/geckodriver', 0o755)
    os.chmod('/opt/homebrew/Caskroom/chromedriver/107.0.5304.62/chromedriver', 0o755)
    browser = webdriver.Chrome(service=Service(
        ChromeDriverManager().install()), options=browser_options)
    #driver = webdriver.Firefox(service = Service(GeckoDriverManager().install()), options=browser_options)

    # if links is not empty then loop through the links and save each post as a text file
    if links:
        for link in links:
            browser.get(link)
            time.sleep(5)
            html = browser.page_source
            soup = BeautifulSoup(html, 'html.parser')
            # show a progress bar to show that the program is running and to give an estimate of how long it will take to finish
            print('Scraping post ' + str(links.index(link) + 1) +
                  ' of ' + str(len(links)))
            # get the post text
            post_text = soup.find('article').get_text(
                strip=True, separator=' ')

            # if the posts directory doesn't exist, create it
            if not os.path.exists('posts'):
                os.makedirs('posts')

            # save the post text to a file
            with open('posts/' + link.split('/')[-2] + '.txt', 'w') as f:
                f.write(post_text)

            print('Post saved as ' + link.split('/')[-2] + '.txt')
    else:
        print('No posts to save')

    # close the browser
    browser.quit()


# run the program
if __name__ == '__main__':
    links = get_posts()
    # save the list of links to a file
    with open('links_full.txt', 'w') as f:
        for link in links:
            f.write(link + '\n')

    with open('links_full.txt', 'r') as f:
        links = f.read().splitlines()
    save_posts(links)
    print('Done!')
