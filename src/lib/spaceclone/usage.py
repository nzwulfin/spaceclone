import modules
from modules import *


def run():
    print "Usage: spaceclone <command> <options>"
    print ""
    print "Commands:"

    for module in modules.__all__:
        print "%s\t\t%s" % (module, getattr(modules, module).__module_desc__)
