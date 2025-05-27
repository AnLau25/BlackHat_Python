# 𝗔𝗥𝗣 𝗔𝘁𝘁𝗮𝗰𝗸𝘀:
# It consist of, basically, convincing the target that we are it's gateway
# Smilarly, we convince the actual gateway that we are a router to the target
# Thus, all trafic between both entities ends up going through us
# To do so, we poison the ARP cache of both points and masks ourself with their MACs (Media Acces Control) address
# The MAC is assigned based on the local network IP of the machine
