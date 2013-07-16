__module_name__ = "report"
__module_desc__ = "Provides a report about a cloneset"

import sys
from optparse import OptionGroup
from ..satellite import Satellite, Cloneset, Clone


def run(parser, rhn, logger):

    parser.add_satellite_options()

    group = OptionGroup(parser.parser, "Report Options")
    group.add_option("-c", "--cloneset", action="store", type="string", dest="cloneset", help="Cloneset")
    parser.add_group(group)

    parser.set_required(["sat_server", "cloneset"])

    (options, args) = parser.parse()

    rhn = Satellite(options.sat_server)

    for system in rhn.get_systems(rhn.cloneset_info(options.cloneset).base.label):
        print "Systems registered to " + options.cloneset + ":"
        print "\t" + system["name"]
