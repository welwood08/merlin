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

# Module by Martin Stone
 
from Core.db import session
from Core.maps import Channel
from Core.loadable import loadable, route

class showchan(loadable):
    """Show details of an existing channel."""
    usage = " <chan>"
    access = 1 # Admin
    
    @route(r"([^\*\s]\S+)", access = "showchan")
    def execute(self, message, user, params):
        
        chan = params.group(1)
        if chan[0] != "#":
            chan = "#" + chan

        c = Channel.load(chan)
        if c is None:
            message.reply("No such channel: '%s'" % (chan,))
            return
        
        message.reply("%s: %s (Max: %s)" % (c.name, c.usergroup.name, c.maxgroup.name))


    @route(r"\*", access = "showchan")
    def showall(self, message, user, params):

        reply = []
        
        for c in session.query(Channel).all():
            reply.append("%s: %s (Max: %s)" % (c.name, c.usergroup.name, c.maxgroup.name))
        
        message.reply("\n".join(reply))
