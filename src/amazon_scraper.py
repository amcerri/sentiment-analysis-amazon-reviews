from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
import lxml
import time
import re
import pandas as pd
import math
from collections import namedtuple
from IPython.display import clear_output

class AmazonScraper:
    # Opting for a namedtuple instead of a dictionary (namedtuples are faster and don't have hashability issues)
    ReviewDetails = namedtuple('ReviewDetails', ['product_name', 'review_title', 'review_body', 'review_rating', 'review_date', 'user_username', 'user_profile_url', 'verified_purchase'])

    # Date pattern to be used when scraping the review date
    date_pattern = re.compile('(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?) \d+, \d{4}')

    # Constructor (initializes the driver)
    def __init__(self):
        self.options = Options()
        self.options.add_argument('--headless')
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=self.options)

    # Scrape the reviews from the given URL for a given number of pages (default is to scrape all pages)
    def scrape_reviews(self, url, max_pages):
        # Add a timeout to the driver to prevent it from hanging indefinitely
        t = time.time()
        self.driver.set_page_load_timeout(10)

        # Open the URL
        try:
            self.driver.get(url)
        except TimeoutException:
            self.driver.execute_script("window.stop();")

        # Get the page source and create a BeautifulSoup object for the product page
        html = self.driver.page_source.encode('utf-8')
        soup = BeautifulSoup(html, 'lxml')

        # Get the product name
        product_name = soup.find('span', {'id': 'productTitle'}).text.strip()

        # Navigate to the reviews page
        reviews_page = soup.find('a', {'data-hook': 'see-all-reviews-link-foot'})
        try:
            self.driver.get('https://www.amazon.com' + reviews_page['href'])
        except TimeoutException:
            self.driver.execute_script("window.stop();")
        

        # Get the page source and create a BeautifulSoup object for the first reviews page
        html = self.driver.page_source.encode('utf-8')
        soup = BeautifulSoup(html, 'lxml')

        # Get the reviews section of the page
        reviews_section = soup.find('div', {'id': 'cm_cr-review_list'})

        # Iterate through the reviews of the current and subsequent pages
        reviews = []
        page = 1

        while page <= max_pages:
            clear_output(wait=True)
            print('Scraping page ' + str(page) + 'of ' + url)


            # Get a list of all the reviews on the page
            product_reviews = reviews_section.find_all('div', {'data-hook': 'review'})

            # Check if data-hook 'dp-global-reviews-header' is present (no more reviews from the US)
            if self.driver.find_elements(By.CSS_SELECTOR, '[data-hook="dp-global-reviews-header"]'):
                print('No more reviews from the US, stopped at page ' + str(page))
                break
            

            # Iterate through the reviews and scrape the details
            for review in product_reviews:
                # Get the review title
                review_title = review.find('a', {'data-hook': 'review-title'}).text.strip()

                # Get the review body
                review_body = review.find('span', {'data-hook': 'review-body'}).text.strip()

                # Get the review rating
                review_rating = review.find('i', {'data-hook': 'review-star-rating'}).text.strip()

                # Get the review date
                review_date = self.date_pattern.search(review.find('span', {'data-hook': 'review-date'}).text.strip()).group()

                # Get the user username
                user_username = review.find('span', {'class': 'a-profile-name'}).text.strip()

                # Get the user profile URL
                user_profile_url = 'https://www.amazon.com' + review.find('a', {'class': 'a-profile'})['href']

                # Check if the review was verified
                verified_purchase = review.find('span', {'data-hook': 'avp-badge'})

                if verified_purchase:
                    verified_purchase = True
                else:
                    verified_purchase = False

                # Add the review details to the list of reviews
                reviews.append(self.ReviewDetails(product_name, review_title, review_body, review_rating, review_date, user_username, user_profile_url, verified_purchase))
                
            # Check if 'a-disabled a-last' is present (no more pages) using selenium
            if self.driver.find_elements(By.CSS_SELECTOR, '[class="a-disabled a-last"]'):
                print('No more pages, stopped at page ' + str(page))
                break
            
            # Get the html for the next page
            next_page = soup.find('li', {'class': 'a-last'})

            # Navigate to the next page
            try:
                self.driver.get('https://www.amazon.com' + next_page.find('a')['href'])
            except TimeoutException:
                self.driver.execute_script("window.stop();")
            

            # Get the page source and create a BeautifulSoup object for the next page
            html = self.driver.page_source.encode('utf-8')
            soup = BeautifulSoup(html, 'lxml')

            # Get the reviews list
            reviews_section = soup.find('div', {'id': 'cm_cr-review_list'})

            # Increment the page number
            page += 1

        return reviews