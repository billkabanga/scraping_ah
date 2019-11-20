"""
module scraper
"""
import requests
from time import sleep, time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup


def get_driver():
  #intislise options
  options = webdriver.ChromeOptions()
  #pass headless arg to options
  options.add_argument('--headless')

  #initialise driver
  driver = webdriver.Chrome(chrome_options=options)
  return driver

def connect_to_site(browser, url):
  connection_attempts = 0
  while connection_attempts < 3:
    try:
      browser.get(url)
      # wait for div with content to load
      WebDriverWait(browser, 5).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'Box'))
      )
      return True
    except Exception as ex:
      connection_attempts += 1
      print(f'Error connecting to {url}')
      print(f'Attempt #{connection_attempts}')
  return False

def parse_html(html):
  #create soup object
  soup = BeautifulSoup(html, 'html.parser')
  output_list = []

  #repo list
  repo_box = soup.find(class_="explore-pjax-container container-lg p-responsive pt-6")

  #find all instances of a class
  repo_list = repo_box.findAll(class_="Box-row")

  for repo in repo_list:
    #find the first <a> and get the text with dev and repo name
    full_repo_name = repo.find('h1').find('a').text.split('/')

    #get dev name at index 0
    dev_name = full_repo_name[0].strip()

    #get repo name at index 1
    repo_name = full_repo_name[1].strip()

    #get number of stars
    stars = repo.find(class_="octicon octicon-star").parent.text.strip()
    
    trending_data = {
      'dev_name': dev_name,
      'repo_name': repo_name,
      'stars': stars
    }

    output_list.append(trending_data)

  return output_list;


def save_to_db(db, output_list):
  for row in output_list:
    entry = db(dev_name=row['dev_name'], repo_name=row['repo_name'], stars=row['stars'])
    entry.save()
