__module_name__ = "create"
__module_desc__ = "Creates a new snapshot"

import sys
from optparse import OptionGroup

def run(parser, rhn, logger):

    parser.add_satellite_options()

    group = OptionGroup(parser.parser, "Create Options")
    group.add_option("-o", "--original", action="store", type="string", dest="original", help="Original Base Channel")
    group.add_option("-n", "--name", action="store", type="string", dest="name", help="Snapshot Name")
    parser.add_group(group)
    
    parser.set_required(["name", "original"])

    (options, args) = parser.parse()

    rhn.login(options.sat_server, options.sat_username, options.sat_password)

    print rhn.new_snapshot(options.original, options.name)
