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
 
from sqlalchemy.sql import desc
from Core.db import session
from Core.maps import User, Intel
from Core.loadable import loadable, route, require_user

class amps(loadable):
    """Show the amp counts of the top 10 alliance scanners. Optionally filter by amps or name."""
    usage = " [pnick|amps]"
    access = 2 # Member
    
    @route(r"(.*)", access="amps")
    def execute(self, message, user, params):
        if params.group(1):
            u = User.load(params.group(1))
            if u:
                message.reply("%s has %s amps." % (u.name, u.planet.intel.amps))
                return
            else:
                if not params.group(1).isdigit():
                    message.reply("No users matching '%s'" % (params.group(1)))
                    return

        Q = session.query(User, Intel)
        Q = Q.join(Intel, User.planet_id == Intel.planet_id)
        if params.group(1):
            Q = Q.filter(Intel.amps >= int(params.group(1)))
        else:
            Q = Q.filter(Intel.amps > 0)
        Q = Q.order_by(desc(Intel.amps))
        Q = Q.limit(10)
        if Q.count() == 0:
            message.reply("No scanners found with at least %s amps." % (params.group(1) if params.group(1) else "1"))
            return
        reply = "Scanners%s:  " % ((" with at least %s amps" % (params.group(1))) if params.group(1) else "")
        for scanner in Q:
            reply += "%s: %s  " % (scanner[0].name, scanner[1].amps)
        message.reply(reply[:-2])
        return

class myamps(loadable):
    """Update your amp count."""
    usage = " [amps]"
    access = 3 # Member

    @route(r"(\d+)?", access="myamps")
    @require_user
    def execute(self, message, user, params):
        if params.group(1):
            user.planet.intel.amps = int(params.group(1))
            session.commit()
            message.reply("Updated your amp count to %s." % (params.group(1)))
        else:
            try:
                message.reply("You have %s amps." % (user.planet.intel.amps))
                return
            except:
                message.reply("You have no amps information. Make sure your planet is set in !pref." % (user.planet.intel.amps))
                return
