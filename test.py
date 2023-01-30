import requests

BASE = "http://127.0.0.1:5000/"

data = [{"likes": 10, "name": "wayne", "views": 5},
        {"likes": 27, "name": "riley", "views": 73},
        {"likes": 55, "name": "jonesy", "views": 117}]

for i in range(len(data)):
    response = requests.put(BASE + "video/" + str(i), data[i])
    print(response.json())


response = requests.get(BASE + "video/1")
print(response.json())