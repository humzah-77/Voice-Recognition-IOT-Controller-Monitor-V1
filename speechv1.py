#this program was created by humzah okadia
#this program is LUCY the speech recognition software to control my iot projects 
import speech_recognition as sr
import pyttsx3
import os
import json
import wolframalpha
import iot_api_client as iot
import time
import ssl
import webbrowser
from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session

ssl._create_default_https_context = ssl._create_unverified_context#allow wolframalpha
app_id = 'APIKEY'#get key from wolfram alpha
client = wolframalpha.Client(app_id)
engine = pyttsx3.init()#initialize speak
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[10].id)

def speak(audio):#text to speech 
	engine.say(audio)
	engine.runAndWait()
	

def getapi(name):#get data fron api
	CLIENT_ID = os.getenv("CLIENT_ID")  # get a valid one from your Arduino Create account
	CLIENT_SECRET = os.getenv("CLIENT_SECRET")  # get a valid one from your Arduino Create account


	# Setup the OAuth2 session that'll be used to request the server an access token
	oauth_client = BackendApplicationClient("Client_ID")
	token_url = "https://api2.arduino.cc/iot/v1/clients/token"

	oauth = OAuth2Session(client=oauth_client)
	token = oauth.fetch_token(
		token_url=token_url,
		client_id="CLIENT_ID",#replace these with the two client values when you create the api
		client_secret="CLIENT_SECRET",
		include_client_id=True,
		audience="https://api2.arduino.cc/iot",
		)
		# If we get here we got the token, print its expiration time
	print("Got a token, expires in {} seconds".format(token.get("expires_in")))
	    # Now we setup the iot-api Python client, first of all create a
	    # configuration object. The access token goes in the config object.
	client_config = iot.Configuration(host="https://api2.arduino.cc/iot")
	    # client_config.debug = True
	client_config.access_token = token.get("access_token")

	    # Create the iot-api Python client with the given configuration
	client = iot.ApiClient(client_config)

	    # Each API model has its own wrapper, here we want to interact with
	    # devices, so we create a DevicesV2Api object
	devices = iot.PropertiesV2Api(client)
	    # Get a list of devices, catching the specific exception
	try:
		if name == "temp":#get dth11 celciciu temp value 
			resp = devices.properties_v2_show('Thing_ID','Variable_ID')#replace with ThingID and VariableID
			print("Response from server:")
			print(resp.last_value)
			return resp.last_value
		elif name == "temp2":#get dth11 farenheight temp value
			resp = devices.properties_v2_show('Thing_ID','Variable_ID')#replace with ThingID and VariableID
			print("Response from server:")
			print(resp.last_value)
			return resp.last_value
		elif name == "humid":#get dth11 humidity value
			resp = devices.properties_v2_show('Thing_ID','Variable_ID')#replace with ThingID and VariableID
			print("Response from server:")
			print(resp.last_value)
			return resp.last_value

	except iot.ApiException as e:#if error
		print("An exception occurred: {}".format(e))


def setapi(status):#send data to api
	CLIENT_ID = os.getenv("CLIENT_ID")  # get a valid one from your Arduino Create account
	CLIENT_SECRET = os.getenv("CLIENT_SECRET")  # get a valid one from your Arduino Create account


	# Setup the OAuth2 session that'll be used to request the server an access token
	oauth_client = BackendApplicationClient("Client_ID")
	token_url = "https://api2.arduino.cc/iot/v1/clients/token"

	oauth = OAuth2Session(client=oauth_client)
	token = oauth.fetch_token(
		token_url=token_url,
		client_id="CLIENT_ID",#replace these with the two client values when you create the api
		client_secret="CLIENT_SECRET",
		include_client_id=True,
		audience="https://api2.arduino.cc/iot",
		)
		# If we get here we got the token, print its expiration time
	print("Got a token, expires in {} seconds".format(token.get("expires_in")))
	# Now we setup the iot-api Python client, first of all create a
	# configuration object. The access token goes in the config object.
	client_config = iot.Configuration(host="https://api2.arduino.cc/iot")
	# client_config.debug = True
	client_config.access_token = token.get("access_token")

	# Create the iot-api Python client with the given configuration
	client = iot.ApiClient(client_config)

	# Each API model has its own wrapper, here we want to interact with
	# devices, so we create a DevicesV2Api object
	devices = iot.PropertiesV2Api(client)
	# Get a list of devices, catching the specific exception
	try:
		if status == 'on':
			propertyValue = {
				'value': True,
				'last_value': False,
				'max_value': None,
				'min_value': None,
				'name': 'openlock',
				#fill the rest with thing property data
                 #fill this with thing property data
                 }
			resp = devices.properties_v2_publish('Thing_ID','Variable_ID', propertyValue)#replace with ThingID and VariableID
			print("Response from server:")
			return("Lights ON");#what lucy will say
		elif status == 'off':
			propertyValue = {
				'value': False,
				'last_value': True,
				'max_value': None,
				'min_value': None,
				'name': 'openlock',
                 #fill this with thing property data
                 }
			resp = devices.properties_v2_publish('Thing_ID','Variable_ID', propertyValue)#replace with ThingID and VariableID
			print("Response from server:")
			return("Lights Off");
		else:
			propertyValue = {#turn lock on 
                'value': True,
				'last_value': False,
				'max_value': None,
				'min_value': None,
				'name': 'openlock',
				#fill the rest with thing property data
                 }
			resp = devices.properties_v2_publish('Thing_ID','Variable_ID', propertyValue)
			print("Response from server:")
			propertyValue = {#turn lock back off after 3 second
                'value': False,
				'last_value': True,
				'max_value': None,
				'min_value': None,
				'name': 'openlock',
				#fill the rest with thing property data
                 }
			resp = devices.properties_v2_publish('Thing_ID','Variable_ID', propertyValue)
			print("Response from server:")
			return("Locke Opened");
	except iot.ApiException as e:
	    print("An exception occurred: {}".format(e))
	    


def command():#get speech and turn into string
    listener = sr.Recognizer()
    with sr.Microphone() as source:#set up microphone
        print("Lucy: Listening...")
        audio= listener.listen(source)
        try:    
            query = listener.recognize_google(audio)
            print("master:" + query)
            return query#return strings
        except:
            print("Try Again")
            

def main():
	while True:
		query = str(command()).lower()#turn into lowercase to avoid confusion
		print(query)#for debugging
		querry1 = "no answer"#if not changed say no onswer
		if 'luci' in str(query): 
			query = str(query).replace('luci', 'lucy')#sometimes reads lucy as luci
		if 'lucy' in str(query):

			commands = str(query).replace('lucy', '')#remove lucy from command
			print(commands)


			if 'hey ' in commands  or'hi ' in commands or 'hello ' in commands or 'yo ' in commands  or 'what`s up' in commands:
				querry1 = 'how can I help you, sir'#greetinfs


			elif 'thanks ' in commands or 'thank you 'in commands or 'respect ' in commands:
				querry1 = 'you welcome, sir'#reply to thanks

					#explains what she is 
			elif commands == ' what were you created for'  or commands ==' who are you' or commands ==' what are you':
				querry1 = 'My name is Lucy. I am a voice recognition software created by Humzah Okadia to monitor and control his iot devices'
				#returns her creator
			elif 'name' in str(commands) or str(commands) == 'who created you' or str(commands) == 'who is your creator':
				querry1 = 'Humzah Okadia'
				#manually search wolfram alpha
			elif 'manual search' in str(commands) or 'manuel search' in str(commands):
				question = input('Type something to ask wolframalpha: ')
				res = client.query(question)#get question from terminal
				try:
					answer = next(res.results).text
					print(answer)#ask wolfram
					querry1 = str(answer)
				except StopIteration:
				    querry1 ="No results"

			elif ' answer' in str(commands):#speak your question to wolfram
				querry1 = str(commands).replace('answer ', '')
				print(querry1)
				res = client.query(querry1)
				try:
					answer = next(res.results).text
					print(answer)
					querry1 = str(answer)
				except StopIteration:
				    querry1 ="No results"

			elif 'look up'  in commands:#to googole seach somehting
				querry1 = commands.replace("look up", "")
				webbrowser.open_new_tab("https://www.google.com/search?q="+querry1)
			
			elif 'celsius' in str(commands):#controls my iot devices
				querry1 = getapi("temp")
			elif 'fahrenheit' in str(commands):
				querry1 = getapi("temp2")
			elif 'humidity' in str(commands):
				querry1 = getapi("humid")
			elif 'light on' in str(commands):
				querry1 = setapi("on")
			elif 'light off' in str(commands):
				querry1 = setapi("off")
			elif 'lock' in str(commands):
				querry1 = setapi("lock")
			else:
				querry1 = 'dont understand'

			speak(str(querry1))


main()
