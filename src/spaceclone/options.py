import sys
from optparse import OptionParser, OptionGroup

class Parser:

        def __init__(self, args):
            usage = "usage: %prog [options]"
	    if len(args) > 1:
		usage = "usage: %prog " + args[1] + " [options]"

            self.args = args
            self.parser = OptionParser(usage=usage)
            self.required = None

        def add_group(self, optgroup):
            self.parser.add_option_group(optgroup)

        def set_required(self, required):
            self.required = required

        def add_satellite_options(self):
            satgroup = OptionGroup(self.parser, "Satellite Options")
            
            satgroup.add_option("-s", "--server", action="store", type="string", dest="sat_server", help="Server Name")
            satgroup.add_option("-u", "--username", action="store", type="string", dest="sat_username", help="Username")
            satgroup.add_option("-p", "--password", action="store", type="string", dest="sat_password", help="Password")

            self.parser.add_option_group(satgroup)

        def parse(self):
            (options, args) = self.parser.parse_args(self.args)
            if self.required:
                missing = []
                for requirement in self.required:
                    if not options.__dict__[requirement]:
                        missing.append(requirement)
                if missing != []:
                    self.parser.print_help()
                    print ""
                    print "** Missing Required Options: " + str(missing)
                    sys.exit()

            return (options, args)
                 

