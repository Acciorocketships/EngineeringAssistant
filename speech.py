import mechanize
from wit import Wit
from Tkinter import *
import wolframalpha
import speech_recognition as sr
access_token = "Y2TXOOVIUF5444QL5U3OYV7MGRLRIJUW"
client = Wit(access_token=access_token, actions={})
wolframclient = wolframalpha.Client('AQV84A-YPJLV47P5P')


def text2speech(text, savefile):
    url = 'http://www.wizzardspeech.com/att_demo.html'
    br = mechanize.Browser()
    br.set_handle_robots(False)
    br.open(url)
    br.select_form(nr=0)
    br['speaktext'] = text
    br['speaker'] = ['crystal16']
    submitlink = br.submit()
    html = submitlink.read()
    linkstart = html.find('MyFile=')
    linkend = html.find('.wav')
    filename = html[linkstart + 7:linkend + 4]
    data = br.open('http://www.wizzardspeech.com/php_tmp/' + filename).read()
    if savefile:
        with open('output.wav', 'wb') as file:
            file.write(data)
    return data


def chatbot(text):
	br = mechanize.Browser()
	br.set_handle_robots(False)
	br.open('http://pandorabots.com/pandora/talk?botid=cf7aa84b0e34555c')
	br.select_form(nr=0)
	br["input"] = text
	html = br.submit().read()
	linkstart = html.find("</form>") + 16
	linkend = html.find("</p>", linkstart)
	response = html[linkstart:linkend]
	return response

def speech2text():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        audio = recognizer.listen(source)
    text = recognizer.recognize_google(audio)
    return text


def getintents(query):
    resp = client.message(query)
    intents = []
    if len(resp['entities']) != 0:
        for intentnum in range(0,len(resp['entities']['intents'])):
            intents.append(resp['entities']['intents'][intentnum]['value'])
    return intents

def runaction(intents,query):
    for intent in intents:
        actions[intent](query)    

def wolfram(query):
    print(query)

def directions():
    print("Running directions action")

def calendar():
    print("Running calendar action")

actions = {
    'Wolfram' : wolfram,
    'Directions' : directions,
    'Calendar' : calendar
}
