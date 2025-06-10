# Brute forcing of POST request 
# For testing form filling, captcha, log-in token or any type of submition 
# 𝗥𝗲𝗾𝘂𝗶𝗿𝗲𝗺𝗲𝗻𝘁𝘀: 
#   - Retreive hidden token from before pswd submition attemps 
#   - Ensure http session accepts cookies
# The remote app sets one or more cookies on on contact and expects them back on login
# 𝘉𝘦𝘢𝘶𝘵𝘪𝘧𝘶𝘭𝘚𝘰𝘶𝘱 𝘢𝘯𝘥 𝘭𝘹𝘮𝘭 packages to parse login form values
# Worpress checks the cookies againts the current user session
# If the cookies don't mach, the login will fail even with the right creds
# 𝗥𝗲𝗾𝘂𝗲𝘀𝘁 𝗳𝗹𝗼𝘄: 
#   1. Retreive log in page and accept all returned cookies
#   2. Parse out all of the form elements from the HTML
#   3. Set the uss and pswd from a guest in diretory
#   4. Send HTTP POST to login processing script, cookies and form fields included
#   5. Test login
  




