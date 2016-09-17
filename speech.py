import mechanize
from wit import Wit
import wolframalpha
import speech_recognition as sr
import googlemaps
import json
import math
import urllib2
import gmplot
import string
import subprocess
from datetime import datetime
witclient = Wit(access_token="Y2TXOOVIUF5444QL5U3OYV7MGRLRIJUW", actions={})
wolframclient = wolframalpha.Client('KHE5G2-42E4UX5AL3')
googleclient = googlemaps.Client(key='AIzaSyDgc8KUW9ZoOUz65bD2mfSElHj-HmztEaI')

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
    # Setup
    currentlocation = locationlookup()
    lat = []
    lng = []
    pods.append(Pod())
    pods.append(Pod())
    pods[0].name = "Map"
    pods[1].name = "Instructions"
    # Get Destination
    if 'location' in witai.response['entities']:
        placename = witai.response['entities']['location'][0]['value']
    else:
        splitindex = witai.query.rfind(' ',0,witai.query.rfind(' ')-1)
        placename = witai.query[splitindex:]
    destination = googleclient.places(placename,location=currentlocation)
    destination = destination['results'][0]['geometry']['location']
    # Get Directions
    directions = googleclient.directions(currentlocation,destination,mode="driving",departure_time=datetime.now())
    # Update Pods and Long/Lat arrays
    pods[0].imgurl = "map.html"
    pods[0].text = "Directions from " + directions[0]['legs'][0]['start_address'] + " to " + directions[0]['legs'][0]['end_address']
    lat.append(directions[0]['legs'][0]['steps'][0]['start_location']['lat'])
    lng.append(directions[0]['legs'][0]['steps'][0]['start_location']['lng'])
    for step in directions[0]['legs'][0]['steps']:
        pods[1].text += step['html_instructions'].replace("<b>","").replace("</b>","").replace('<div style="font-size:0.9em">','').replace("</div>","") + "\n"
        lat.append(step['end_location']['lat'])
        lng.append(step['end_location']['lng'])
    # Create Map
    zoom = zoomlevel(directions[0]['bounds']['northeast']['lat'],directions[0]['bounds']['southwest']['lat'],directions[0]['bounds']['northeast']['lng'],directions[0]['bounds']['southwest']['lng'])
    gmap = gmplot.GoogleMapPlotter(lat[0],lng[0],zoom)
    gmap.plot(lat,lng,'cornflowerblue',edge_width=10)
    gmap.draw("map.html")


def matlab():
    subprocess.call(["/usr/bin/open", "-W", "-n", "-a", "/Applications/MATLAB.app"])


def calendar():
    print("Running calendar action")


# HELPER FUNCTIONS


actions = {
    'Wolfram' : wolfram,
    'Directions' : directions,
    'Calendar' : calendar,
    'Matlab' : matlab
}

def zoomlevel(maxlat,minlat,maxlng,minlng):
    latdiff = abs(maxlat - minlat)*120/180
    lngdiff = (maxlng - minlng)*100/360
    if lngdiff < 0:
        lngdiff += 100
    scope = max(latdiff,lngdiff)
    zoom = 1.4*math.log(1/(8000*scope)) + 20.5
    if zoom > 18:
        zoom = 18
    elif zoom < 2:
        zoom = 2
    return zoom
    

def locationlookup():
    try:
        return json.load(urllib2.urlopen('http://ipinfo.io/json'))['loc']
    except urllib2.HTTPError:
        return False
