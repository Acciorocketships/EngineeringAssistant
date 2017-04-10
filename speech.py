import mechanize
import numpy as np
from scipy.io import wavfile
from scipy import signal
import speech_recognition as sr
import random

def text2speech(text, savefile=True):
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


def glados(text, savefile=True):
	text2speech(text,True)
	crystal = wavfile.read('output.wav')
	X = np.fft.fft(crystal[1])
	N = len(X)

	gauss1center = N*3/4
	gauss2center = N*1/4
	gauss1sigma = N*1/10
	gauss2sigma = N*1/10
	gaussperc = 0
	switchtime = 1

	Xnew = X

	gauss1 = signal.gaussian(2*(N-gauss1center),gauss1sigma)
	Xnew[N-2*gauss1center-1:N-1] = Xnew[N-2*gauss1center-1:N-1] + gaussperc * np.multiply(Xnew[0:2*(gauss1center-N)], gauss1)
	gauss2 = signal.gaussian(2*(gauss2center-N),gauss2sigma)
	Xnew[0:2*(gauss2center-N)] = Xnew[0:2*(gauss2center-N)] + gaussperc * np.multiply(Xnew[0:2*(gauss2center-N)], gauss2)

	Xnew = np.real(Xnew)
	for n in range(0,N-crystal[0]*switchtime-1,crystal[0]*switchtime):
		freq = pow(-1,random.randrange(0,1)) * np.cos(random.random()/30*np.array(range(0,crystal[0]*switchtime)))
		Xnew[n:n+crystal[0]*switchtime] = np.multiply(signal.hilbert(Xnew[n:n+crystal[0]*switchtime]), signal.hilbert(freq))

	Xnew = Xnew / 5

	glados = np.fft.ifft(Xnew)
	glados = np.int16(np.round(np.real(glados)))
	if savefile:
		wavfile.write("glados.wav",crystal[0],glados)
	return glados


if __name__ == '__main__':
	glados("It's been a long time. how have you been")