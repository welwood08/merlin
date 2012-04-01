from Core.loadable import loadable, route
from Core.config import Config

class newb(loadable):
    
    @route()
    def execute(self, message, user, params):
        
        links = [Config.get("URL","arthur"),]
        
        message.reply(self.url("Sign up to netgamers.org, Log into P and set usermode +ix - Do !pref password=*** and !pref planet=*:*:* IN A PM TO ME! You can then sign into: "+" | ".join(links), user))