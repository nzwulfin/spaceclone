__module_name__ = "list"
__module_desc__ = "Lists all spaceclones"

import sys
from optparse import OptionGroup

def run(parser, rhn, logger):

    parser.add_satellite_options()

    (options, args) = parser.parse()

    rhn.login(options.sat_server, options.sat_username, options.sat_password)

    print rhn.list_clones()
    print ""
