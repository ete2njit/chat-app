class Chatbot:
    name = ""
    key = ""
    
    def __init__(self, name="chatbot", key="botkey"):
        self.name=name
        self.key=key
    
    def about(self):
        return "A long time ago, in a chat room far far away there lived a chatbot with functionality that can be found when typing !! help"
    
    def help(self):
        return "Type '!! about' for info about me! Type '!! funtranslate <message>' and I will translate your message!"
    
    def process(self, argument):
        return argument
        
    def isCommand(self, argument):
        if argument.strip()[0] == '!' and argument.strip()[1] == '!':
            return True
        return False
        