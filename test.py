import speech

query = "rref [1 0; 0 1]"
intents = speech.getintents(query)
speech.runaction()