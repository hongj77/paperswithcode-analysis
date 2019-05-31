from database_client import DatabaseClient
import json
import time
import os
import pdb
import requests
from github import Github


class GithubSearchClient:
  def __init__(self, token):
    self.g = Github(token)

  def repository_name(self, url):
    """ Returns the repository pathname from the github URL
    """
    user_name_index = url.find(url.split("/")[3])
    return url[user_name_index:]

  def has_keyword_in_file(self, keyword, url):
    """ Return True if |keyword| is in any of the files
    """
    repo_name = self.repository_name(url)
    query = "{} in:file repo:{}".format(keyword, repo_name)

    # Shortcut: weak heuristic for which libraries are used.
    # The search and matching process is an isolated problem that can be 
    # improved greatly.
    res = self.g.search_code(query=query)
    try:
        return res.totalCount > 0
    except Exception as e:
      raise Exception("Unable to fetch {}. Error:{}".format(repo_name, e))


class GithubFetcher:
  def __init__(self, keywords, db = DatabaseClient()):
    self.g = GithubSearchClient("a77d4b49fac3f43fa1d1df585ea62aa6fc17401c")
    self.keywords = keywords
    self.db = db

  def add_task(self, json_obj):
    repo_url = json_obj["repo_url"]
    paper_title = json_obj["paper_title"]

    libraries = self.maybe_get_github_libraries(repo_url)

    # Only insert if the fetch was successful.
    github_object = {
      "url": repo_url,
      "paper_title": paper_title, 
      "libraries": libraries
    }
    self.db.maybe_update_github_object(github_object)

  def maybe_get_github_libraries(self, repo_url):
    """ Returns which libraries are used in this repo.
    """
    libraries = dict()
    for keyword in keywords:
      if self.g.has_keyword_in_file(keyword, repo_url):
        libraries[keyword] = True
    return libraries

  def start(self):
    print "Starting GithubFetcher"
    with open('data/links-between-papers-and-code.txt') as f:
      links = json.load(f)
      print len(links)
      for link in links:
        try:
          self.add_task(link)
        except Exception as e:
          print e
        time.sleep(0.5)


if __name__=="__main__":
  keywords = ["numpy", "scikit", "tensorflow", "pytorch", "matlab"]
  github_fetcher = GithubFetcher(keywords)
  github_fetcher.start()

  