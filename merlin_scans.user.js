// ==UserScript==
// @name           Merlin Scan Script for YOUR_ALLIANCE
// @version        2.0.0
// @namespace      https://github.com/d7415/merlin
// @description    Submit scan URLs to Arthur.
// @grant          unsafeWindow

// @exclude        *://*/login*
// @exclude        *://*/signup*
// @exclude        *://*/register*
// @exclude        *://*/preferences*
// @exclude        *://*/support*
// @exclude        *://*/manual*
// @exclude        *://*/chat*
// @exclude        *://*/forum*
// @exclude        *://*/botfiles*
// @exclude        *://beta.planetarion.com/*
// @exclude        *://speedgame.planetarion.com/*
// @exclude        *://pirate.planetarion.com/*
// @exclude        *://ninja.planetarion.com/*
// @exclude        *://forum.planetarion.com/*
// @exclude        *://www.planetarion.com/*

// @include        /^https?://146\.185\.135\.215/(waves|showscan).pl\?/
// @include        /^https?://(pa|game)\.ranultech\.co\.uk/(waves|showscan).pl\?/
// @include        /^https?://[^/]*\.planetarion\.com/(waves|showscan).pl\?/
// @copyright      2008-2012 William Elwood (Will) / 2012 Dizkarte / 2013-2015 Martin Stone (Pit)
// @license        GNU General Public License version 3; http://www.gnu.org/licenses/gpl.html
// ==/UserScript==

(function(window, doc) {
    var script = doc.createElement('script');
    script.setAttribute('src', 'http://ARTHUR_DOMAIN_HERE/lookup/?nick=' + unsafeWindow.PA_planet.nick + '&lookup=' + window.location);
    doc.body.appendChild(script);
})(this, this.document);
