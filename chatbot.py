from random import choice
import requests

class Chatbot:
    name = ""
    key = ""
    
    def __init__(self, name="chatbot", key="botkey"):
        self.name=name
        self.key=key
    
    def about(self):
        return "A long time ago, in a chat room far far away there lived a chatbot with functionality that can be found when typing !! help"
    
    def help(self):
        return ("Type '!! about' for info about me! Type '!! funtranslate <message>' and I will translate your message. " +
                "Type '!! randcase <message>' and I'll return your message with random capitalization. " +
                "Type '!! funtranslate <message>' and Master Yoda will have a look at your message and rephrase it for you. " +
                "Type '!! joke' and I will tell you a programming joke! We all love those! Right?")
        
    def randcase(self, sentence):
        return ''.join(choice((str.upper, str.lower))(c) for c in sentence)
        
    def joke(self):
        response = requests.get('https://official-joke-api.appspot.com/jokes/programming/random')
        joke_content = response.json()[0]
        
        if response:
            return joke_content['setup'] + " " + joke_content['punchline']
        return "Error when fetching joke from the official joke api"
        
    def translate(self, sentence):
        response = requests.get("https://api.funtranslations.com/translate/yoda.json?text=" + sentence)
        translation = response.json()
        
        if response:
            return translation["contents"]["translated"]
        return "Error when fetching translation of '" + sentence + "' from Master Yoda"
        
    
    def process(self, argument):
        line = argument.strip()[2:].strip()
        arg_list = line.split()
        command = arg_list[0]
        param = " ".join(arg_list[1:])
        
        if command.lower() == "about":
            return self.about()
        if command.lower() == "help":
            return self.help()
        if command.lower() == "randcase":
            return self.randcase(param)
        if command.lower() == "joke":
            return self.joke()
        if command.lower() == "funtranslate":
            return self.translate(param)
        
        
        
        return "'" + command.lower() + "' is not a recognized command. Type !! help for info about recognized commands"
        
    def isCommand(self, argument):
        if argument.strip()[0] == '!' and argument.strip()[1] == '!':
            return True
        return False
        