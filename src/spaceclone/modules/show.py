__module_name__ = "show"
__module_desc__ = "Show a specific Cloneset"

import sys
from optparse import OptionGroup
from optparse import OptionConflictError
from prettytable import PrettyTable

from ..satellite import Satellite, Cloneset, Clone

def run(parser, rhn, logger):

    try:
        parser.add_satellite_options()
    except OptionConflictError:
        # MAybe we were called from another module
        pass

    parser.set_required(["sat_server", "sat_username", "sat_password", "cloneset"])


    try:
        group = OptionGroup(parser.parser, "Show Options")
        group.add_option("-c", "--cloneset", action="store", type="string", dest="cloneset", help="Cloneset")
        parser.add_group(group)
    except OptionConflictError:
        # Maybe we were called from another module
        pass

    (options, args) = parser.parse()

    rhn = Satellite(options.sat_server, options.sat_username, options.sat_password)

    chanShow = PrettyTable(["Channel", "Type", "Origin", "Base"])
    chanShow.align = "l"

    try:
        cloneset = rhn.cloneset_info(options.cloneset)
    except KeyError:
        print "Cloneset not found: %s" % options.cloneset
        sys.exit()

    chanShow.add_row([cloneset.base.label, "parent", cloneset.base.source, cloneset.base.baselabel])

    for child in cloneset.children:
        chanShow.add_row([child.label, "child", child.source, child.baselabel])

    print chanShow
