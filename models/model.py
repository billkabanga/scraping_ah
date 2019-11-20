from mongoengine import *
connect('parallel_scraping_results')

class GithubTrendingData(Document):
  dev_name = StringField()
  repo_name = StringField()
  stars = StringField()

