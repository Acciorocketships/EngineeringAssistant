import mechanize
import wolframalpha
import json
import urllib
import urllib2
import subprocess
import googlemaps
import speech_recognition as sr
import PIL
from PIL import Image
from wit import Wit
from datetime import datetime
witclient = Wit(access_token="Y2TXOOVIUF5444QL5U3OYV7MGRLRIJUW", actions={})
wolframclient = wolframalpha.Client('KHE5G2-42E4UX5AL3')
googleclient = googlemaps.Client(key='AIzaSyDgc8KUW9ZoOUz65bD2mfSElHj-HmztEaI')


class Pod:
	def __init__(self):
		self.name = ""
		self.text = ""
		self.img = ""

class Witai:
	def __init__(self):
		self.query = ""
		self.response = {}
		self.intents = []

pods = []
witai = Witai()







# FUNCTIONS

def getintents(query):
	witai.intents = []
	witai.query = query
	try:
		witai.response = witclient.message(query)
	except:
		pass
	if 'intents' in witai.response['entities']:
		for intentnum in range(0,len(witai.response['entities']['intents'])):
			witai.intents.append(witai.response['entities']['intents'][intentnum]['value'])
	return witai.intents


def runaction():
	for intent in witai.intents:
		try:
			actions[intent]()
		except:
			pass
	if len(witai.intents)==0:
		try:
			actions["Wolfram"]()
		except:
			pass
	if len(pods)==0:
		try:
			actions["Chatbot"]()
		except:
			pass


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


def speech2text():
	recognizer = sr.Recognizer()
	with sr.Microphone() as source:
		audio = recognizer.listen(source)
	text = recognizer.recognize_google(audio)
	return text


def bot(text):
	br = mechanize.Browser()
	br.set_handle_robots(False)
	try:
		br.open('http://pandorabots.com/pandora/talk?botid=cf7aa84b0e34555c')
	except:
		return ""
	br.select_form(nr=0)
	br["input"] = text
	html = br.submit().read()
	linkstart = html.find("</form>") + 16
	linkend = html.find("</p>", linkstart)
	response = html[linkstart:linkend]
	response.replace('<br>','\n')
	return response


def wolfram():
	response = wolframclient.query(witai.query)
	for pod in response['pod']:
		pods.append(Pod())
		pods[-1].name = pod['@title']
		if isinstance(pod['subpod'],list):
			pods[-1].text = pod['subpod'][0]['plaintext']
			pods[-1].img = "%s.png" % (pods[-1].name)
			urllib.urlretrieve(pod['subpod'][0]['img']['@src'], "%s.png" % (pods[-1].name))
		else:
			pods[-1].text = pod['subpod']['plaintext']
			pods[-1].img = "%s.png" % (pods[-1].name)
			urllib.urlretrieve(pod['subpod']['img']['@src'], "%s.png" % (pods[-1].name))


def directions():
	# Setup
	currentlocation = locationlookup()
	lat = []
	lng = []
	pods.append(Pod())
	pods.append(Pod())
	pods[-2].name = "Map"
	pods[-1].name = "Instructions"
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
	if (len(directions) != 0):
		# Update Pods and Long/Lat arrays
		pods[-2].img = 'map-full.png'
		pods[-2].text = 'Directions from ' + directions[0]['legs'][0]['start_address'] + " to " + directions[0]['legs'][0]['end_address']
		lat.append(directions[0]['legs'][0]['steps'][0]['start_location']['lat'])
		lng.append(directions[0]['legs'][0]['steps'][0]['start_location']['lng'])
		for step in directions[0]['legs'][0]['steps']:
			pods[-1].text += step['html_instructions'].replace("<b>","").replace("</b>"," ").replace('<div style="font-size:0.9em">','').replace("</div>"," ") + "\n"
			lat.append(step['end_location']['lat'])
			lng.append(step['end_location']['lng'])
		start = '%0.7f,%0.7f' % (lat[1],lng[1])
		end = '%0.7f,%0.7f' % (lat[-1],lng[-1])
		mapcommand = 'https://www.google.com/maps/preview?saddr=%s&daddr=%s&dirflg=r' % (start,end)
		subprocess.call(['webkit2png',mapcommand,'-W 1100','-H 600','-F','-o map'])
		img = Image.open(' map-full.png')
		img = img.resize((586, 330), PIL.Image.ANTIALIAS)
		img.save('map-full.png')
		


def openapp():
	application = witai.query.rsplit(" ",1)[-1]
	path = "/Applications/" + application + ".app"
	subprocess.call(["/usr/bin/open", "-W", "-n", "-a", path])


def chatbot():
	response = ""
	response = bot(witai.query)
	if len(response) != 0:
		pods.append(Pod())
		pods[-1].name = "GLADoS:"
		pods[-1].text = response









# HELPER FUNCTIONS


actions = {
	'Wolfram' : wolfram,
	'Directions' : directions,
	'Openapp' : openapp,
	'Chatbot' : chatbot
}
	

def locationlookup():
	try:
		return json.load(urllib2.urlopen('http://ipinfo.io/json'))['loc']
	except urllib2.HTTPError:
		return False


if __name__ == "__main__":
	query = speech2text()
	print(query)
	intents = getintents(query)
	runaction()
	for pod in pods:
		print(pod.name)
		print(pod.text)


#import matlab.engine as matlab
#matlabclient = matlab.start_matlab()
#def matlab():
#	lb = witai.query.find('[')
#	ub = witai.query.find(']',lb)
#	if lb != -1 and ub != -1:
#		matrixstring = witai.query[lb:ub]
#		numrows = matrixstring.count(';') + 1
#		matrixstring = matrixstring.replace(","," ").replace(";"," ")[1:]
#		output = matlabclient.reducematrix(matrixstring,numrows)
#		matrix = ''
#		for x in range(numrows):
#			line = '['
#			for y in range(len(output[0])):
#				line += '%6.3f ' % output[x][y]
#			line += ']\n'
#			matrix += line
#		pods.append(Pod())
#		pods[-1].name = "Matrix Row Reduction"
#		pods[-1].text = matrix
