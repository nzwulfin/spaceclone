__module_name__ = "Move"
__module_desc__ = "Move a system to a cloneset"

import sys
from optparse import OptionGroup
from optparse import OptionConflictError
from prettytable import PrettyTable
from ..satellite import Satellite, Cloneset, Clone


def run(parser, rhn, logger):

    parser.add_satellite_options()

    parser.set_required(["sat_server", "sat_username", "sat_password", "cloneset"])

    group = OptionGroup(parser.parser, "Move Options")
    group.add_option("-i", "--systemid", action="store", type="int", dest="systemid", help="System ID")
    group.add_option("-n", "--hostname", action="store", type="string", dest="hostname", help="Hostname search")
    group.add_option("-c", "--cloneset", action="store", type="string", dest="cloneset", help="Cloneset")
    parser.add_group(group)

    (options, args) = parser.parse()

    rhn = Satellite(options.sat_server, options.sat_username, options.sat_password)

    servers = []

    if options.hostname:
        for system in rhn.sat.system.search.hostname(rhn.key, options.hostname):
            servers.append([system["id"], system["hostname"]])

    if options.systemid:
        system = rhn.sat.system.getDetails(rhn.key, options.systemid)
        servers.append([system["id"], system["hostname"]])

    if servers == []:
        print "No systems found."
    else:
        table = PrettyTable(["ID", "Hostname"])
        for server in servers:
            table.add_row(server)

    print "These systems will be moved..."
    print table

    yesno = raw_input("Confirm changes? [Y/n] ")
    if yesno.rstrip() != "Y":
        print "Aborted."
        sys.exit()
    else:
        for server in servers:
            print "Moving " + server[1] + "..."
            move(rhn, server[0], options.cloneset)


def move(rhn, systemid, cloneset):
    # find our current cloneset
    baselabel = rhn.get_base_channel(systemid)
    original_base = baselabel

    children = [channel["label"] for channel in rhn.get_child_channels(systemid)]

    original = {}
    target = {}

    cloneset_label = None

    # Get basenames for system channels
    for k, cs in rhn.get_clones().iteritems():
        if cs.base.label == baselabel:
            baselabel = cs.base.baselabel
            cloneset_label = cs.base.cloneset_label

    table = PrettyTable(["Before", "After"])
    table.align = "l"
    subscribeTo = []
    if cloneset_label is not None:
        currentCloneSet = rhn.cloneset_info(cloneset_label)
        for child in currentCloneSet.children:
            if child.label in children:
                subscribeTo.append(child.baselabel)
                original[child.baselabel] = child.label
    else:
        subscribeTo = children
        for child in subscribeTo:
            original[child] = child

    target_cloneset = rhn.cloneset_info(cloneset)
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

    print table
    print ""

    rhn.set_base_channel(systemid, target_cloneset.base.label)
    rhn.set_child_channels(systemid, target_subscribe)
