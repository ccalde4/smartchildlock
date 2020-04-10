from flask import Flask,redirect, url_for, render_template
from flask_ask import Ask, statement, question, session, context,request,version
import json
import requests
import time
import unidecode
import spidev
import RPi.GPIO as GPIO
from lib_nrf24 import NRF24

app = Flask(__name__)
ask = Ask(app, "/child_locks")


locks = ["blue", "green", "red"]
pipes=[[0xe8,0xe8,0xf0,0xf0,0xe1],[0xf0,0xf0,0xf0,0xf0,0xe1]]
GPIO.setmode(GPIO.BCM)
radio= NRF24(GPIO,spidev.SpiDev())
radio.begin(0,17)
radio.setPayloadSize(32)
radio.setChannel(0x76)
radio.setDataRate(NRF24.BR_1MBPS)
radio.setPALevel(NRF24.PA_MAX)
radio.setAutoAck(True)
radio.enableDynamicPayloads()
radio.enableAckPayload()
radio.openWritingPipe(pipes[0])
radio.openReadingPipe(1,pipes[1])
radio.printDetails()




@app.route('/')
def homepage():
	return render_template("index.html")

@app.route('/unlock')
def unlocked():
	radio.write("Unlocked");
	return render_template("index.html")
	
@app.route('/zones')
def zones():
	return render_template("zoning.html")

@app.route('/schedules')
def schedules():
	return render_template("schedules.html")

@app.route('/all_locks')
def all_locks():
	return render_template("all_locks.html")

	

@ask.launch
def start_skill():
	welcome_message = 'Welcome to the smart locks application. What lock would you like to unlock?"'
	return statement(welcome_message)

@ask.intent("UnlockIntent", mapping={'cabinet':'color'})
def unlock_cabinet(color):
	try:
		person = context.System.person.personId
	except:
		return statement("No person object present")
	else:
		if(person in authorized_people):
					if color in locks:
						i=0
						while i < 1:
							radio_msg = list(color)
							while len(radio_msg) < 32:
								radio_msg.append(0)
							radio.write(radio_msg)
							print("Sent the message {}".format(color))
							i +=1
						start = time.time()
						while not radio.available(0):
							time.sleep(1/100)
							if time.time() - start > 2:
								print("Timed out")
								return_msg = "Timed out"
								return statement(return_msg)
						receivedMessage=[]
						radio.read(receivedMessage, radio.getDynamicPayloadSize())
						print("Received :{}".format(receivedMessage))
						radio.stopListening()
						return_msg = 'Unlocked cabinet, {}'.format(color)

						return statement(return_msg)
					else:
						return_msg = 'That lock could not be found'
						return statement(return_msg)
		else:
			return statement("I don't know you or you are not authorized")




@ask.intent("NoIntent")
def no_intent():
	bye_text = 'Goodbye'
	return statement(bye_text)

@ask.intent("PersonIDTestIntent")
def test():
	try:
		person = context.System.person.personId
	except:
		return statement("No person object present")
	else:
		print(person)
		if(person == "amzn1.ask.person.AH6KQDCMUWY44HKGYMXWVOFL7NNRCZ6DUVJ5PH5S5FOV3GPCG762NOJWNM2QLPGLLUUSTWA3S4V7HCLAQQPKDLNSCPRTEX62TM2SC7MG"):
			return statement("You are Austin")
		elif(person == "amzn1.ask.person.AH6KQDCMUWY44HKGYMXWVOFL7NNRCZ6DUVJ5PH5S5FOV3GPCG762NNKUK44AM5KMDCAO5R57C3NEG7AZNFFUHP7ITGHVXFFIN64EU5YO"):
			print(person)
			return statement("You are Gary but you are unauthorized to use this skill")
		else:
			return statement("I don't know you")

if __name__=='__main__':
	app.run(debug=True)
