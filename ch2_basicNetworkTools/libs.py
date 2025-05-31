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
# header = {'User-Agent': "Googlebot"}
# request = urllib2.Request(url, headers=headers)
# response = urllib2.urlopen(request)
# print(response.read())
# response.close()

import urllib.parse
import urllib.response

url = 'https://www.nostarch.com'
