import speech

query = "Directions to 37th and market street"
intents = speech.getintents(query)
speech.runaction()