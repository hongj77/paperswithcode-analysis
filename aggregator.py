from database_client import DatabaseClient


class Aggregator:
  def __init__(self, db=DatabaseClient()):
    self.db = db

  def phase_one(self):
    # Join the papers and repos tables and store the result into
    # the papers_info table.
    self.db.update_papers_stats_table()

  def phase_two(self):
    # Perform aggregation on the joined data and store it back into
    # the conference_stats table.
    num_numpy, num_scikit, num_tensorflow, num_pytorch, num_matlab, num_papers = (0,0,0,0,0,0)

    # Shortcut: Do manual aggregation here for each row.
    # Keep a hashmap keyed by conference_name and write it back to the DB.

    conference_stats = dict()
    rows = self.db.get_all_papers_stats()
    for papers_info in rows:
      conference_name = papers_info[1]
      # Initialize a hashmap for each conference_name to aggregate data.
      if conference_name not in conference_stats:
        conference_stats[conference_name] = dict()
        conference_stats[conference_name]['num_papers'] = 0
        conference_stats[conference_name]['num_numpy'] = 0
        conference_stats[conference_name]['num_scikit'] = 0
        conference_stats[conference_name]['num_tensorflow'] = 0
        conference_stats[conference_name]['num_pytorch'] = 0
        conference_stats[conference_name]['num_matlab'] = 0

      # Update the map with the counts of the libraries.
      conference_stats[conference_name]['num_papers'] += 1
      if papers_info[2]:
        conference_stats[conference_name]['num_numpy'] += 1
      if papers_info[3]:
        conference_stats[conference_name]['num_scikit'] += 1
      if papers_info[4]:
        conference_stats[conference_name]['num_tensorflow'] += 1
      if papers_info[5]:
        conference_stats[conference_name]['num_pytorch'] += 1
      if papers_info[6]:
        conference_stats[conference_name]['num_matlab'] += 1

      # Write the aggregated information to the conference_stats table.
      values = {
        "conference_name": conference_name,
        "num_numpy": conference_stats[conference_name]['num_numpy'],
        "num_scikit": conference_stats[conference_name]['num_scikit'],
        "num_tensorflow": conference_stats[conference_name]['num_tensorflow'],
        "num_pytorch": conference_stats[conference_name]['num_pytorch'],
        "num_matlab": conference_stats[conference_name]['num_matlab'],
        "num_papers": conference_stats[conference_name]['num_papers'],
      }
      self.db.update_conference_stats_table(values)

  def start(self):
    print "Staring Aggregator"
    print "Starting Phase 1"
    # Phase 1 involves performing a join and storing the result back into
    # the DB. This gives us two things: 1) the app layer can read from this 
    # table instantaneously to output which libraries were used and 
    # 2) it allows aggregation part to be parallelized in the next step.
    self.phase_one()

    print "Starting Phase 2"
    # Phase 2 involves performing a read-only task to create an aggregated
    # data. This part could be parallelized using map-reduce.
    self.phase_two()


if __name__=="__main__":
  aggregator = Aggregator()
  aggregator.start()