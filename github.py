from bs4 import BeautifulSoup
import requests

# URL to fetch top python projects
URL = "https://github.com/search?l=Python&q=stars%3A%3E1&s=stars&type=Repositories"
prefix = "https://github.com"
soup = BeautifulSoup(requests.get(URL).text)

h3s = soup.find_all(class_='repo-list-name')
repo_links = []
repos = []
for h3 in h3s:
	a = h3.find('a').get('href')
	repo_links.append(a)
	# Get the repo name
	a = a.split('/')
	repos.append(a[1])
	# Just for testing
	print a[1]

for i in xrange(len(repo_links)):
	repo_links[i] = prefix + repo_links[i]
	print repo_links[i]

# fetch code from each repo and store it in a text file

for repo in repo_links:
	soup = BeautifulSoup( requests.get ( repo ) )