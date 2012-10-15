# This file is part of Merlin.
# Merlin is the Copyright (C)2008,2009,2010 of Robin K. Hansen, Elliot Rosemarine, Andreas Jacobsen.

# Individual portions may be copyright by individual contributors, and
# are included in this collective work with permission of the copyright
# owners.

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
 
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110-1301 USA
 
from Core.exceptions_ import PNickParseError, UserError
from Core.maps import Channel, Command
from Core.db import session
from Core.loadable import loadable, route
from Core.callbacks import Callbacks
from sqlalchemy.sql import desc
from datetime import datetime, timedelta

class help(loadable):
    """Help"""
    usage = " [command]"
    
    @route(r"\S+")
    def command(self, message, user, params):
        pass
    
    @route(r"")
    def execute(self, message, user, params):
        Q = session.query(Command)
        Q = Q.filter(Command.username == user.name)
        Q = Q.filter(Command.command.ilike("help"))
        Q = Q.order_by(desc(Command.command_time))
        if len(Q.all()) > 0:
            time = datetime.now() - Q[0].command_time
            print "DEBUG::: %s" % (time)
            if time.days == 0 and time.seconds < 10:
                message.reply("Slow down!")
                return
        
        commands = []
        message.reply(self.doc+". For more information use: "+self.usage)
        if message.in_chan():
            channel = Channel.load(message.get_chan())
        else:
            channel = None
        for callback in Callbacks.callbacks["PRIVMSG"]:
            try:
                if callback.check_access(message, None, user, channel) is not None:
                    commands.append(callback.name)
            except PNickParseError:
                continue
            except UserError:
                continue
        message.reply("Loaded commands: " + ", ".join(commands))
