import usage
import satellite
import logging
import modules
import options

def run(args):

    parser = options.Parser(args)
    logger = None
    rhn = None

    # First option on command line should be valid module
    if len(args) < 2 or args[1] not in modules.__all__:
        usage.run()
    else:
        # Pass args to module
        module = args.pop(1)
        getattr(modules, module).run(parser, rhn, logger)
