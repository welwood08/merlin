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
from Core.maps import Group, Access
from Core.loadable import loadable, route, require_user

class addgroup(loadable):
    """Add a new user group. Optionally copy initial command access from an existing group."""
    usage = " <name> \"<description>\" [T/F - only admins can change] [base]"
    access = 1 # Admin
    
    @route(r"(\S+)\s+[\"']([^\"']*)[\"'](?:\s+([TtFf]))?(?:\s+(\S+))?", access = "addgroup")
    @require_user
    def execute(self, message, user, params):
        
        name = params.group(1).lower()
        desc = params.group(2)
        admin_only = params.group(3) and params.group(3).lower() == "t"
        parent = params.group(4) and params.group(4).lower()

        g = Group.load(name)
        if g:
            message.reply("A%s %s group already exists." % ("n" if name[0] in "aehiou" else "", name))
            return
        if parent:
            p = Group.load(parent)
            if not p:
                message.reply("Group '%s' does not exist." % (parent))
                return
        g = Group(name=name, desc=desc, admin_only=admin_only)
        session.add(g)
        if parent:
            if p.id == 1:
                g.commands = session.query(Access).all()
            else:
                g.commands = p.commands.all()

        session.commit()
        message.reply("'%s' group created%s." % (g.name, " based on %s" % (p.name) if parent else ""))
