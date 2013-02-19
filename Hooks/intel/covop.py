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
#
# Module by Martin Stone
 
from Core.maps import Planet, Updates
from Core.loadable import loadable, route, require_planet

class covop(loadable):
    """Calculates target alert, damage caused and liklihood of success of a covop based on stored scans."""
    usage = " <x:y:z> [agents] [stealth]"
    access = 3 # Member
    
    @route(loadable.planet_coord+r"(?:\s+(\d+))?(?:\s+(\d+))?")
    @require_planet
    def execute(self, message, user, params):
        
        planet = Planet.load(*params.group(1,3,5))
        if planet is None:
            message.alert("No planet with coords %s:%s:%s" % params.group(1,3,5))
            return

        tick=Updates.load().current_tick()

        pscan = planet.scan("P")
        if pscan is None:
            message.reply("No Planet Scans of %s:%s:%s found"%(planet.x,planet.y,planet.z))
            return
        else:
            p_age = tick - pscan.tick
            pscan = pscan.planetscan

        dscan = planet.scan("D")
        if dscan is None:
            message.reply("No Development Scans of %s:%s:%s found"%(planet.x,planet.y,planet.z))
            return
        else:
            d_age = tick - dscan.tick
            dscan = dscan.devscan

        gov_bonus = 0
        gov = "Unknown"
        if planet.intel.gov is not None:
            if planet.intel.gov[0].lower() == "c":
                gov = "Corporatism"
                gov_bonus = -0.05
            if planet.intel.gov[0].lower() == "d":
                gov = "Democracy"
                gov_bonus = -0.10
            if planet.intel.gov[0].lower() == "n":
                gov = "Nationalism"
                gov_bonus = 0.25
            if planet.intel.gov[0].lower() == "s":
                gov = "Socialism"
                gov_bonus = 0.00
            if planet.intel.gov[0].lower() == "t":
                gov = "Totalitarianism"
                gov_bonus = 0.10


        alert_min = int((50+5*min(pscan.guards/(planet.size+1),15))*(1+dscan.security_centre*2/dscan.total + (gov_bonus if gov != "Unknown" else -0.10) + 0.0))
        alert_max = int((50+5*min(pscan.guards/(planet.size+1),15))*(1+dscan.security_centre*2/dscan.total + (gov_bonus if gov != "Unknown" else +0.25) + 0.5))

        message.reply("Planet: %s:%s:%s  Government: %s  Alert: %s-%s  (Scan Age P:%s D:%s)" % (planet.x, planet.y, planet.z, gov, alert_min, alert_max, p_age, d_age))
        if params.group(6):
            agents = int(params.group(6))
            max_res = user.planet.resources_per_agent(planet)
            message.reply("Results:   SD: %1.1f%% (%dXP) NC: %d%% (%dXP) EF: %d roids (%dXP) S: %d ships (%dXP) SGP: %d guards (%dXP)" % (0.5*agents, self.xpcalc(agents,1),
                     agents, self.xpcalc(agents,2), agents/3, self.xpcalc(agents,3), agents, self.xpcalc(agents,4), 10*agents, self.xpcalc(agents,5)))
            message.reply("           IB: %d amps+dists (%dXP) RT: %dM %dC %dE (%dXP) H: %d buildings (%dXP)" % (agents/15, self.xpcalc(agents,6),
                     min(max_res, pscan.res_metal/10), min(max_res, pscan.res_crystal/10), min(max_res, pscan.res_eonium/10), self.xpcalc(agents,7), agents/20, self.xpcalc(agents,8)))

            if params.group(7):
                stealth = int(params.group(7))
                stealth = stealth - 5 - int(agents/2)
                t=19-alert_min
                prob = 100*(t+stealth)/(t+alert_max)
                if prob < 0:
                    prob = 0
                elif prob > 100:
                    prob = 100

                race = user.planet.race
                if race == "Ter":
                    growth = 6
                elif race == "Cat":
                    growth = 10
                elif race == "Xan":
                    growth = 4
                elif race == "Zik":
                    growth = 6
                elif race == "Etd":
                    growth = 6
                from math import ceil
                message.reply("New stealth: %s  Success rate: %s%%  Recovery time: %1.1f ticks" % (stealth, prob, ceil((5+int(agents/2))/growth)))
# base_max_stealth * (1 + gov_bonus / 100) + cumulative_success_bonus
# base_recovery*bonus_from_government (rounded down)

# (50+5*min(security_guards/(total_asteroids+1),15))*(1+(%security_centers*2 + %government alert bonus + %population security workers)/100)

# new_stealth = (old stealth - 5 - int(No_of_agents*0.5) )
# Note: "int()" means "take the integer part of", e.g. int(5.x) = 5
# (1-20)* + new_stealth - target_alertness must be higher than 1 for the operation to succeed.
# *chosen randomly

    def xpcalc(self, agents, num):
        return int(2*(num+agents/5))
