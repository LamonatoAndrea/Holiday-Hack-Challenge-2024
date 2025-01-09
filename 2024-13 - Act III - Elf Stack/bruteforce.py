import requests
import json 
import sys
from termcolor import colored

def answerQuestion (session, questionId, answer):
	response = session.get("https://hhc24-elfstack.holidayhackchallenge.com/get_question/{}".format(questionId))
	response_json = json.loads(response.text)
	token = response_json['token']
	question = response_json['question']
	print ("{} --> TRYING ANSWER: {}".format(question, answer))
	answer_json = {"token":token,"answer":answer}
	response = session.post("https://hhc24-elfstack.holidayhackchallenge.com/check_answer", json=answer_json)
	if json.loads(response.text)['correct']:
		print (colored(" --> ANSWER IS CORRECT", "cyan"))
		return True
	else:
		print (colored(" --> WRONG ANSWER", "red"))
		return False

mode = "hard"
known_answers = open("known_answers.txt", "r").read().split("\n")
test_dict = open("dict.txt", "r").read().split("\n")

session = requests.Session()
print (" --> SETTING MODE TO {}".format(mode))	
response = session.post("https://hhc24-elfstack.holidayhackchallenge.com/set_mode", json={"mode":mode})
total_questions = json.loads(response.text)['total_questions']

questionId = 1
for answer in known_answers:
	answerQuestion (session, questionId, answer)
	questionId += 1
correct_answer = False
i = 0
while questionId < total_questions and i < len(test_dict) and not correct_answer:
	correct_answer = answerQuestion (session, questionId, test_dict[i])
	i += 1