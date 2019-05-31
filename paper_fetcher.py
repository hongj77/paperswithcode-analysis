from database_client import DatabaseClient
import json


class PaperFetcher:
  def __init__(self, db=DatabaseClient()):
    self.db = db

  def add_task(self, json_obj):
    paper_title = json_obj["title"]
    proceeding = json_obj["proceeding"]
    try:
      self.db.maybe_update_paper_object({
        "paper_title": paper_title, 
        "conference_name": proceeding
      })
    except:
      return

  def start(self):
    print "Staring PaperFetcher"
    with open('data/papers-with-abstracts.txt') as f:
      abstracts = json.load(f)
      print len(abstracts)
      for abstract in abstracts:
        self.add_task(abstract)


if __name__=="__main__":
  paper_fetcher = PaperFetcher()
  paper_fetcher.start()