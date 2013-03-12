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
 
from sqlalchemy.exc import IntegrityError
from Core.config import Config
from Core.db import session
from Core.maps import Channel, Group
from Core.loadable import loadable, route, require_user

class addchan(loadable):
    """Adds a channel with the given level with maxlevel equal to your own access level"""
    usage = " <chan> <level> [maxlevel]"
    access = 1 # Admin
    
    @route(r"(#\S+)\s+(\S+)(?:\s+(\S+))?", access = "addchan")
    @require_user
    def execute(self, message, user, params):
        
        chan = params.group(1)
        access = params.group(2)
        maxaccess = params.group(3)
        g = Group.load(access)
        if g is None:
            message.reply("Invalid access level '%s'" % (access,))
            return
        if maxaccess:
            mg = Group.load(maxaccess)
            if mg is None:
                message.reply("Invalid access level '%s'" % (maxaccess,))
                return
        
        if (not user.is_admin) and (g.admin_only or (maxaccess and mg.admin_only)):
            message.reply("You may not add a channel with higher access than your own")
            return
        
        try:
            session.add(Channel(name=chan, userlevel=g.id, maxlevel=mg.id if maxaccess else g.id))
            session.commit()
            message.reply("Added chan %s with access %s (max: %s)" % (chan,access,))
            message.privmsg("set %s autoinvite on" %(chan,),Config.get("Services", "nick"));
            message.privmsg("invite %s" %(chan,),Config.get("Services", "nick"));
        except IntegrityError:
            session.rollback()
            message.reply("Channel %s already exists" % (chan,))
