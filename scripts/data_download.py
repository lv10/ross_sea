import os
import sys

import requests
from bs4 import BeautifulSoup

base_url = "http://csdirs.ccny.cuny.edu/u/gib/rohit/2015_336/"
data_path = os.path.join(os.pardir, "data")

req = requests.get(base_url)
html_doc = req.text

soup = BeautifulSoup(html_doc, 'html.parser')

links = soup.find_all('a')

filenames = list()
for link in links:
    if link.get('href')[:3] == 'G_2':
        filenames.append(link.get('href'))

# Download files
print "Preparing to download files {0}...".format(len(filenames))
for filename in filenames:
    path = os.path.join(os.getcwd(), data_path)

    if not os.path.exists(path):
        print "Creating Data Dir".format(filename)
        os.makedirs(path)
        print "Created Data Dir".format(filename)

    with open(os.path.join(path, filename), 'wb') as f:
        print "Saving {0} ...".format(filename)
        url = base_url + filename
        req = requests.get(url, stream=True)
        if not req.ok:
            print "Somethiing went wrong"
            sys.exit(0)
        f.write(req.content)
        print "Saved {0} ...".format(filename)

print "Done, files downloaded!"
