import mechanize
from wit import Wit
import wolframalpha
import speech_recognition as sr
import googlemaps
import json
import urllib2
import gmplot
from datetime import datetime
witclient = Wit(access_token="Y2TXOOVIUF5444QL5U3OYV7MGRLRIJUW", actions={})
wolframclient = wolframalpha.Client('KHE5G2-42E4UX5AL3')
googleclient = googlemaps.Client(key='AIzaSyDpiP-1JYBIfuvfgmuDdxzhYX4FW-XmC0k')

class Pod:
    def __init__(self):
        self.name = ""
        self.text = ""
        self.imgurl = ""

class Witai:
    def __init__(self):
        self.query = ""
        self.response = {}
        self.intents = []
        #self.arguments = []

pods = []
witai = Witai()


# FUNCTIONS


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
    witai.query = query
    witai.response = witclient.message(query)
    if 'intents' in witai.response['entities']:
        for intentnum in range(0,len(witai.response['entities']['intents'])):
            witai.intents.append(witai.response['entities']['intents'][intentnum]['value'])

def runaction():
    for intent in witai.intents:
        actions[intent]()    

def wolfram():
    response = wolframclient.query(witai.query)
    for result in response.results:
        pods.append(Pod())
        pods[-1].name = result['@title']
        pods[-1].text = result['subpod']['plaintext']
        pods[-1].imgurl = result['subpod']['img']['@src']

def directions():
    currentlocation = location_lookup()['loc']
    lat = []
    lng = []
    instructions = []
    lat.append(float(currentlocation[:currentlocation.find(",")-1]))
    lng.append(float(currentlocation[currentlocation.find(",")+1:]))
    directions = googleclient.directions(currentlocation,"Concord,MA",mode="driving")
    gmap = gmplot.GoogleMapPlotter(lat[0],lng[0],16)
    gmap.plot(lat,lng,'cornflowerblue',edge_width=10)
    gmap.draw("mymap.html")


def calendar():
    print("Running calendar action")


# HELPER FUNCTIONS

actions = {
    'Wolfram' : wolfram,
    'Directions' : directions,
    'Calendar' : calendar
}

def location_lookup():
  try:
    return json.load(urllib2.urlopen('http://ipinfo.io/json'))
  except urllib2.HTTPError:
    return False
