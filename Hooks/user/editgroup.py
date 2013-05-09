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
from Core.maps import Group
from Core.loadable import loadable, route, require_user

class editgroup(loadable):
    """Edit an existing user group."""
    usage = " <name> [newname] [\"<description>\"] [T/F - only admins can change]"
    access = 1 # Admin
    
    @route(r"(\S+)\s+([^\s\"']+)?(?:\s*[\"']([^\"']*)[\"'])?(?:\s+([TtFf]))?", access = "editgroup")
    @require_user
    def execute(self, message, user, params):
        
        name = params.group(1).lower()
        newname = params.group(2)
        if newname:
            newname = newname.lower()
        if newname in "tf":
            admin_only = newname
            newname = None
        desc = params.group(3)
        admin_only = params.group(4)

        g = Group.load(name)
        if not g:
            message.reply("There is no %s group." % (name))
            return

        if (not user.is_admin) and g.admin_only:
            message.reply("You don't have access to delete the %s group." % (name,))
            return

        if newname:
            if  Group.load(newname):
                message.reply("A%s %s group already exists." % ("n" if newname[0] in "aehiou" else "", newname))
                return
            else:
                g.name = newname

        if desc is not None:
            g.desc = desc

        if admin_only:
            if admin_only.lower() == "t":
                g.admin_only = True
            elif admin_only.lower() == "f":
                g.admin_only = False

        session.commit()
        message.reply("'%s' group updated." % (g.name))
