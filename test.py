import assistant

query = "rref [1 0; 0 1]"
intents = assistant.getintents(query)
assistant.runaction()