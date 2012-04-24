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
 
from sqlalchemy.orm import aliased
from sqlalchemy.sql import desc
from sqlalchemy.sql.functions import count
from Core.db import session
from Core.maps import Updates, Galaxy, Planet, Alliance, User, Intel
from Core.loadable import loadable, route
from Core.config import Config
from Core.paconf import PA

class top10(loadable):
    """Top planets in a given alliance"""
    usage = " [alliance]"
    access = "member"
    
    @route(r"(\S+)")
    def user_alliance(self, message, user, params):
        alliance = Alliance.load(params.group(1))
        if alliance is None:
            message.reply("No alliance or user matching '%s' found" % (params.group(1),))
        else:
            self.execute(message, alliance=alliance)
    
    @route(r"")
    def me(self, message, user, params):
        self.execute(message)
    
    def execute(self, message, alliance=None):
        tick = Updates.current_tick()
        target = aliased(Planet)
        target_intel = aliased(Intel)
        planet = aliased(Planet)
        planet_intel = aliased(Intel)
        
        Q = session.query(planet.x, planet.y, planet.z, planet.score, planet.value, planet.size, planet.xp, planet.race, planet_intel.nick)
        if alliance:
            Q = Q.join((planet.intel, planet_intel))
            Q = Q.filter(planet_intel.alliance == alliance)
        Q = Q.group_by(planet.x, planet.y, planet.z)
        Q = Q.order_by(desc(planet.score))
        result = Q.all()
        
        reply = "Top planets"
        if alliance:
            reply+="in %s"%(alliance.name,)
        reply+=":\n"
        prev = []
        i=0
        for x, y, z, score, value, size, xp, race, nick in result[:10]:
            i+=1
            prev.append("#%s - %s (%s %s:%s:%s) - Score: %s Value: %s Size: %s XP: %s"%(i,nick,race,x,y,z,score,value,size,xp))
        message.reply(reply+"\n".join(prev))
