#!/bin/bash
lxterminal --command './ngrok http 8001'
lxterminal --command './ngrok http 5000'
lxterminal --command 'python3 ~/Desktop/smartchildlock/alexa.py'
lxterminal --working-directory=/home/austin/Desktop/smartchildlock/webapp --command 'python3 webapprun.py'
lxterminal --working-directory=/home/austin/Desktop/smartchildlock/webapp --command 'python3 time_monitor.py'
