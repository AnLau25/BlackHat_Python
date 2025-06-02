from io import BytesIO # allows us to use byte string content as a file-like obj
from lxml import etree # package content parser
import requests

url = 'https://nostarch.com'
r = requests.get(url) # GET
content = r.content   # content is type 'bytes'

parser = etree.HTMLParser()
content = etree.parse(BytesIO(content), parser=parser) # Parse into etree
for link in content.findall('//a'): # Looks for all 𝘢𝘯𝘤𝘩𝘰𝘳 tags in the parsed content
    print(f"{link.get('href')} -> {link.text}") # print results