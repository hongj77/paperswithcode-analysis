import sqlite3
import pdb


class DatabaseClient:
  def __init__(self):
    # Initalize all tables if it doesn't already exist.
    self.maybe_create_papers_table()
    self.maybe_create_repos_table()
    self.maybe_create_papers_stats_table()
    self.maybe_create_conference_stats_table()

  def execute_sql(self, sql):
    try:
      with sqlite3.connect("test.db") as conn:
        cursor = conn.execute(sql)
        return cursor
    except Exception as e:
      print e
    return None

  def maybe_create_papers_table(self):
    sql = '''CREATE TABLE IF NOT EXISTS papers
        (paper_title text primary key not null,
          conference_name text default "NA")'''
    self.execute_sql(sql)

  def maybe_create_repos_table(self):
    sql = '''CREATE TABLE IF NOT EXISTS repos
        (repo_url text,
          has_numpy integer,
          has_scikit  integer,
          has_tensorflow  integer,
          has_pytorch integer,
          has_matlab  integer,
          paper_title text,
          PRIMARY KEY(repo_url),
          FOREIGN KEY(paper_title) REFERENCES papers(paper_title))'''
    self.execute_sql(sql)

  def maybe_create_conference_stats_table(self):
    sql = '''CREATE TABLE IF NOT EXISTS conference_stats
        (conference_name text primary key not null,
          num_numpy integer,
          num_scikit integer,
          num_tensorflow integer,
          num_pytorch integer,
          num_matlab integer,
          num_papers integer)'''
    self.execute_sql(sql)

  def maybe_create_papers_stats_table(self):
    sql = '''CREATE TABLE IF NOT EXISTS papers_stats
        (paper_title text PRIMARY KEY NOT NULL,
          conference_name text,
          has_numpy integer,
          has_scikit integer,
          has_tensorflow integer,
          has_pytorch integer,
          has_matlab integer)'''
    self.execute_sql(sql)

  def update_conference_stats_table(self, values):
    sql = '''REPLACE INTO conference_stats
        VALUES (\"{}\", {},{},{},{},{},{})'''.format(
          values['conference_name'],
          values['num_numpy'], 
          values['num_scikit'], 
          values['num_tensorflow'], 
          values['num_pytorch'], 
          values['num_matlab'], 
          values['num_papers'])
    self.execute_sql(sql)

  def update_papers_stats_table(self):
    # Joins the papers and repos table and updates papers_info table.
    sql = '''REPLACE INTO papers_stats 
    SELECT papers.paper_title, conference_name, has_numpy, 
      has_scikit, has_tensorflow, has_pytorch, has_matlab
      from papers
      inner join repos
      on papers.paper_title = repos.paper_title'''
    self.execute_sql(sql)

  def create_repo_row(self, url, paper_title, libraries):
    numpy, scikit, tensorflow, pytorch, matlab = 0,0,0,0,0
    if libraries:
      for key,value in libraries.items():
        if key == "numpy" and value:
          numpy = 1
        if key == "scikit" and value:
          scikit = 1
        if key == "tensorflow" and value:
          tensorflow = 1
        if key == "pytorch" and value:
          pytorch = 1
        if key == "matlab" and value:
          matlab = 1
    values = "(\"{}\",{},{},{},{},{},\"{}\")".format(
      url,  numpy, scikit, tensorflow, pytorch, matlab, paper_title)
    return values

  def maybe_update_github_object(self, github_object):
    values = self.create_repo_row(
          github_object['url'], 
          github_object['paper_title'], 
          github_object['libraries'])
    sql = '''REPLACE INTO repos VALUES {}'''.format(values)
    self.execute_sql(sql)

  def create_paper_row(self, paper_title, conference_name):
    values = "(\"{}\",\"{}\")".format(paper_title, conference_name)
    return values

  def maybe_update_paper_object(self, paper_object):
    values = self.create_paper_row(
          paper_object['paper_title'], 
          paper_object['conference_name']) 
    sql = '''REPLACE INTO papers VALUES {}'''.format(values)
    self.execute_sql(sql)

  def get_all_papers_stats(self):
    # Returns the rows of papers_stats returned by the DB.
    sql = '''SELECT * FROM papers_stats'''
    cursor = self.execute_sql(sql)
    result = []
    for item in cursor:
      result.append(item)
    return result

  def get_all_conference_stats(self):
    # Returns the rows of conference_stats returned by the DB.
    sql = '''SELECT * FROM conference_stats'''
    cursor = self.execute_sql(sql)
    result = []
    for item in cursor:
      result.append(item)
    return result


if __name__=="__main__":
  print "Staring DatabaseClient"
  db = DatabaseClient()
