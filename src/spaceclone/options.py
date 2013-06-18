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
            
        satgroup.add_option("-s", "--server", action="store", type="string", dest="sat_server", help="Satellite Server Name")
        satgroup.add_option("-u", "--username", action="store", type="string", dest="sat_username", help="Satellite Username")
        satgroup.add_option("-p", "--password", action="store", type="string", dest="sat_password", help="Satellite Password")

        self.parser.add_option_group(satgroup)

    def parse(self):
        (options, args) = self.parser.parse_args(self.args)

        # This is really hacky, is there a better way?
        # Prompt users to provide required options interactively
        # if they're missing

        if self.required:
            missing = []
            for requirement in self.required:
                if not options.__dict__[requirement]:
                    missing.append(requirement)
            if missing != []:
                for destination in missing:
                    option = self.get_option(destination)
                    if "password" not in option.help.lower():
                        answer = raw_input(option.help + ": ")
                    else:
                        answer = getpass(option.help + ": ")

                    if answer == None:
                        self.parser.print_help()
                        print "Invalid Option: " + option.help
                        sys.exit()
                    else:
                        self.args.append(option._short_opts[0])
                        self.args.append(answer)

        (options, args) = self.parser.parse_args(self.args)
        return (options, args)

    def get_option(self, destination):
        for group in self.parser.option_groups:
            for option in group.option_list:
                if destination == option.dest:
                    return option
