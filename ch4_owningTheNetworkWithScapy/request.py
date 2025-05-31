import requests # auto handdles cookies

url = 'http://boodelyboo'
response = requests.get(url) # GET

data = {'user' : 'Name', 'passwd':'1407'}
response = requests.get(url, data=data) # POST
print(response.text) # response.text = string; response.content = bytestring