import json
import requests


url = "https://api.datamuse.com/words?sp=amon*"

n = 0
r = requests.get(url)
data = json.loads(r.text)



word_list = []
example = ""

for word in data:
    name = word['word']
    word_list.append(name)
    example.join(name)

print(word_list)

l = len(word_list)

# for l in word_list:
#     print(l)

print(example)

# print(data[0]['word'])