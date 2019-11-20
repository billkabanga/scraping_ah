from time import sleep, time

from scrapers.scraper import get_driver, connect_to_site, parse_html, save_to_db
from models.model import GithubTrendingData

def run_scraper(db, url, browser):
  if connect_to_site(browser, url):
    sleep(2)
    html = browser.page_source
    output_list = parse_html(html)
    save_to_db(db, output_list)
  else:
    print('Error connecting to github')

if __name__ == '__main__':
  # set varibales
  url = 'https://github.com/trending'
  db = GithubTrendingData
  browser = get_driver()
  run_scraper(db, url, browser)
  browser.quit()
