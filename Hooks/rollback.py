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
 
# This module provides an entry point for system reboots or reloads

# Module by Martin Stone

from Core.loadable import system
from Core.maps import Updates
from sqlalchemy.sql import text
from Core.db import session

@system('PRIVMSG', admin=True, robocop=True)
def rollback(message):
    """Rollback to a given tick. Tick must be repeated for confirmation."""
    
    msg = message.get_msg().split()[1:]
    if len(msg) != 2:
        message.reply("rollback <tick> <tick>")
        return
    if msg[0] != msg[1]:
        message.reply("Ticks must match!")
        return
    if not msg[0].isdigit():
        message.reply("Ticks should be numeric.")
        return
    if int(msg[0]) > Updates.current_tick():
        message.reply("Timetravel module not installed. Cannot rollback to a future tick.")
        return

    session.execute(text("DELETE FROM updates WHERE id > %s;" % (msg[0])))
    session.execute(text("DELETE FROM planet_exiles WHERE tick > %s;" % (msg[0])))
    session.execute(text("DELETE FROM planet_idles WHERE tick > %s;" % (msg[0])))
    session.execute(text("DELETE FROM planet_value_drops WHERE tick > %s;" % (msg[0])))
    session.execute(text("DELETE FROM planet_landings WHERE tick > %s;" % (msg[0])))
    session.execute(text("DELETE FROM planet_landed_on WHERE tick > %s;" % (msg[0])))
    session.execute(text("DELETE from galaxy_history where tick > %s;" % (msg[0])))
    session.execute(text("DELETE from planet_history where tick > %s;" % (msg[0])))
    session.execute(text("DELETE from alliance_history where tick > %s;" % (msg[0])))
    session.execute(text("DELETE from cluster_history where tick > %s;" % (msg[0])))

    session.commit()
    message.reply("Rollback complete. Bot will update at next tick.")
