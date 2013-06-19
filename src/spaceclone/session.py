# Initial attempt at session creation
# Check for existing session, if exists, use it
# If no exisiting session, prompt for missing information
# initial ideas from this code from spacewalk-manage-channel-lifecycle

session = None
session_cache.mkstemp(prefix="sct-")

# check for an existing session
if os.path.exists(session_cache[1]):
    try:
        fh = open(session_cache[0], 'r')
        session = fh.readline()
        fh.close()
   except IOError, e:
        if options.debug: logging.exception(e)
        logging.debug('Failed to read session cache')

    # validate the session
    try:
        client.channel.listMyChannels(session)
    except xmlrpclib.Fault, e:
        if options.debug: logging.exception(e)
        logging.warning('Existing session is invalid')
        session = None

if not session:
    # prompt for the username
    if not options.sat_username:
        options.sat_username = raw_input('Spacewalk Username: ')

    # prompt for the password
    if not options.sat_password:
        options.sat_password = getpass.getpass('Spacewalk Password: ')

    # login to the server
    try:
        session = client.auth.login(options.username, options.password)
    except xmlrpclib.Fault, e:
        if options.debug: logging.exception(e)
        logging.error('Failed to log into %s' % options.server)
        sys.exit(1)

    # save the session for subsuquent runs
    try:
        fh = open(session_cache[0], 'w')
        fh.write(session)
        fh.close()
    except IOError, e:
        if options.debug: logging.exception(e)
        logging.warning('Failed to write session cache')

