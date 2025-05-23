# 𝗜𝗖𝗠𝗣 𝗗𝗲𝗰𝗼𝗱𝗶𝗻𝗴
#   - Content varys but the 𝘵𝘺𝘱𝘦, 𝘤𝘰𝘥𝘦 𝘢𝘯𝘥 𝘤𝘩𝘦𝘤𝘬𝘴𝘶𝘮 fields 𝘢𝘳𝘦 𝘤𝘰𝘯𝘴𝘪𝘴𝘵𝘦𝘯𝘵 
#   - The type and code 𝘵𝘦𝘭𝘭 𝘵𝘩𝘦 𝘳𝘦𝘤𝘪𝘷𝘪𝘯𝘨 𝘩𝘰𝘴𝘵 the type of ICMP
#   - type 3, code 3 is the 𝘗𝘰𝘳𝘵 𝘜𝘯𝘳𝘦𝘢𝘤𝘩𝘢𝘣𝘭𝘦 𝘦𝘳𝘳𝘰𝘳 message
#   - That's what we're looking for to identify possible targets in the network
#   - When the host sends an ICMP, it also sends the IP header of the msg that generated the response
#            𝘗𝘰𝘳𝘵 𝘜𝘯𝘳𝘦𝘢𝘤𝘩𝘢𝘣𝘭𝘦 Message
#   ---------------------------------------
#   |   0 - 7  | 8 - 15 |     16 - 31     |
#   ---------------------------------------
#   | Type = 3 |  Code  | Header Checksum |
#   ---------------------------------------
