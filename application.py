import argparse
from aggregator import Aggregator
from github_fetcher import GithubFetcher
from paper_fetcher import PaperFetcher
from database_client import DatabaseClient
import pdb


class Application:
  def __init__(self):
    self.keywords = ["numpy", "scikit", "tensorflow", "pytorch", "matlab"]
    self.github_fetcher = GithubFetcher(self.keywords)
    self.paper_fetcher = PaperFetcher()
    self.db = DatabaseClient()

  def get_paper_stats(self):
    # Returns the (paper, conference, libraries) tuple of the most recently
    # processed data. Not guranteed to be fresh.
    rows = self.db.get_all_papers_stats()
    formatted_result = []
    for row in rows:
      column_names = ['paper_title', 'conference_name'] + self.keywords
      zipped = zip(column_names, row)
      formatted_result.append(zipped)
    return formatted_result

  def get_conference_stats(self):
    # Returns the (conference, library_count) tuple for each conference.
    # Not guranteed to be fresh.
    rows = self.db.get_all_conference_stats()
    formatted_result = []
    for row in rows:
      column_names = ['conference_name'] + self.keywords
      zipped = zip(column_names, row)
      formatted_result.append(zipped)
    return formatted_result

  def start(self, response):
    if response == "0":
      # Run the offline pipeline.
      self.paper_fetcher.start()
      self.github_fetcher.start()
      self.aggregator.start()
    elif response == "1":
      results = self.get_paper_stats()
      for result in results:
        print "================================="
        print result
    elif response == "2":
      results = self.get_conference_stats()
      for result in results:
        print "================================="
        print result
    else:
      print "Not a valid response"


if __name__=="__main__":
  while True:
    print "================================="
    print "Press 0 to fetch/update data (only done once)"
    print "Press 1 to see paper stats"
    print "Press 2 to see conference stats"
    print "================================="
    response = raw_input()
    if response == "4":
      break
    app = Application()
    app.start(response)
