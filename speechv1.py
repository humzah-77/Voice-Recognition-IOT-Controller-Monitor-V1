#this program was created by humzah okadia
#this program is LUCY the speech recognition software to control my iot projects 
import speech_recognition as sr
import pyttsx3
import os
import json
import iot_api_client as iot#imports

from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session

engine = pyttsx3.init()#set up text to speech
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
                 #fill this with thing property data
                 }
			resp = devices.properties_v2_publish('Thing_ID','Variable_ID', propertyValue)#replace with ThingID and VariableID
			print("Response from server:")
			return("Lights ON");#what lucy will say
		else:
			propertyValue = {
                 #fill this with thing property data
                 }
			resp = devices.properties_v2_publish('Thing_ID','Variable_ID', propertyValue)#replace with ThingID and VariableID
			print("Response from server:")
			return("Lights Off");
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
		query = command()#get speech command
		query1 = '0'
		if 'Lucy' in str(query) or 'Luci' in str(query):#only do action if the name lucy is called
			print (query)
			if 'Lucy' in str(query):
				commands = str(query).replace('Lucy', '')#remove lucy from command
			if 'Luci' in str(query):
				commands = str(query).replace('Luci', '')
			if 'name' in str(commands):
				querry1 = 'Humzah Okadia'#returns my name
			elif 'celsius' in str(commands) or 'Celsius' in str(commands):#commands
				querry1 = getapi("temp")
			elif 'fahrenheit' in str(commands) or 'Fahrenheit' in str(commands):
				querry1 = getapi("temp2")
			elif 'Humidity' in str(commands) or 'humidity' in str(commands):
				querry1 = getapi("humid")
			elif 'light on' in str(commands) or 'Light on' in str(commands) or 'Light On' in str(commands) or 'light On' in str(commands):
				querry1 = setapi("on")
			elif 'light off' in str(commands) or 'Light off' in str(commands) or 'Light Off' in str(commands) or 'light Off' in str(commands):
				querry1 = setapi("off")
			else:
				querry1 = 'dont understand'

			speak(str(querry1))#say reply to commands

main()