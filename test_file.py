from os import link


f = open("./links.txt", "r")

links = []

for item in f:
    links.append(item)

print(type(links[0]))
print(links[1])
print(links[2])

f.close()