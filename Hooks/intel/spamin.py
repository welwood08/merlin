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
 
import re
from Core.db import session
from Core.maps import Planet, Alliance, Intel
from Core.loadable import loadable, route


class spamin(loadable):
    """Update intel on many planets at once. Accepts !spam format."""
    usage = " <alliance> [x.y.z]+"
    planet_coordre = re.compile(loadable.planet_coord)

    @route(r"(\S+)\s(.+)", access = "member")
    def execute(self, message, user, params):
        alliance = Alliance.load(params.group(1))
        if (alliance is None) and (params.group(1).lower() not in ["None", "<>", "?"]):
            message.alert("No alliances match %s" % (params.group(1)))
            return

        reply = "Planets added to '%s':" % (alliance.name if alliance else "None")

        planets = self.planet_coordre.findall(params.group(2))
        for coord in planets:
            planet=Planet.load(coord[0],coord[2],coord[4])
            if planet:
                if planet.intel is None:
                    planet.intel = Intel()
                planet.intel.alliance=alliance
                reply += " %s:%s:%s" % (coord[0],coord[2],coord[4])

        session.commit()
        message.reply(reply)

