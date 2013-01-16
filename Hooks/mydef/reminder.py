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
from Core import Merlin
from Core.exceptions_ import PNickParseError
from Core.config import Config
from Core.chanusertracker import CUT
from Core.loadable import system
from Core.maps import User, Updates

@system('JOIN')
def join(message):
    # Someone is joining a channel
    if message.get_nick() != Merlin.nick:
        # Someone is joining a channel we're in
        try:
            u = User.load(name=message.get_pnick())
            if u is None:
                return
            defage = Updates.current_tick() - (u.fleetupdated or 0)
            if defage > (Config.getint("Misc", "defage") if Config.has_option("Misc", "defage") else 25):
                message.notice("Your mydef is %d ticks old. Update it now!" % (defage), message.get_nick())
        except PNickParseError:
            return
