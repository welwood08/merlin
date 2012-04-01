from Core.loadable import loadable, route

class newb(loadable):

    @route()
    def execute(self, message, user, params):

        webby = ["lolidunno.co.uk",]
        message.reply("set !pref planet=*:*:* and !pref password=***** then you can sign into "+" | ".join(webby))
