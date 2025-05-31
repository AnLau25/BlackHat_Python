from bs4 import BeautifulSoup as bs
import requests

url = 'http://bing.com'
r = requests.get(url) # GET
tree = bs(r.text, 'html.parser') # Parser intp tree
for link in tree.find_all('a'): # find all anchor elements
    print(f"{link.get('href')} -> {link.text}")