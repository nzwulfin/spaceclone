__module_name__ = "create"
__module_desc__ = "Creates a new cloneset"

import sys
from optparse import OptionGroup
from ..satellite import Satellite, Cloneset, Clone


def run(parser, rhn, logger):

    parser.add_satellite_options()

    group = OptionGroup(parser.parser, "Create Options")
    group.add_option("-o", "--origin", action="store", type="string", dest="origin", help="Origin Base Channel")
    group.add_option("-t", "--target", action="store", type="string", dest="target", help="Target Cloneset Name")
    group.add_option("-f", "--prefix", action="store", type="string", dest="prefix", default="Spaceclone", help="Prefix for Channel Name")
    parser.add_group(group)

    parser.set_required(["sat_server", "target", "origin"])

    (options, args) = parser.parse()

    rhn = Satellite(options.sat_server)
    cloneset = Cloneset(rhn, prefix=options.prefix, origin=options.origin, target=options.target)
    cloneset.create()
