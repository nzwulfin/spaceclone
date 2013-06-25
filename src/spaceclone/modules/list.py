__module_name__ = "List"
__module_desc__ = "List all clonesets"

import sys
from optparse import OptionGroup
from prettytable import PrettyTable

from ..satellite import Satellite, Cloneset, Clone

def run(parser, rhn, logger):

    parser.add_satellite_options()

    parser.set_required(["sat_server", "sat_username", "sat_password"])

    (options, args) = parser.parse()

    rhn = Satellite(options.sat_server, options.sat_username, options.sat_password)

    chanList = PrettyTable(["Cloneset", "Created", "Origin", "Base", "Registered Systems"])
    chanList.align = "l"
    for label, cloneset in rhn.get_clones().iteritems():
        chanList.add_row(["-".join(cloneset.base.cloneset.lower().split(" ")), cloneset.base.created.strftime("%d %B %Y"), cloneset.base.source, cloneset.base.baselabel, rhn.channel_info(cloneset.base.label)["systems"]])
    print chanList
