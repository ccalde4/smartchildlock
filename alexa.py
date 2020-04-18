from flask import Flask
from flask_ask import Ask, statement, question, session, context,request,version
import json
import requests
import unidecode
import flask_sqlalchemy as SQLAlchemy
from dbschema import db, Lock, Zone, Person
#from RadioControl import init_radio, unlock_function


app = Flask(__name__)
ask = Ask(app,"/child_locks")
#init_radio() This line commented out due to no longer being able to prototype on RPi


#Startup Intent for no specified action
@ask.launch
def start_skill():
	welcome_message = 'Welcome to the smart locks application. What lock would you like to unlock?'
	return question(welcome_message)

#Skill called but no action required
@ask.intent("NoIntent")
def no_intent():
	bye_text = 'Goodbye'
	return statement(bye_text)

#Intent to control unlocking cabinet
@ask.intent("UnlockIntent", mapping={'cabinet':'color'})
def unlock_cabinet(color):
	authorized_people = Person.query.all()
	locks = Lock.query.all()
	try:
		person = context.System.person.personId
	except:
		return statement("No person object present")
	else:
		for authorized_person in authorized_people:
			if person == authorized_person.amazon_id:
				for lock in locks:
					if (color.upper()==lock.lock_name.upper()):
						#unlock_function(color.upper()) This line commented out due to COVID19
						return_msg = 'Unlocked cabinet, {}'.format(lock.lock_name)
						return statement(return_msg)
				else:
					return statement("That lock could not be found.")
			else:
				return statement("You are not authorized")

@ask.intent("AMAZON.FallbackIntent")
def not_understood():
	return statement("Sorry, but your request could not be understood")

@ask.intent("AMAZON.CancelIntent")
def cancel():
	return statement("Cancelled")

@ask.intent("AddPersonIntent")
def get_person():
	authorized_people = Person.query.all()
	try:
		person = context.System.person.personId
	except:
		return statement("No person object present")
	else:
		for authorized_person in authorized_people:
			if(person==authorized_person.amazon_id):
				return question("Would you like to add a new voice user?")

@ask.intent("YesIntent")
def yes_intent():
	return question("In order to add a new person, make sure they have already setup their Amazon Voice Profile. Otherwise, have the new user say Add Their Name to Authorized Users")

@ask.intent("NoIntent")
def no_intent():
	return statement("No new user was added")

@ask.intent("NewUserIntent", mapping={'name':'name'})
def new_user(name):
	return statement("You have successfully added Austin to authorized users")
	try:
		person = context.System.person.PersonId
	except:
		return statement("The person was unrecognized. Make sure they have registered their voice with Amazon")
	else:
		new_user = Person(person_name=name,amazon_id=person)
		db.session.add(new_user)
		try:
			db.session.commit()
		except:
			return statement("An error has occurred. No new user added")
		else:
			return statement("You have been succesfully added {}".format(name))


if __name__=='__main__':
	app.run(port=8001)
