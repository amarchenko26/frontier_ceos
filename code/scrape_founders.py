#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 29 22:54:29 2023
@author: anyamarchenko
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
import csv
import time

def get_wikipedia_page(driver, first_name, last_name):
    print(f"Searching for Wikipedia page of {first_name} {last_name}")
    search_query = f"{first_name} {last_name} Wikipedia"
    driver.get("https://www.google.com")
    search_box = driver.find_element(By.NAME, "q")
    search_box.send_keys(search_query + Keys.RETURN)
    time.sleep(2)  # wait for page to load

    try:
        wikipedia_link = driver.find_element(By.XPATH, "//div[@class='g']//a[contains(@href, 'wikipedia')]")
        wikipedia_url = wikipedia_link.get_attribute('href')
        print(f"Found Wikipedia URL: {wikipedia_url}")
        return wikipedia_url
    except NoSuchElementException:
        print(f"Wikipedia page not found for {first_name} {last_name}")
        return None

def scrape_wikipedia_page(url, driver):
    print(f"Accessing Wikipedia page: {url}")
    driver.get(url)
    time.sleep(2)  # wait for page to load
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    info_box = soup.find('table', {'class': 'infobox biography vcard'})

    if not info_box:
        print("No infobox found on the Wikipedia page.")
        return None

    data = {}
    for row in info_box.find_all('tr'):
        if row.th and row.td:
            key = row.th.text.strip()
            value = row.td.text.strip()
            data[key] = value
    print(f"Scraped data: {data}")
    return data

def read_and_scrape(csv_file, driver):
    with open(csv_file, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            first_name, last_name = row['First Name'], row['Last Name']
            wikipedia_url = get_wikipedia_page(driver, first_name, last_name)
            if wikipedia_url:
                scraped_data = scrape_wikipedia_page(wikipedia_url, driver)
                print(f"Data for {first_name} {last_name}: {scraped_data}")
            else:
                print(f"No data found for {first_name} {last_name}")


# Setup Selenium WebDriver
options = webdriver.ChromeOptions()
options.add_argument('--headless')  # Run Chrome in headless mode
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome(options=options)


print("Starting scraping process...")
read_and_scrape('/Users/anyamarchenko/Desktop/entrepreneur_test.csv', driver)

print("Scraping process completed.")
driver.quit()