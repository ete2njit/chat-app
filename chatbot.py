from random import choice

class Chatbot:
    name = ""
    key = ""
    
    def __init__(self, name="chatbot", key="botkey"):
        self.name=name
        self.key=key
    
    def about(self):
        return "A long time ago, in a chat room far far away there lived a chatbot with functionality that can be found when typing !! help"
    
    def help(self):
        return "Type '!! about' for info about me! Type '!! funtranslate <message>' and I will translate your message. '!! randcase <message>' and I'll return your message with random capitalization."
        
    def randcase(self, sentence):
        return ''.join(choice((str.upper, str.lower))(c) for c in sentence)
    
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
        
        
        
        return "'" + command.lower() + "' is not a recognized command. Type !! help for info about recognized commands"
        
    def isCommand(self, argument):
        if argument.strip()[0] == '!' and argument.strip()[1] == '!':
            return True
        return False
        