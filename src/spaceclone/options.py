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

    def add_satellite_options(self):
	satgroup = OptionGroup(self.parser, "Satellite Options")
	satgroup.add_option("-s", "--server", action="store", type="string", dest="sat_server", help="Server Name")
	self.parser.add_option_group(satgroup)

    def set_required(self, required):
        self.required = required

    def parse(self):
        (options, args) = self.parser.parse_args(self.args)

        if self.required:

            missing = []
            for requirement in self.required:
                if not options.__dict__[requirement]:
                    missing.append(requirement)

            if missing:
                for dest in missing:
                    opt = self.get_option(dest)
		    answer = raw_input(opt.help + ": ")

                    if not answer:
                        print "Required options can not be blank"
                        sys.exit()
                    else:
                        options.__dict__[dest] = answer

        return (options, args)

    def get_option(self, destination):
        for group in self.parser.option_groups:
            for option in group.option_list:
                if destination == option.dest:
                    return option
