# 𝗕𝘂𝗿𝗯, 𝗣𝘆𝘁𝗵𝗼𝗻 𝘀𝗲𝘁 𝘂𝗽:
# Download 𝘑𝘺𝘵𝘩𝘰𝘯 𝘚𝘵𝘢𝘯𝘥𝘢𝘭𝘰𝘯𝘦 JAR⁡⁢⁣⁢*⁡
# Go to Extensions >>> Extensions Settings >>> Python env. >>> Location of Jython standalone JAR file 
# Place file location in box
# Close and re-open
# ​‍‌‌⁡⁢⁣⁢‍‍1⁡​​Jython expects python2 

# 𝗕𝘂𝗿𝗽 𝗔𝗣𝗜 𝗱𝗼𝗰𝘂𝗺𝗲𝗻𝘁𝗮𝘁𝗶𝗼𝗻:
# Go to Extensions
# Go to 𝗔𝗣𝗜𝘀 tab
# For fuzz web requests during Intruder attacks:
#   - Intruder folder (↓)
#   - IIntruderPayloadGenerator (creo que es IntruderPayloadGenerator)
#   - IIntruderPayloadGeneratorFactory (idk) 
# 

# 𝗧𝗲𝘀𝘁 𝗯𝗵𝗽_𝗳𝘂𝘇𝘇𝗲𝗿.𝗽𝘆:
#   - Add to extensions: Extensions >>> Add: Set Extension type to Python, Extension file bhp_fuzzer.py location
#   - >>> Proxy: Click "𝘖𝘱𝘦𝘯 𝘣𝘳𝘰𝘸𝘴𝘦𝘳", go to http://testphp.vulnweb.com/
#   - Turn on intercept, interact with testphp search box >>> Proxy: HTTP Hisotry
#   - Select POST method + rightClick, select 𝘚𝘦𝘯𝘥 𝘵𝘰 𝘐𝘯𝘵𝘳𝘶𝘥𝘦𝘳
#   - >>> Intruder >>> Position >>> Select payload and click 𝘈𝘥𝘥
#   - >>> Intruder: Payload, Set Payload type to 𝘌𝘹𝘵𝘦𝘯𝘴𝘪𝘰𝘯-𝘨𝘦𝘯𝘦𝘳𝘢𝘵𝘦𝘥 and Extension payload generator to 𝘉𝘏𝘗 𝘗𝘢𝘺𝘭𝘰𝘢𝘥 𝘎𝘦𝘯𝘦𝘳𝘢𝘵𝘰𝘳 
#   - Click 𝘚𝘵𝘢𝘳𝘵 𝘈𝘵𝘵𝘢𝘤𝘬
#   - New window with fuzzing results will apear

# 𝗧𝗲𝘀𝘁 𝗯𝗵𝗽_wordlist.𝗽𝘆:
#   - Add to extensions: Extensions >>> Add: Set Extension type to Python, Extension file bhp_fuzzer.py location
#   - >>> Dashboard: Select New live task, select "Add all links observed in traffic through Proxy to site map"
#   - Get results from Targe, opening browse as in last step
#   - Select all targets, rightClick: Select Extensions, create Wordlist
#   - >>> Extender >>> Output: Check that the wordlist was created