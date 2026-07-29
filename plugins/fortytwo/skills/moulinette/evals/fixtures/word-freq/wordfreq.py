import sys

path = sys.argv[1]

f = open(path)
text = f.read()

counts = {}
for w in text.split():
    w = w.lower().strip(".,")
    if w in counts:
        counts[w] = counts[w] + 1
    else:
        counts[w] = 1

items = list(counts.items())
items.sort(key=lambda x: x[1], reverse=True)

for i in range(10):
    print(str(items[i][1]) + " " + items[i][0])
