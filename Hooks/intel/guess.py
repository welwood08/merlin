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
 
from sqlalchemy.orm import aliased
from sqlalchemy.sql.functions import count, coalesce
from sqlalchemy.sql.expression import literal_column
from Core.db import session
from Core.maps import FleetScan, Planet, Alliance, Intel
from Core.loadable import loadable, route

class guess(loadable):
    """Use stored fleet data to suggest possible alliances for unknown planets."""
    usage = " [x.y.z] [limit]"
    access = 3

    @route(r"(\d+)?")
    def list_planets(self, message, user, params):
        oIntel = aliased(Intel)
        tIntel = aliased(Intel)
        
        # Find all planets with unknown alliance, who have been defended by planets (outside of their galaxy) with known alliance
        TQ = session.query(Planet.x, Planet.y, Planet.z, Alliance.name, count()).select_from(FleetScan).filter(FleetScan.in_galaxy==False, FleetScan.mission=="Defend")
        TQ = TQ.join(oIntel, FleetScan.owner_id == oIntel.planet_id).join(tIntel, FleetScan.target_id == tIntel.planet_id)
        TQ = TQ.filter(tIntel.alliance_id == None).filter(oIntel.alliance_id != None)
        TQ = TQ.join(Alliance, oIntel.alliance_id == Alliance.id).join(Planet, FleetScan.target_id == Planet.id)
        TQ = TQ.group_by(Planet.x, Planet.y, Planet.z, Alliance.name)

        # Find all planets with unknown alliance, who have defended planets (outside of their galaxy) with known alliance
        OQ = session.query(Planet.x, Planet.y, Planet.z, Alliance.name, count()).select_from(FleetScan).filter(FleetScan.in_galaxy==False, FleetScan.mission=="Defend")
        OQ = OQ.join(oIntel, FleetScan.owner_id == oIntel.planet_id).join(tIntel, FleetScan.target_id == tIntel.planet_id)
        OQ = OQ.filter(tIntel.alliance_id != None).filter(oIntel.alliance_id == None)
        OQ = OQ.join(Alliance, tIntel.alliance_id == Alliance.id).join(Planet, FleetScan.owner_id == Planet.id)
        OQ = OQ.group_by(Planet.x, Planet.y, Planet.z, Alliance.name)

        # A FULL OUTER JOIN would fit nicely here, but SQLAlchemy doesn't support it and I'm trying to stick with ORM, so we'll use Python

        # Combine the results into one sorted list
        results = sorted(TQ.all()+OQ.all())

        # Quit now if there are no results
        if len(results) == 0:
            message.reply("No suggestions found")
            return

        i = 0
        while i < (len(results)-1):
          # Check for planet/alliance combinations that appeared in both lists
          if results[i][:4] == results[i+1][:4]:
            r = list(results.pop(i))
            # Add the fleet counts (r[i+1] has moved to r[i])
            r[4] += results.pop(i)[4]
            results.insert(i, r)
          i+=1

        # Sort by number of fleets using a helper function
        from operator import itemgetter
        results.sort(key=itemgetter(4), reverse=True)

        # Reply to the user
        message.reply("Coords     Suggestion      Fleets")
        limit = int(params.group(1) or 5)
        for r in results[:limit]:
            message.reply("%-9s  %-14s  %s" % ("%s:%s:%s" % (r[0], r[1], r[2]), r[3], r[4]))
        if len(results) > limit:
            message.reply("%s results not shown (%s total)" % (len(results)-limit, len(results)))

    
    @route(loadable.coord+r"(?:\s+(\d+))?")
    def list_fleets(self, message, user, params):
        # Check the planet exists
        planet = Planet.load(*params.group(1,3,5))
        if planet is None:
            message.alert("No planet with coords %s:%s:%s" % params.group(1,3,5))
            return

        # Find all fleets with a known alliance who have defended this planet
        OQ = session.query(coalesce(FleetScan.launch_tick, FleetScan.landing_tick), literal_column("'From'").label("dir"), Planet.x, Planet.y, Planet.z, Alliance.name).select_from(FleetScan)
        OQ = OQ.filter(FleetScan.target_id == planet.id, FleetScan.in_galaxy==False, FleetScan.mission=="Defend")
        OQ = OQ.join(Intel, FleetScan.owner_id == Intel.planet_id).filter(Intel.alliance_id != None)
        OQ = OQ.join(Alliance, Intel.alliance_id == Alliance.id).join(Planet, FleetScan.owner_id == Planet.id)

        # Find all fleets with a known alliance who have been defended by this planet
        TQ = session.query(coalesce(FleetScan.launch_tick, FleetScan.landing_tick), literal_column("'To  '").label("dir"), Planet.x, Planet.y, Planet.z, Alliance.name).select_from(FleetScan)
        TQ = TQ.filter(FleetScan.owner_id == planet.id, FleetScan.in_galaxy==False, FleetScan.mission=="Defend")
        TQ = TQ.join(Intel, FleetScan.target_id == Intel.planet_id).filter(Intel.alliance_id != None)
        TQ = TQ.join(Alliance, Intel.alliance_id == Alliance.id).join(Planet, FleetScan.target_id == Planet.id)

        # Combine the results into one sorted list
        results = sorted(OQ.all()+TQ.all(), reverse=True)

        # Quit now if there are no results
        if len(results) == 0:
            message.reply("No suggestions found")
            return

        # Reply to the user
        message.reply("Tick  Dir   Planet     Alliance")
        limit = int(params.group(6) or 5)
        for r in results[:limit]:
            message.reply("%4s  %s  %-9s  %s" % (r[0], r[1], "%s:%s:%s" % (r[2], r[3], r[4]), r[5]))
        if len(results) > limit:
            message.reply("%s results not shown (%s total)" % (len(results)-limit, len(results)))
