import speech
import tungsten

query = "What is the derivative of x squared"

intents = speech.getintents(query)
speech.runaction(intents,query)

#speech.text2speech(speech.chatbot(query),True)
#print(speech.speech2text())

