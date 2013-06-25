import sys
from getpass import getpass
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

            for requirement in self.required:
                if options.__dict__[requirement]:
                    self.required.pop(self.required.index(requirement))

            if self.required:
                for dest in self.required:
                    opt = self.get_option(dest)

                    if "password" in opt.help.lower():
                        answer = getpass(opt.help + ": ")
                    else:
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
