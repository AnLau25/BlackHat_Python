# Bing allows you to query for for all the websites it finds at an IP using, the "IP" search modifier

from burp import IBurpExtender
from burp import IContextMenuFactory
# Provides context menu on right-click for requests
# Allows send to Bing option

from java.net import URL
from java.util import ArrayList
from javax.swing import JMenuItem
from thread import start_new_thread

import json
import socket
import urllib
API_KEY = "YOURKEY"
API_HOST = 'api.cognitive.microsoft.com'


class BurpExtender(IBurpExtender, IContextMenuFactory):
    
    def registerExtender(self, callbacks):
        self._callbacks = callbacks
        self._helpers = callbacks.getHelpers()
        self.context = None
        
        # Set up extentsion
        callbacks.setExtensionName("BHP Bing")
        callbacks.registerContextMenuFactory(self)
        # Register menu handdler, ebables the Bing query construct

        return
    
    def createMenuItems(self, context_menu):
        self.context = context_menu
        menu_list = ArrayList()
        menu_list.add(JMenuItem(
            "Send to Bing", actionPerformed=self.bing_menu
        ))
        # Set up, create menu item that receives a 𝘐𝘊𝘰𝘯𝘵𝘦𝘹𝘵𝘔𝘦𝘯𝘶𝘍𝘢𝘤𝘵𝘰𝘳𝘺 obj
        # Determines the HTTP request selected by the user
        # Renders the menu itemand handles the click event with 𝘣𝘪𝘯𝘨_𝘮𝘦𝘯𝘶 method
        return menu_list
    
    def bing_menu(self, event):
         
        http_traffic = self.context.getSelectedMessage()
        # grab details of what the user clicked
        # Triggered when the user clicks on defined menu item
        
        print("%d requests highlighted" % len(http_traffic))
        
        for traffic in http_traffic:
            http_service = traffic.getHttpService()
            host = http_service.getHost()
            # Retreive IP and host name 
            
            print("User selected host: %s" % host) 
            self.bing_search(host)
            
        return
    
    def bing_search(self, host):
        
        # check for IP host name
        try:
            is_ip = False
            domain = False
        except socket.error:
            is_ip = False
        
        if is_ip:
            ip_address = host
            domain = False
        else:
            ip_address = socket.gethostbyname(host)
            domain = True
        
        start_new_thread(self.bing_query, ('ip: %s' % ip_address,))
        # Query Bing for all virtual hosts on that IP
        
        if domain:
            start_new_thread(self.bing_query, ('domain: %s' % host))
            # If domain was also defined, do secondary search for subdomains that Bing may have indexed
            
    def bing_query(self, bing_query_string):
        print('Performing Bing search: %s' % bing_query_string)
        http_request = 'GET https://%s/bing/v7.0/search?' % API_HOST
        
        # Query encode
        http_request += 'q=%s HTTP/1.1\r\n' % urllib.quote(bing_query_string)
        http_request += 'Host: %s\r\n' % API_HOST
        http_request += 'Ocp-Apim-Subscription-Key: %s\r\n' % API_KEY
        http_request += 'User Agent: Black Hat Python\r\n\r\n'
        # Build a http request and add API key  to make an API call
        
        json_body = self._callbacks.makeHttpRequest(
            API_HOST, 433, True, http_request).tostring()
        # Send http request to Microsoft server
         
        json_body = json_body.split('\r\n\r\n', 1)[1]
        # split headers when response is returned
        
        try:
            response = json.loads(json_body) # response -> JSON parser
        except (TypeError, ValueError) as e:
            print('No results from Bing: %s' % e)
        else:
            site = list()
            if response.get('webPages'):
                sites = response['webPages']['value']
            if len(sites):
                for sites in sites: # Output infor about discovered sites
                    print('*'*100)
                    print('Name: %s       ' % site['name'])
                    print('Url: %s        ' % site['url'])
                    print('Description: %s' % site['snippet'])
                    print('*'*100)
                    
                    java_url = URL(site['url'])
                    if not self._callbacks.isInScope(java_url): # If site not in target scope, add it
                        print('Adding %s to Burp scope' % site['url'])
                        self._callbacks.includeInScope(java_url)
            else:
                print('Empty response from Bing: %s' % bing_query_string)
        
        return