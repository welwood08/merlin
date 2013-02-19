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
from Core.maps import Updates, UserFleet
from Core.loadable import loadable, route, require_user

class aumydef(loadable):
    """Add your fleets for defense listing using an Advanced Unit scan for your planet. Send the link to the bot, then use this command."""
    usage = " [fleets] x [comment]"
    access = 3 # Member
    
    @route(r"(\d)\s*x\s*(.*)", access="aumydef")
    @require_user
    def execute(self, message, user, params):
        
        fleetcount = int(params.group(1))
        comment = params.group(2)
        reply = ""

        if user.planet:
            scan = user.planet.scan("A")
            if scan is None:
                message.reply("Advanced Unit Scan not found for %s:%s:%s" % (user.planet.x, user.planet.y, user.planet.z))
                return
        else:
            message.reply("Planet not set. Use !pref planet=x:y:z")
            return

        scanage = Updates.current_tick() - scan.tick
        if scanage > 12:
            reply += "Warning: Scan is %d ticks old.\n" % scanage

        self.update_comment_and_fleetcount(user, fleetcount, comment)
        user.fleets.delete()
        for uscan in scan.units:
            user.fleets.append(UserFleet(ship_id=uscan.ship_id, ship_count=uscan.amount))
        session.commit()

        ships = user.fleets.all()
        
        reply += "Updated your def info to: fleetcount %s, updated: pt%s ships: " % (user.fleetcount, user. fleetupdated)
        reply += ", ".join(map(lambda x:"%s %s" % (self.num2short(x.ship_count), x.ship.name), ships))
        reply += " and comment: %s" %(user.fleetcomment)
        message.reply(reply)
    
    def update_comment_and_fleetcount(self, user, fleetcount, comment):
        user.fleetcount = fleetcount
        if comment != "":
            if comment in self.nulls:
                comment = ""
            user.fleetcomment = comment
        user.fleetupdated = Updates.current_tick()

