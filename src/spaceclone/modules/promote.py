__module_name__ = "promote"
__module_desc__ = "Promotes a cloneset to the same version as it's origin"

import sys
from optparse import OptionGroup
from prettytable import PrettyTable
from ..satellite import Satellite, Cloneset, Clone


def run(parser, rhn, logger):

    parser.add_satellite_options()

    group = OptionGroup(parser.parser, "Promote Options")
    group.add_option("-c", "--cloneset", action="store", type="string", dest="cloneset", help="Cloneset")
    parser.add_group(group)

    parser.set_required(["sat_server", "sat_username", "sat_password", "cloneset"])

    (options, args) = parser.parse()

    rhn = Satellite(options.sat_server, options.sat_username, options.sat_password)

    cloneset = rhn.cloneset_info(options.cloneset)

    print "\nThe following target channels will be updated with the content in the origin channel:\n"

    table = PrettyTable(["Origin", "", "Target"])

    table.align = "l"

    channels = {}

    for clone in [cloneset.base] + cloneset.children:
        table.add_row([clone.source, "-->", clone.label])
        channels[clone.label] = clone.source

    print table

    yesno = raw_input("\nConfirm? [Y/n] ")

    if yesno.rstrip() != "Y":
        print "Aborted."
        sys.exit()

    for target, origin in channels.iteritems():
        sys.stdout.write("Merging %s to %s... " % (origin, target))
        sys.stdout.flush()
        rhn.sat.channel.software.mergePackages(rhn.key, origin, target)
        sys.stdout.write("[ OK ]\n")
        sys.stdout.flush()

    print ""
