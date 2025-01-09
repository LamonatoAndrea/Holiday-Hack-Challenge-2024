import requests
import json

url = 'https://hhc24-hardwarehacking.holidayhackchallenge.com/joke'

try:
  with open("jokes.txt", "r") as jokes_file:
    jokes = jokes_file.read().split("\n")

  print ("jokes --> {}".format(jokes))
except:
  jokes = []

with open("jokes.txt", "a") as jokes_file:
  sameJokeCount = 0
  while sameJokeCount < 1000:
    r = requests.get(url)
    joke = json.loads(r.text)['joke']
    if joke in jokes:
      print ("GOT [{}] OLD (DAD) JOKES: {}".format(sameJokeCount, joke))
      sameJokeCount += 1
    else:
      jokes_file.write("{}\n".format(joke))
      jokes.append(joke)
      print ("NEW (DAD) JOKE: {}".format(joke))
      sameJokeCount = 0
