# Amazon Product Reviews Sentiment Analysis

This is the project for the Natural Language Processing course at the Federal University of Pelotas, developed by me ([amcerri](https://github.com/amcerri)), Afonso and Emerson.

For the final project, all students were assigned to choose a topic related to the discipline for the development of a project, and for that, we selected sentiment analysis.

## Dataset

For the dataset, we chose to perform web scraping instead of using readily available datasets. This allows us to target specific products or categories we wish to analyze, and narrow down the analysis on purpose, which becomes useful when we are considering analyzing a specific product or brand.

## Web Scraping

The web scraping was performed using the [Scrapy](https://scrapy.org/) framework. The scraping was done on the [Amazon](https://www.amazon.com/) website, and the data was collected from the reviews of the products.

The web crawler project can be found at the respository [Amazon Reviews Web Scraper](https://github.com/amcerri/amazon-reviews-scraper).