__module_name__ = "Move"
__module_desc__ = "Move a system to a cloneset"

import sys
from optparse import OptionGroup
from optparse import OptionConflictError
from prettytable import PrettyTable

from ..satellite import Satellite, Cloneset, Clone

def run(parser, rhn, logger):

    parser.add_satellite_options()

    parser.set_required(["sat_server", "sat_username", "sat_password", "systemid", "cloneset"])

    group = OptionGroup(parser.parser, "Move Options")
    group.add_option("-i", "--systemid", action="store", type="int", dest="systemid", help="System ID")
    group.add_option("-c", "--cloneset", action="store", type="string", dest="cloneset", help="Cloneset")
    parser.add_group(group)

    (options, args) = parser.parse()

    rhn = Satellite(options.sat_server, options.sat_username, options.sat_password)

    # find our current cloneset
    baselabel = rhn.get_base_channel(options.systemid)
    original_base = baselabel

    children = [channel["label"] for channel in rhn.get_child_channels(options.systemid)]

    original = {}
    target = {}

    cloneset = None
    
    # Get basenames for system channels
    for k, cs in rhn.get_clones().iteritems():
        if cs.base.label == baselabel:
            baselabel = cs.base.baselabel
            cloneset = cs.base.cloneset_label
            
    table = PrettyTable(["Before", "After"])
    table.align = "l"
    subscribeTo = []
    if cloneset != None:
        currentCloneSet = rhn.cloneset_info(cloneset)
        for child in currentCloneSet.children:
            if child.label in children:
                subscribeTo.append(child.baselabel)
                original[child.baselabel] = child.label  
    else:
        subscribeTo = children

    target_cloneset = rhn.cloneset_info(options.cloneset)
    target_subscribe = []

    for child in target_cloneset.children:
        if child.baselabel in subscribeTo:
            target_subscribe.append(child.label)
            target[child.baselabel] = child.label   
 
    table.add_row([original_base, target_cloneset.base.label])

    for k, v in original.iteritems():
        try:
            table.add_row([v, target[k]])
        except KeyError:
            table.add_row([v, "!!!!!! No Match Found !!!!!!"])

    print "Moving system..."
    print table
    print ""
    yesno = raw_input("Confirm changes? [Y/n] ")
    if yesno.rstrip() != "Y":
        print "Aborted."
        sys.exit()
    
    rhn.set_base_channel(options.systemid, target_cloneset.base.label)
    rhn.set_child_channels(options.systemid, target_subscribe)
