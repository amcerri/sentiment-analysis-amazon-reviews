# Amazon Product Reviews Sentiment Analysis

This is the final assignment project for the Natural Language Processing course at the Federal University of Pelotas.

All students were assigned to choose a topic related to the discipline for the development of a project, and for that, sentiment analysis was selected.

## Dataset

For the dataset, we chose to perform web scraping instead of using readily available datasets. This allows to target specific products or categories that we wish to analyze, and narrow down the analysis on purpose, which becomes useful when considering analyzing a specific product or brand.

## Web Scraping

The web scraping was performed using the [Scrapy](https://scrapy.org/) framework. The scraping was done on the [Amazon](https://www.amazon.com/) website, and the data was collected from the reviews of the products.

The web crawler project can be found at the respository [Amazon Reviews Web Scraper](https://github.com/amcerri/amazon-reviews-scraper).

## Results

The dataset after labeling the reviews are unbalanced, no form of data augmentation was performed. The dataset was split into 80% for training and 20% for testing. The results are far from ideal, but they are a good starting point for further improvements.