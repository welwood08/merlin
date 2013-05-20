##Merlin Command Reference


<table>
<tr><td> Command </td><td> Usage </td><td> Description </td></tr>
<tr><td> debug </td><td>  </td><td> Execute a statement. Warning: Playing with this is risky! </td></tr>
<tr><td> quit </td><td>  </td><td> Quit IRC and close down </td></tr>
<tr><td> raw </td><td>  </td><td> Send a raw message to the server. </td></tr>
<tr><td> reboot </td><td>  </td><td> Quit IRC reboot, reload and reconnect </td></tr>
<tr><td> reload </td><td>  </td><td> Dynamically reload the Core and Hooks </td></tr>
<tr><td> auth </td><td>  </td><td> Authenticates the user, if they provide their username and password </td></tr>
<tr><td> letmein </td><td>  </td><td> Invites the user to the private channel, if they provide their username and password </td></tr>
<tr><td> secure </td><td>  </td><td> Secures the PNick of the bot. </td></tr>
<tr><td> commandlog </td><td> commandlog <command> [user=<username>] <parameters> | <id> </td><td> Search the bot's command log for use of specified command. Parameters is a % encapsulated list of arguments. For example, to search for someone setting the alliance on a planet in 1:1, do: !commandlog intel %1%1%alliance=%. You can also limit the search to a specific username using the optional user= argument. </td></tr>
<tr><td> help </td><td> help [command] </td><td> Help </td></tr>
<tr><td> adduser </td><td> adduser <pnick> <access> </td><td> Used to add new users with the specified pnick and access level </td></tr>
<tr><td> galmate </td><td> galmate <pnick> </td><td> Add a user with galmate access </td></tr>
<tr><td> edituser </td><td> edituser <user> (<access>|true|false) </td><td> Used to change a user's access or (de)activate them </td></tr>
<tr><td> getanewdaddy </td><td> getanewdaddy <pnick> </td><td> Remove sponsorship of a member. Their access will be reduced to "galmate" level. Anyone is free to sponsor the person back under the usual conditions. This isn't a kick and it's not final. </td></tr>
<tr><td> remuser </td><td> remuser <user> </td><td> Permenantly delete a user </td></tr>
<tr><td> whois </td><td> whois <pnick> </td><td> Lookup a user's details </td></tr>
<tr><td> aids </td><td> aids <pnick> </td><td> See who a user has sexed </td></tr>
<tr><td> pref </td><td> pref [planet=x.y.z] [password=pass] [url=ip] [phone=999] [pubphone=T|F] [smsmode=clickatell|google|both] [email=user@example.com] </td><td> Set your planet, password for the webby, URL preference and phone number and settings; order doesn't matter </td></tr>
<tr><td> phone </td><td> phone <list|allow|deny|show> [pnick] </td><td> Lookup someone's phone number or set permissions for who can view your number if you've not set public (pref) </td></tr>
<tr><td> quitter </td><td> quitter <pnick> </td><td>  </td></tr>
<tr><td> quits </td><td> quits <pnick> </td><td>  </td></tr>
<tr><td> addchan </td><td> addchan <chan> <level> </td><td> Adds a channel with the given level with maxlevel equal to your own access level </td></tr>
<tr><td> galchan </td><td> galchan <chan> </td><td> Adds a channel where the access of commands is limited to 1 in that channel (so you don't accidentally do !intel or something 'important') </td></tr>
<tr><td> remchan </td><td> remchan <chan> </td><td>  </td></tr>
<tr><td> alias </td><td> alias <alias> (at most 15 characters) </td><td> Set an alias that maps to your pnick, useful if you have a different nick than your pnick and people use autocomplete. </td></tr>
<tr><td> forcepref </td><td> forcepref <user> [planet=x.y.z] [password=pass] [url=ip] [phone=999] [pubphone=T|F] [smsmode=clickatell|google|both] </td><td> Set a user's planet, password for the webby, URL preference and phone number and settings; order doesn't matter </td></tr>
<tr><td> members </td><td> members [coords] [defage] [mydef] [galmates] </td><td> List all members, in format nick (alias). Optionally include coordinates, mydef age, tick of last mydef update. </td></tr>
<tr><td> paranoidcunts </td><td> paranoidcunts [galmates] [check] [noemail] </td><td> List members who are have not set their phone number properly. Optionally sanity-checks phone numbers. </td></tr>
<tr><td> tell </td><td> tell <nick> <message> </td><td> Sends a message to a user when they next join a channel with me. </td></tr>
<tr><td> prop </td><td> prop [<invite|kick> <pnick> <comment>] | [list] | [vote <number> <yes|no|abstain>] | [expire <number>] | [show <number>] | [cancel <number>] | [recent] | [search <pnick>] | [suggest <decision to be made>] </td><td> A proposition is a vote to do something. For now, you can raise propositions to invite or kick someone. Once raised the proposition will stand until you expire it.  Make sure you give everyone time to have their say. Votes for and against a proposition are weighted by carebears. You must have at least 1 carebear to vote. </td></tr>
<tr><td> adopt </td><td> adopt <pnick> </td><td> Adopt an orphan </td></tr>
<tr><td> orphans </td><td>  </td><td> Lists all members whose sponsors are no longer members. Use !adopt to someone. </td></tr>
<tr><td> cookie </td><td> cookie [howmany] <receiver> <reason> | [stat] </td><td> Cookies are used to give out carebears. Carebears are rewards for carefaces. Give cookies to people when you think they've done something beneficial for you or for the alliance in general. </td></tr>
<tr><td> gac </td><td>  </td><td> Displays stats about the Gross Alliance Cookies. Similar to the Gross Domestic Product, GAC covers how many cookies changed hands in a given week. </td></tr>
<tr><td> yourmum </td><td> yourmum [pnick] </td><td>  </td></tr>
<tr><td> sms </td><td> sms <nick> <message> </td><td> Sends an SMS to the specified user. Your username will be appended to the end of each sms. The user must have their phone correctly added and you must have access to their number. </td></tr>
<tr><td> smslog </td><td> smslog [id] </td><td> Show the last ten SMS sent, or the text of a specific SMS sender. </td></tr>
<tr><td> showmethemoney </td><td>  </td><td>  </td></tr>
<tr><td> email </td><td> email <nick> <message> </td><td> Sends an email to the specified user. Your username will be included automatically. </td></tr>
<tr><td> fuckthatname </td><td> fuckthatname <fucked tag> usethis <better name> </td><td>  </td></tr>
<tr><td> lookup </td><td> lookup [x:y[:z]|alliance|user] </td><td>  </td></tr>
<tr><td> details </td><td> details <x.y.z> </td><td> This command basically collates lookup, xp, intel and status into one simple to use command. Neat, huh? </td></tr>
<tr><td> intel </td><td> intel <x.y[.z]> [option=value]+ </td><td> View or set intel for a planet. Valid options: alliance, nick, fakenick, defwhore, covop, amps, dists, bg, gov, relay, reportchan, comment </td></tr>
<tr><td> search </td><td> search <alliance|nick> </td><td> Search for a planet by alliance or nick. </td></tr>
<tr><td> supersearch </td><td> supersearch[option=value]+ [comment=key words] </td><td> Advanced planet/intel search: alliance, nick, reportchan, amps, dists, size, value, race, comment </td></tr>
<tr><td> bumchums </td><td> bumchums <alliance> [alliance] [number] </td><td> Pies </td></tr>
<tr><td> info </td><td> info <alliance> </td><td> Alliance information (All information taken from intel, for tag information use the lookup command) </td></tr>
<tr><td> spam </td><td> spam <alliance> </td><td> Spam alliance coords </td></tr>
<tr><td> racism </td><td> racism <alliance> | <x:y> </td><td> Shows averages for each race matching a given alliance in intel or for a galaxy. </td></tr>
<tr><td> covop </td><td> covop <x:y:z> [agents] [stealth] </td><td> Calculates target alert, damage caused and liklihood of success of a covop based on stored scans. </td></tr>
<tr><td> spamin </td><td> spamin <alliance> [x.y.z]+ </td><td> Update intel on many planets at once. Accepts !spam format. </td></tr>
<tr><td> epenis </td><td> epenis [user] </td><td> Penis </td></tr>
<tr><td> galpenis </td><td> galpenis <x:y> </td><td> Cock </td></tr>
<tr><td> apenis </td><td> apenis [alliance] </td><td> Schlong </td></tr>
<tr><td> bigdicks </td><td>  </td><td> BEEFCAKE!!!11onetwo </td></tr>
<tr><td> loosecunts </td><td>  </td><td>  </td></tr>
<tr><td> value </td><td> value <x:y:z> </td><td> Value of a planet over the last 15 ticks </td></tr>
<tr><td> exp </td><td> exp <x:y:z> </td><td> XP of a planet over the last 15 ticks </td></tr>
<tr><td> newb </td><td>  </td><td>  </td></tr>
<tr><td> bitches </td><td> bitches [minimum eta] </td><td> List of booked targets by galaxy and alliance </td></tr>
<tr><td> status </td><td> status [x:y[:z]|user|alliance] [tick] </td><td> List of targets booked by user, or list of bookings for a given galaxy or planet </td></tr>
<tr><td> book </td><td> book <x:y:z> (eta|landing tick) [later] </td><td> Book a target for attack. You should always book your targets, so someone doesn't inadvertedly piggy your attack. </td></tr>
<tr><td> unbook </td><td> unbook <x:y:z> [eta|landing tick] </td><td>  </td></tr>
<tr><td> gangbang </td><td> gangbang <alliance> [tick] </td><td> List of booked targets in an alliance </td></tr>
<tr><td> attack </td><td> attack [<eta|landingtick> [<#waves>w] <coordlist> [comment]] | [list] | [show <id>] </td><td> Create an attack page on the webby with automatic parsed scans </td></tr>
<tr><td> editattack </td><td> editattack [<id> add|remove <coordlist>] | [<id> land <tick|eta>] | [<id> comment <comment>] [<id> waves <waves>] </td><td>  </td></tr>
<tr><td> mydef </td><td> mydef [fleets] x <[ship count] [ship name]> [comment] </td><td> Add your fleets for defense listing. For example: 2x 20k Barghest 30k Harpy Call me any time for hot shipsex. </td></tr>
<tr><td> showdef </td><td> showdef <pnick> </td><td>  </td></tr>
<tr><td> searchdef </td><td> searchdef [number] <ship> </td><td>  </td></tr>
<tr><td> usedef </td><td> usedef <pnick> [num] <ship> </td><td>  </td></tr>
<tr><td> logdef </td><td> logdef [ship] | [user] </td><td>  </td></tr>
<tr><td> finddef </td><td> finddef [<class>] <target class> [t1|t2|t3] </td><td> Search mydef for ships by target class and, optionally, ship class or target level. </td></tr>
<tr><td> theirdef </td><td> theirdef [user] [fleets] x <[ship count] [ship name]> [comment] </td><td> Update another user's fleets for defense listing. For example: 2x 20k Barghest 30k Harpy Call me any time for hot shipsex. </td></tr>
<tr><td> defcall </td><td> defcall <x:y:z> <eta> <description> </td><td> Make a broadcast to the channel requesting defence </td></tr>
<tr><td> aumydef </td><td> aumydef [fleets] x [comment] </td><td> Add your fleets for defense listing using an Advanced Unit scan for your planet. Send the link to the bot, then use this command. </td></tr>
<tr><td> victim </td><td> victim [alliance] [race] [<|>][size] [<|>][value] [bash] (must include at least one search criteria, order doesn't matter) </td><td> Target search, ordered by maxcap </td></tr>
<tr><td> idler </td><td> idler [alliance] [race] [<|>][size] [<|>][value] [bash] (must include at least one search criteria, order doesn't matter) </td><td> Target search, ordered by idle ticks </td></tr>
<tr><td> whore </td><td> whore [alliance] [race] [<|>][size] [<|>][value] [bash] (must include at least one search criteria, order doesn't matter) </td><td> Target search, ordered by xp gain </td></tr>
<tr><td> cunts </td><td> cunts [alliance] [race] [<|>][size] [<|>][value] [bash] (must include at least one search criteria, order doesn't matter) </td><td> Target search, based on planets currently attacking our alliance, ordered by size </td></tr>
<tr><td> topcunts </td><td> topcunts [x:y[:z]|alliance|user] </td><td> Top planets attacking the specified target </td></tr>
<tr><td> surprisesex </td><td> surprisesex [x:y[:z]|alliance|user] </td><td> Top alliances attacking the specified target </td></tr>
<tr><td> top10 </td><td> top10 [alliance] [race] [score|value|size|xp] </td><td> Top planets by specified criteria </td></tr>
<tr><td> top10lookup </td><td> top10lookup [alliance] [race] [score|value|size|xp] </td><td> Top planets by specified criteria. Results in !lookup format. </td></tr>
<tr><td> last10 </td><td> last10 [alliance] [race] [score|value|size|xp] </td><td> Bottom planets by specified criteria </td></tr>
<tr><td> last5 </td><td> last5 [alliance] [race] [score|value|size|xp] </td><td> Bottom planets by specified criteria </td></tr>
<tr><td> exile </td><td>  </td><td>  </td></tr>
<tr><td> launch </td><td> launch <class|eta> <land_tick> </td><td> Calculate launch tick, launch time, prelaunch tick and prelaunch modifier for a given ship class or eta, and land tick. </td></tr>
<tr><td> roidcost </td><td> roidcost <roids> <value_cost> [mining_bonus] </td><td> Calculate how long it will take to repay a value loss capping roids. </td></tr>
<tr><td> roidsave </td><td> roidsave <roids> <ticks> [mining_bonus] </td><td> Tells you how much value will be mined by a number of roids in that many ticks. </td></tr>
<tr><td> bashee </td><td> bashee <x:y:z> </td><td>  </td></tr>
<tr><td> basher </td><td> basher <x:y:z> </td><td>  </td></tr>
<tr><td> maxcap </td><td> maxcap (<total roids>|<x:y:z> [a:b:c]) </td><td>  </td></tr>
<tr><td> xp </td><td> xp <x:y:z> [a:b:c] </td><td>  </td></tr>
<tr><td> seagal </td><td> seagal <x:y:z> [sum] </td><td>  </td></tr>
<tr><td> tick </td><td>  </td><td>  </td></tr>
<tr><td> au </td><td> au (<x:y:z> [old] [link] | <id>) </td><td>  </td></tr>
<tr><td> dev </td><td> dev (<x:y:z> [old] [link] | <id>) </td><td>  </td></tr>
<tr><td> jgp </td><td> jgp (<x:y:z> [old] [link] | <id>) </td><td>  </td></tr>
<tr><td> news </td><td> news (<x:y:z> [old] [link] | <id>) </td><td>  </td></tr>
<tr><td> planet </td><td> planet (<x:y:z> [old] [link] | <id>) </td><td>  </td></tr>
<tr><td> unit </td><td> unit (<x:y:z> [old] [link] | <id>) </td><td>  </td></tr>
<tr><td> scans </td><td> scans <x:y:z> </td><td>  </td></tr>
<tr><td> request </td><td> request <x.y.z> <scantype(s)> [dists] | <id> blocks <amps> | cancel <id> | list | links </td><td> Request a scan </td></tr>
<tr><td> catcher </td><td>  </td><td>  </td></tr>
<tr><td> toprequesters </td><td> toprequesters <age> <number> </td><td> List top scan requesters in the last x ticks. </td></tr>
<tr><td> topscanners </td><td> topscanners <age> <number> [all] </td><td> List top scanners in the last x ticks. Shows requested scans by default. Use the "all" option to show all parsed scans. </td></tr>
<tr><td> amps </td><td> amps [pnick|amps] </td><td> Show the amp counts of the top 10 alliance scanners. Optionally filter by amps or name. </td></tr>
<tr><td> myamps </td><td> myamps [amps] </td><td> Update your amp count. </td></tr>
<tr><td> ship </td><td> ship <ship> </td><td> Returns the stats of the specified ship </td></tr>
<tr><td> cost </td><td> cost <number> <ship> </td><td> Calculates the cost of producing the specified number of ships </td></tr>
<tr><td> eff </td><td> eff <number> <ship> [t1|t2|t3] </td><td> Calculates the efficiency of the specified number of ships </td></tr>
<tr><td> stop </td><td> stop <number> <ship> [t1|t2|t3] </td><td> Calculates the required defence to the specified number of ships </td></tr>
<tr><td> prod </td><td> prod <number> <ship> <factories> [population] [government] </td><td> Calculate ticks it takes to produce <number> <ships> with <factories>. Specify population and/or government for bonuses. </td></tr>
<tr><td> rprod </td><td> rprod <ship> <ticks> <factories> [population] [government] </td><td> Calculate how many <ship> you can build in <ticks> with <factories>. Specify population and/or government for bonuses. </td></tr>
<tr><td> afford </td><td> afford <x:y:z> <ship> </td><td> Calculates the number of a certain ship the planet can produce based on the most recent planet scan </td></tr>
<tr><td> addslogan </td><td> addslogan <slogan goes here> </td><td>  </td></tr>
<tr><td> slogan </td><td>  </td><td>  </td></tr>
<tr><td> remslogan </td><td> remslogan <slogan to remove> </td><td>  </td></tr>
<tr><td> addquote </td><td> addquote <quote goes here> </td><td>  </td></tr>
<tr><td> quote </td><td>  </td><td>  </td></tr>
<tr><td> remquote </td><td> remquote <quote to remove> </td><td>  </td></tr>
<tr><td> links </td><td>  </td><td>  </td></tr>
<tr><td> catcher </td><td>  </td><td>  </td></tr>
<tr><td> broadcast </td><td> broadcast <message> [HIDEME] </td><td> Make a broadcast to all alliance channels. Append "HIDEME" if you do not want your username included. </td></tr>
</table>
