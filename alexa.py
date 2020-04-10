from flask import Flask
from flask_ask import Ask, statement, question, session, context,request,version
import json
import requests
import unidecode

app = Flask(__name__)
ask = Ask(app,"/child_locks")
locks = ["green","red","blue"]

#Startup Intent for no specified action
@ask.launch
def start_skill():
	welcome_message = 'Welcome to the smart locks application. What lock would you like to unlock?"'
	return statement(welcome_message)

#Skill called but no action required
@ask.intent("NoIntent")
def no_intent():
	bye_text = 'Goodbye'
	return statement(bye_text)

#Intent to control unlocking cabinet
@ask.intent("UnlockIntent", mapping={'cabinet':'color'})
def unlock_cabinet(color):
	try:
		person = context.System.person.personId
	except:
		return statement("No person object present")
	else:
		#if(person in authorized_people):
					if color in locks:
						return_msg = 'Unlocked cabinet, {}'.format(color)

						return statement(return_msg)
					else:
						return_msg = 'That lock could not be found'
						return statement(return_msg)
		#else:
			#return statement("I don't know you or you are not authorized")

if __name__=='__main__':
	app.run(port=8000)
