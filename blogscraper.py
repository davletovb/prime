# PostScraper class to scrape the posts from wirecutter and save each post as a text file in the posts folder
import os
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium import webdriver
from bs4 import BeautifulSoup
import pathlib
import time

import logging
logging.basicConfig(level=logging.INFO)


class BlogPostScraper:

    def __init__(self):
        self.url = 'https://www.nytimes.com/wirecutter/everything/'
        self.links = []
        self.base_path = pathlib.Path(__file__).resolve().parent
        self.posts_folder = self.base_path / 'posts'
        self.links_file = self.base_path / 'links.txt'

        # create the posts folder if it doesn't exist
        if not self.posts_folder.exists():
            self.posts_folder.mkdir()

    # get the list of posts
    def get_posts(self):
        # use selenium to get the html
        browser_options = Options()
        browser_options.add_argument("--window-size=1920x1080")

        # If on MacOS you may need to add this: os.chmod('path to geckodriver', 0o755)

        browser = webdriver.Firefox(service=Service(
            GeckoDriverManager().install()), options=browser_options)

        browser.get(self.url)
        time.sleep(5)
        html = browser.page_source
        soup = BeautifulSoup(html, 'html.parser')

        # keep clicking the load more button until there are no more posts to load
        while True:
            # click the load more button
            try:
                logging.info(
                    'Loading more posts... And clicking the button...')
                button = browser.find_element(
                    By.XPATH, '//button[.="Show more..."]')
                button.location_once_scrolled_into_view

                # get the links to the posts, where element a id contains 'post', also skip the links that are already in the list
                for link in soup.find_all('a', id=lambda x: x and 'group-title' in x):
                    if link['href'] not in self.links:
                        self.links.append(link['href'])
                    else:
                        continue

                logging.info('Number of posts: ' + str(len(self.links)))
                # save the links to a file
                with open(self.links_file, 'w') as f:
                    for link in self.links:
                        f.write(link + '\n')

                button.click()
                logging.info('Show More button clicked')
                time.sleep(5)
                html = browser.page_source
                soup = BeautifulSoup(html, 'html.parser')
            except:
                logging.info('No more Show More button')
                # if there are no more posts to load, break out of the while loop and continue with the rest of the program
                break

        # close the browser
        browser.quit()

    # loop through the links and save each post as a text file
    def save_posts(self, links):
        logging.info('Saving posts...')
        # use selenium to get the html
        browser_options = Options()
        browser_options.add_argument("--window-size=1920x1080")

        # If on MacOS you may need to add this: os.chmod('path to geckodriver', 0o755)

        browser = webdriver.Firefox(service=Service(
            GeckoDriverManager().install()), options=browser_options)

        # if links is not empty then loop through the links and save each post as a text file
        if links:
            for link in links:
                browser.get(link)
                time.sleep(5)
                html = browser.page_source
                soup = BeautifulSoup(html, 'html.parser')
                # show a progress bar to show that the program is running and to give an estimate of how long it will take to finish
                logging.info('Scraping post ' + str(links.index(link) + 1) +
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

                logging.info('Post saved as ' + link.split('/')[-2] + '.txt')
        else:
            logging.info('No posts to save')

        # close the browser
        browser.quit()

    def run(self):

        logging.info('Getting the list of posts...')

        self.get_posts()

        logging.info('Done getting the list of posts')

        logging.info('Scraping posts...')

        # read the links from the links file if it exists
        if self.links_file.exists():
            with open(self.links_file, 'r') as f:
                links = f.read().splitlines()

        self.save_posts(links)

        logging.info('Done scraping posts')


if __name__ == '__main__':
    scraper = BlogPostScraper()
    scraper.run()
