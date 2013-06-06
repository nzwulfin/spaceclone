__module_name__ = "Delete"
__module_desc__ = "Delete a specific Cloneset"

import sys
from optparse import OptionGroup
from prettytable import PrettyTable
import show
from ..satellite import Satellite, Cloneset, Clone

def run(parser, rhn, logger):

    parser.add_satellite_options()

    parser.set_required(["sat_server", "sat_username", "sat_password", "cloneset"])

    group = OptionGroup(parser.parser, "Show Options")
    group.add_option("-c", "--cloneset", action="store", type="string", dest="cloneset", help="Cloneset")
    parser.add_group(group)

    (options, args) = parser.parse()

    rhn = Satellite(options.sat_server, options.sat_username, options.sat_password)

    try:
        cloneset = rhn.cloneset_info(options.cloneset)
    except KeyError:
        print "Cloneset not found: %s" % options.cloneset
        sys.exit()

    print ""
    print "Selected cloneset: " + options.cloneset
    print ""
    show.run(parser, rhn, logger)

    response = raw_input("Are you sure? (This can't be undone) [Y/n] ")
    if response.rstrip() == "Y":
        cloneset.delete()
    else:
        print "Aborted."
