
## Design: 
https://docs.google.com/document/d/1LyK6Vw-yNhsfIczV9JHEYlIwEFSdFEFpKl7pl6xi0Yk/edit?usp=sharing

## Run Instructions
1. Clone repo
2. Pip install dependencies in requirements.txt `pip install -r requirements.txt`
3. Get Personal access token from Github. (needed for reading from the repo through API)
4. `export ACCESS_TOKEN=<your token>`
5. Download the json files from paperswithcode.com and unzip them into `data/` directory
5. `./application.sh`

## Example
Note: Pressing 0 takes a long time to accumilate the data due to the Github API rate limiting, which is limited to 60 requests per hour. The provided `test.db` in this repo contains the results of the fetching that I have already done. It is not a complete data set. I was only able to fetch a few hundred repositories for a proof of concept.

For demo purposes, you can directly skip to pressing 1 or 2.

```
$> ./application.sh
=================================
Press 0 to fetch/update data (only done once)
Press 1 to see paper stats
Press 2 to see conference stats
=================================
1
=================================
[('paper_title', u'Efficient First-Order Algorithms for Adaptive Signal Denoising'), ('conference_name', u'ICML 2018 7'), ('numpy', 0), ('scikit', 0), ('tensorflow', 0), ('pytorch', 0), ('matlab', 1)]
...
...
=================================
Press 0 to fetch/update data (only done once)
Press 1 to see paper stats
Press 2 to see conference stats
=================================
2
=================================
[('conference_name', u'COLING 2018 8'), ('numpy', 1), ('scikit', 0), ('tensorflow', 1), ('pytorch', 0), ('matlab', 0)]
=================================
[('conference_name', u'ICML 2018 7'), ('numpy', 1), ('scikit', 0), ('tensorflow', 1), ('pytorch', 0), ('matlab', 1)]
...
... 
```
