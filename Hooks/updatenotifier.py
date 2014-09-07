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
from Core.config import Config
from Core.exceptions_ import ChanParseError, PNickParseError

@system('PRIVMSG', robocop=True)
def updatenotifier(message):
    """Receive and parse update notifications"""
    m = message.get_msg()
    if m[0] == '@':
        try:
            if message.get_chan() == Config.get("Updates", "notify-channel") and message.get_pnick() in Config.get("Updates", "notify-allow").split():
                params = m[1:].split("/", 3)
                if params[0] in Config.get("Updates", "notify-repo").split():
                    mtags = params[1].split(",")
                    ctags = Config.get("Updates", "notify-branch").split()
                    selected = False
                    if "all" in mtags or "all" in ctags:
                        selected = True
                    else:
                        for tag in mtags:
                            if tag in ctags:
                                selected = True
                                break
                            if tag == "unstable":
                                mtags.extend(["acl", "master"])
                            elif tag == "stable":
                                mtags.extend(["acl-stable", "legacy-stable"])
                    if selected == True:
                        levels = Config.get("Updates", "notify-level").split()
                        if params[2] in levels or ("all" in levels and params[2] != "forks"):
                            nu = Config.get("Updates", "notify-users").split()
                            message.privmsg("UPDATE (%s): %s in %s: %s" % (message.get_pnick(), params[2], "/".join(params[:1]), params[3]), 
                                            ",".join(nu) if nu else Config.options("Admins")[0], priority=+5)
        except (ChanParseError, PNickParseError):
            pass
