"""
Nagios plugin implementation for base command and SNMP based commands
"""

import sys

from seine.snmp.client import SNMPClient, SNMPv1Auth, SNMPv2cAuth, SNMPv3Auth, SNMPError
from systematic.shell import Script, ScriptError


NAGIOS_STATE_OK = 'OK'
NAGIOS_STATE_WARNING = 'WARNING'
NAGIOS_STATE_CRITICAL = 'CRITICAL'
NAGIOS_STATE_UNKNOWN = 'UNKNOWN'

NAGIOS_STATES = {
    0: NAGIOS_STATE_OK,
    1: NAGIOS_STATE_WARNING,
    2: NAGIOS_STATE_CRITICAL,
    3: NAGIOS_STATE_UNKNOWN,
}
NAGIOS_INITIAL_STATE = 3

class NagiosPluginError(Exception):
    pass

class NagiosPlugin(object):
    """Nagios plugin base class

    Implementation of nagios plugin in python

    See examples directory in source code for usage
    """
    def __init__(self, description=None):
        object.__setattr__(self, 'state_code', NAGIOS_INITIAL_STATE)
        self.message = 'UNINITIALIZED'
        self.parser = Script(description=description)

    def __repr__(self):
        return '{0:d} {1}'.format(self.state_message, self.message)

    def __setattr__(self, attr, value):
        if attr == 'state':
            self.set_state(value)
        object.__setattr__(self, attr, value)

    @property
    def state_message(self):
        return NAGIOS_STATES[self.state_code]

    def set_state(self, value):
        """Set nagios plugin state

        Sets internal state to provided value, which can be integer from 0 to 3
        or one of strings 'OK', 'WARNING', 'CRITICAL', 'UNKNOWN'

        Silently refuses to lower plugin state to less critical error. UNKNOWN
        state can always be overwritten.
        """
        try:
            value = int(value)
            if value not in NAGIOS_STATES.keys():
                raise ValueError
        except ValueError:
            pass

        if value in NAGIOS_STATES.keys():
            state_code = int(value)
        else:
            for k,v in NAGIOS_STATES.items():
                if value == v:
                    state_code = k
                    break

        if state_code not in NAGIOS_STATES.keys():
            raise AttributeError('Attempt to set invalid plugin state {0}'.format(value))

        # Silently ignore lowering of error state for a plugin
        if self.state_code != NAGIOS_INITIAL_STATE and self.state_code > state_code:
            self.parser.log.debug('Refuse lowering state from {0} to {1}'.format(self.state_code, state_code))
            return

        object.__setattr__(self, 'state_code', state_code)

    def add_argument(self, *args, **kwargs):
        """Add CLI argument

        Add CLI argument. Uses argparse.ArgumentParser.add_argument syntax

        """
        self.parser.add_argument(*args, **kwargs)

    def parse_args(self, *args, **kwargs):
        """Parse arguments

        Parse self.parser arguments. Called automatically from self.run()

        """
        self.args = self.parser.parse_args(*args, **kwargs)
        return self.args

    def error(self, message, code=2):
        """Exit with error

        Exit with error code (must be valid nagios state code)

        Writes error message to stdout

        """
        try:
            code = int(code)
            if code not in NAGIOS_STATES.keys():
                raise ValueError
        except ValueError:
            raise AttributeError('Invalid error code {0}'.format(code))

        sys.stdout.write('Error running plugin: {0}\n'.format(message))
        sys.exit(code)

    def exit(self):
        """Return nagios message and exit

        Print self.state_message + self.message to stdout for nagios and
        exit with self.state_code code

        """
        sys.stdout.write('{0} {1}\n'.format(self.state_message, self.message))
        sys.exit(self.state_code)

    def run(self):
        """Run the plugin

        Run the plugin:
          - Parse arguments
          - Set message to empty
          - run self.check_plugin_status() callback
          - run self.exit()

        If check_plugin_status raises NagiosPluginError, state is set to
        critical and error message is appended to message before exit
        """
        args = self.parse_args()
        self.message = ''

        try:
            self.check_plugin_status()
        except NagiosPluginError, emsg:
            self.state = 'CRITICAL'
            self.message += '{0}'.format(emsg)

        self.exit()

    def check_plugin_status(self):
        """Run the plugin

        Method required to execute this plugin, executed from self.run()

        Implement your test case in this method.

        """

        raise NotImplementedError('You must define check_plugin_status method in your actual plugin class')

class NagiosSNMPPlugin(NagiosPlugin):
    """Nagios SNMP check plugin wrapper

    Class to implement plugins which use SNMP to check check_plugin_status

    Instance of seine.snmp.client.SNMPClient is available to check_plugin_status with
    provided credentials.
    """
    def __init__(self, description=None):
        NagiosPlugin.__init__(self, description=description)
        self.client = None

        self.add_argument('-H', '--host', required=True, help='SNMP host to contact')
        self.add_argument('-1', '--v1', action='store_true', help='Use SNMP V1')
        self.add_argument('-2', '--v2c', action='store_true', help='Use SNMP V2')
        self.add_argument('-3', '--v3', action='store_true', help='Use SNMP V3')
        self.add_argument('-C', '--community', help='SNMP community for SNMP v1 / v2')
        self.add_argument('--username', help='SNMP username for SNMP v3')
        self.add_argument('--auth-pass', help='SNMP authentication password for SNMP v3')
        self.add_argument('--priv-pass', help='SNMP privacy password for SNMP v3')
        self.add_argument('--auth-protocol', help='SNMP v3 authentication protocol')
        self.add_argument('--priv-protocol', help='SNMP v3 privacy protocol')

    def parse_args(self, *args, **kwargs):
        """Parse SNMP plugin arguments

        Initialize plugin arguments, requiring valid SNMP session settings

        As a side effect, self.client() is set to SNMP session.

        """
        args = NagiosPlugin.parse_args(self, *args, **kwargs)

        if not args.v1 and not args.v2c and not args.v3:
             self.error('SNMP version not specified')

        if args.v1 or args.v2c:
            if args.username or args.auth_pass or args.priv_pass:
                self.error('Incompatible SNMP arguments')
        elif args.v3 and args.community:
            self.error('Incompatible SNMP arguments')

        if args.v1:
            if args.community is None:
                self.error('SNMP v1 requires community')
            auth = SNMPv1Auth(args.community)

        elif args.v2c:
            if args.community is None:
                self.error('SNMP v2c requires community')
            auth = SNMPv2cAuth(args.community)

        elif args.v3:
            if not args.username and not args.auth_pass:
                self.error('SNMP v3 requires username and authentication password')

            auth = SNMPv3Auth(args.username, args.auth_pass,
                args.priv_pass, args.auth_protocol, args.priv_protocol
            )

        self.client = SNMPClient(address=args.host, auth=auth)

        return args

    def check_plugin_status_example(self):
        """Example SNMP GET plugin test

        Example SNMP GET test: receives sysDescr (1.3.6.1.2.1.1.1.0) from
        host, splits result and returns second field

        """

        oid = '.1.3.6.1.2.1.1.1.0'
        try:
            res = self.client.get(oid)
        except SNMPError, emsg:
            raise NagiosPluginError('ERROR reading OID {0}: {1}'.format(oid, emsg))

        try:
            value = '{0}'.format(res[1])
            self.message += value.split()[2]
            self.state = 'OK'
        except IndexError:
            raise NagiosPluginError('Error splitting SNMP GET result {0}'.format(res[1]))
