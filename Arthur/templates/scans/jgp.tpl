{% from 'macros.tpl' import planetscanslink, alliancelink with context %}
<table cellspacing="1" cellpadding="3" width="700" class="black">
{% with planet = scan.planet %}
<tr class="datahigh">
    <th colspan="8">
    {% include "scans/header.tpl" %}
      </th>
</tr>
    
    <tr class="header">
        <th width="8%">Target</th>
        <th width="30%">Fleet</th>
        <th width="6%">Race</th>
        <th width="7%">Value</th>
        <th width="5%">ETA</th>
        <th width="15%">Alliance</th>
        <th class="right" width="20%">Ships <span class="red">(H)</span>/<span class="green">(F)</span></th>
        <th width="10%">Scans</th>
    </tr>
    
    <tr class="datahigh">
        <td class="center">{{ planet.x }}:{{ planet.y }}:{{ planet.z }}</td>
        <td> </td>
        <td> </td>
        <td> </td>
        <td> </td>
        <td> </td>
        <td class="right" colspan="2">
            <span class="red">{{ scan.total_hostile|intcomma }} ({{ scan.total_hostile_fleets }})</span>
            /
            <span class="green">{{ scan.total_friendly|intcomma }} ({{ scan.total_friendly_fleets }})</span>
        </td>
    </tr>
    
    {% for fleet in scan.fleets %}
    {% with owner = fleet.owner %}
    <tr class="{%if fleet.mission|lower=="defend" and fleet.in_galaxy%}galdef{%else%}{{ fleet.mission|lower }}{%endif%}">
        <td class="datahigh"></td>
        <td nowrap="nowrap">
            {% if fleet.mission|lower == "attack" %}-{% elif fleet.mission|lower == "defend" %}+{% elif fleet.mission|lower == "return"%}~{% endif %}
            {{ fleet.fleet_name }}
            (<a {{planetscanslink(owner)}}>{{ owner.x }}:{{ owner.y }}:{{ owner.z }}</a>)
        </td>
        <td class="{{ owner.race }} center"> {{ owner.race }} </td>
        <td class="right"> {{ ((owner.value or 0)/1000000.0)|round(1) }}M </td>
        <td class="center"> {{ fleet.eta }} </td>
        <td class="center"> {%if owner.intel%}{{ owner.intel.nick or "" }}{%if owner.intel.nick and owner.alliance%}<br>{%endif%}{%if owner.alliance%}
            <a {{alliancelink(owner.alliance.name)}}>{{ owner.alliance.name }}</a>{%endif%}{%endif%} </td>
        <td class="right"> {{ fleet.fleet_size|intcomma }}</td>
        <td class="center datahigh">
        {% if owner.scan("A") %}
             {% set scanage = update.id - owner.scan("A").tick %}
                 <a href="#{{ owner.scan("A").link|url }}" class="scan_age_{% if scanage > 12 %}ancient{% elif scanage > 5 %}older{% elif scanage > 0 %}old{% else %}new{% endif %}">{{ owner.scan("A").scantype }}</a>
        {% elif owner.scan("U") %}
             {% set scanage = update.id - owner.scan("U").tick %}
                 <a href="#{{ owner.scan("U").link|url }}" class="scan_age_{% if scanage > 12 %}ancient{% elif scanage > 5 %}older{% elif scanage > 0 %}old{% else %}new{% endif %}">{{ owner.scan("U").scantype }}</a>
        {% endif %}
        {% if owner.scan("N") %}
             {% set scanage = update.id - owner.scan("N").tick %}
                 <a href="#{{ owner.scan("N").link|url }}" class="scan_age_{% if scanage > 12 %}ancient{% elif scanage > 5 %}older{% elif scanage > 0 %}old{% else %}new{% endif %}">{{ owner.scan("N").scantype }}</a>
        {% endif %}
        </td>
    </tr>
    {% endwith %}
    {% endfor %}
    
    
    
    <tr class="header">
        <th colspan="8">Overview for each ETA with incoming</th>
    </tr>
    <tr class="datahigh">
        <th> </th>
        <th> Combat Tick </th>
        <th> </th>
        <th colspan="2"> ETA </th>
        <th> </th>
        <th class="right" colspan="2">
        Ships <span class="red">(H)</span>/<span class="green">(F)</span>
        </th>
    </tr>
    
    {% for lt in scan.fleet_overview() %}
    <tr class="{{ loop.cycle('odd', 'even') }} center">
        <td> </td>
        <td> Tick: {{ lt[0] }} </td>
        <td> </td>
        <td colspan="2"> {{ lt[1] }} </td>
        <td> </td>
        <td class="right" colspan="2">
            <span class="red"> {{ lt[3] }} ({{ lt[2] }}) </span>
            /
            <span class="green"> {{ lt[5] }} ({{ lt[4] }}) </span>
        </td>
    </tr>
    {% endfor %}
    
{% endwith %}
</table>
