from bs4 import BeautifulSoup
import requests

code_prefix = "https://raw.githubusercontent.com"

def get_pylinks (directory_links):
	if directory_links == []:
		return []
	python_file_links = []
	for directory_link in directory_links:
		link = directory_link.get('href')
		name = directory_link.text
		name = name.split('.')
		if len(name) == 1 : # It is generally a directory
			# Do some directory shit
			split_link = link.split('/')
			if split_link[3] == 'tree':
				soup = BeautifulSoup( requests.get ( prefix + link ).text )
				new_directory_links = soup.find_all(class_='js-directory-link')
				python_file_links += python_file_links + get_pylinks(new_directory_links)
				
		elif name[-1] == 'py':
			# sp = BeautifulSoup( requests.get( code_prefix + link.replace('/blob', '') ).text )
			# print sp.find('p').text
			python_file_links.append(code_prefix + link.replace('/blob', ''))
		else:
			continue
	return python_file_links
	
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
python_file_links = []
# i = 0
for repo in repo_links:
	repo = repo_links[2]
	soup = BeautifulSoup( requests.get ( repo ).text )
	directory_links = soup.find_all(class_='js-directory-link')
	python_file_links += get_pylinks(directory_links)

with open('links.txt', 'w') as py_links:
	for each in python_file_links:
		pylinks.write(each + "\n")

print len (python_file_links)
