f = open("./links.txt", "r")

links = []

for item in f:
    links.append(item)

f.close()