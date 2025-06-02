# Ie, how to not end up crying when u only got plain old Python2x or 3x
# In most cases this can happen if you are on a victim machine, and it doesn't have python cause the user is no progarammer

# import urllib2
# url = 'https://www.nostarch.com'
# response = urllib2.urlopen(url) 
# GET ; returns a file with the body of the raw page in the remote Server
# print(response.read()) # read the raw body
# response.close

# import urllib2
# url = "https://www.nostarch.com"
# header = {'User-Agent': "Googlebot"} # defines the header as a dictionary
# Allows us to choose the header keys and values that we want
# request = urllib2.Request(url, headers=headers) # Create request obj
# response = urllib2.urlopen(request) # Returns a normal file
# print(response.read())
# response.close() 

import urllib.parse
import urllib.request

url = 'http://boodelyboo.com' # url definition for http req
with urllib.request.urlopen(url) as response: # urllib as context manager for request
    content = response.read() # Read response
print()

# to create a POST request, pass de data dictionary to the request obj, encoded
# the dictionary in question should have key value pairs targeting web app aspects
info = {'user' : 'Name', 'passwd':'1407'}
data =  urllib.parse.urlencode(info).encode() # data type -> byte

req = urllib.request.Request(url, data)
with urllib.request.urlopen(req) as response: # POST
# Sends the credentials in byte type and records the web response to the logIn attempt
    content = response.read()
print(content)




