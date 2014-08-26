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
 
from Core.loadable import system
from Core.exceptions_ import PNickParseError

@system('PRIVMSG', robocop=True)
def ctcp(message):
    """Respond to CTCP queries (from admins)"""
    m = message.get_msg()
    if m[0] == '\001':
        from Core.config import Config
        try:
            if message.get_pnick() in Config.options("Admins"):
                if m[1:5] == 'PING':
                    message.write("NOTICE %s :\001PING %s\001" % (message.get_nick(), m[6:]))
                elif m[1:8] == 'VERSION':
                    import subprocess
                    try:
                        version = subprocess.check_output(["git", "describe", "HEAD"]).strip()
                        version += "/" + "/".join(subprocess.check_output(["git", "describe", "origin/acl", "origin/master"]).split())
                    except:
                        pass
                    message.write("NOTICE %s :\001VERSION %s\001" % (message.get_nick(), "Merlin (%s)" % version))
        except PNickParseError:
            pass
