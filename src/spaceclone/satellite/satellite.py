import base64
import re
import pickle
import xmlrpclib
import zlib
import tempfile
import getpass
import time
import os
from cloneset import Cloneset

class Satellite:

    def __init__(self, server, verbose=0):
        self._sat = xmlrpclib.Server("http://" + server + "/rpc/api", verbose=verbose)
        self._channels = {}
        self._clonesets = {}
	self._key = None

	# Build the cache file location based on CRC32 of server name
	active_key = None
	hexhash = "%08x" % zlib.crc32(server)
	cache_file = str(tempfile.gettempdir()) + '/spc-' + str(hexhash)
	try:
		with open(cache_file) as cache:
			cache_creds = cache.read()
			cache_key, cache_time = cache_creds.split(":")
			# If the cached key is less than 5 mins old, use it
			if time.time() - float(cache_time) < 300:
				active_key = cache_key
			else:
				print "Cached credentials too old"
				active_key = None
	except IOError:
		print "No cached credentials found"
		pass
	if active_key is None:
	# Prompt for user credentials
		username = raw_input("Org Admin username: ")
		password = getpass.getpass("Org Admin password: ")
		active_key = self._sat.auth.login(username, password)

	if self._sat.channel.listMyChannels(active_key):
		ts = time.time()
		cred = active_key + ':' + str(ts)
		with os.fdopen(os.open(cache_file, os.O_WRONLY | os.O_CREAT, 0o0600), 'w') as cache:
			cache.write(cred)
			cache.close()
		self._key = active_key

   	if self._key is None:
		exit(1)

    @property
    def sat(self):
        return self._sat

    @property
    def key(self):
        return self._key

    def get_systems(self, label):
        return self.sat.channel.software.listSubscribedSystems(self.key, label)

    def get_channels(self):
        if self._channels == {}:
            for channel in self.sat.channel.listAllChannels(self.key):
                self._channels[channel["label"]] = self.sat.channel.software.getDetails(self.key, channel["label"])
                self._channels[channel["label"]]["systems"] = channel["systems"]
                self._channels[channel["label"]]["children"] = self.sat.channel.software.listChildren(self.key, channel["label"])

        return self._channels

    def get_clones(self):
        if self._clonesets == {}:
            clones = []
            for channel in self.get_channels():
                desc = re.sub("\n", "", self.channel_info(channel)["description"])
                if re.match(".*\$sc\$.*\$.*", desc):
                    clones.append(pickle.loads(base64.b64decode(re.search("\$sc\$(.*)\$", desc).group(1))))

            for clone in clones:
                if clone.parent is None:
                    self._clonesets[clone.cloneset_label] = Cloneset(self)
                    self._clonesets[clone.cloneset_label].base = clone

            for clone in clones:
                if clone.parent is not None:
                    self._clonesets[clone.cloneset_label].add(clone)

        return self._clonesets

    def get_child_channels(self, systemid):
        return self.sat.system.listSubscribedChildChannels(self.key, systemid)

    def get_base_channel(self, systemid):
        return self.sat.system.getSubscribedBaseChannel(self.key, systemid)["label"]

    def set_base_channel(self, systemid, label):
        return self.sat.system.setBaseChannel(self.key, systemid, label)

    def set_child_channels(self, systemid, children):
        return self.sat.system.setChildChannels(self.key, systemid, children)

    def channel_info(self, label):
        return self.get_channels()[label]

    def cloneset_info(self, cloneset):
        return self.get_clones()[cloneset]
