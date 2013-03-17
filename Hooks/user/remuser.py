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
 
from Core.config import Config
from Core.db import session
from Core.maps import User
from Core.chanusertracker import CUT
from Core.loadable import loadable, route, require_user

class remuser(loadable):
    """Permenantly delete a user"""
    usage = " <user>"
    access = 1 # Admin
    
    @route(r"(\S+)", access = "remuser")
    @require_user
    def execute(self, message, user, params):
        
        username = params.group(1)
        member = User.load(name=username, active=False)
        if member is None:
            message.alert("No such user '%s'" % (username,))
            return
        if member.group.admin_only and not user.is_admin:
            message.reply("You may not remove %s; they are in the %s group." %(member.name, member.group.name,))
            return
        
        for chan in member.group.autochannels:
            message.privmsg("remuser %s %s" %(chan.channel.name, member.name), Config.get("Services", "nick"))
#            message.privmsg("ban %s *!*@%s.%s GTFO, EAAD"%(chan.channel.name, member.name, Config.get("Services", "usermask"),), Config.get("Services", "nick"))
        session.delete(member)
        session.commit()
        message.reply("Removed user %s" % (member.name,))
        CUT.untrack_user(member.name)
