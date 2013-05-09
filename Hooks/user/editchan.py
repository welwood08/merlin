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
from Core.maps import Channel, Group
from Core.loadable import loadable, route, require_user

class editchan(loadable):
    """Edits the level and, optionally, maxlevel of an existing channel"""
    usage = " <chan> <level> [maxlevel]"
    access = 1 # Admin
    
    @route(r"(#\S+)\s+(\S+)(?:\s+(\S+))?", access = "editchan")
    @require_user
    def execute(self, message, user, params):
        
        chan = params.group(1)
        access = params.group(2)
        maxaccess = params.group(3)

        c = Channel.load(chan)
        if c is None:
            message.reply("'%s'? Is that even a channel?" % (chan,))
            return
        g = Group.load(access)
        if g is None:
            message.reply("Invalid access level '%s'" % (access,))
            return
        if maxaccess:
            mg = Group.load(maxaccess)
            if mg is None:
                message.reply("Invalid access level '%s'" % (maxaccess,))
                return
        
        if (not user.is_admin) and ((g.admin_only or (maxaccess and mg.admin_only)) or c.usergroup.admin_only or (maxaccess and c.maxgroup.admin_only)):
            message.reply("You may not edit a channel with higher access than your own")
            return

        c.usergroup = g
        if maxaccess:
            c.maxgroup = mg
        session.commit()
        message.reply("Edited channel %s access to %s%s" % (chan, access, (" (max: %s)" % maxaccess) if maxaccess else ""))
