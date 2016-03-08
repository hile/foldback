
Foldback nagios plugins
=======================

This module contains base implementations of two kinds of nagios plugin classes for python:

* foldback.nagios.plugin.NagiosPlugin

  Generic nagios plugin for any kind of command

* foldback.nagios.plugin.NagiosSNMPPlugin

  Nagios SNMP plugin, extending the base class

Included plugins
----------------

Installed to lib/foldback/plugins directory of your install prefix, a couple of ready to use
pluings are also available. In sources, see directory data/plugins for the implementations.

Default nagios configuration for these plugins is installed to share/foldback/commands.cfg to
be included in nagios.

Agents for net-snmp
-------------------

Some of the plugins use net-snmp pass_persist script agents. Required agent scripts are in
lib/foldback/agents directory with installed package and need to be added to snmpd.conf with
correct OID prefix to be used.

Example from a FreeBSD host:

```
pass_persist 1.3.6.1.4.1.2021.13.16 /usr/lib/foldback/agents/freebsd-temperatures
pass_persist 1.3.6.1.4.1.2021.13.17 /usr/lib/foldback/agents/freebsd-kernel
```

See the agent or plugin for expected prefixes to configure in snmpd.conf.

Examples
--------

Using the plugin base classes is described in two examples of the source code tree:

* examples/check-local

  describes using generic NagiosPlugin

* examples/check-snmp

  describes using the NagiosSNMPPlugin variant

Contact and copyright
=====================

This code was been slowly brewing by Ilkka Tuohela <hile@iki.fi> since 2008 in various modules.

The name *foldback* refers to [stage monitoring](https://en.wikipedia.org/wiki/Foldback_(sound_engineering)).

The code is licensed as open source with [Python Software Foundation License](https://en.wikipedia.org/wiki/Python_Software_Foundation_License)
