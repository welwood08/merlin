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

from Core.maps import Group
from Core.loadable import loadable, route, require_user

class show(loadable):
    """Show commands granted to a given group."""
    usage = " <access groups>"
    access = 1 # Admin
    
    @route(r"(\S+)", access = "show")
    @require_user
    def execute(self, message, user, params):
        
        groups = params.group(1).lower().split(",")

        for group in groups:
            g = Group.load(group)
            if not g:
                message.reply("Invalid access group '%s'" % (group,))
                continue
            reply = "%s has access to: " % (g.name)
            if g.id == 1:
                reply += "Everything (idiot)  "
            else:
                for command in g.commands.all():
                    reply += "%s, " % (command.name)
            message.reply(reply[:-2])
