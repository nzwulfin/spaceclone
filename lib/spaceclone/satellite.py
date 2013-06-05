from prettytable import PrettyTable
import datetime
import base64
import pickle
import getpass
import xmlrpclib
import re

class Satellite:

    def __init__(self):
        self.sat = None
        self.key = None

    def login(self, server, username, password, verbose=0):
        if server == None:
            server = self.ask_user("Server: ")

        if username == None:
            username = self.ask_user("Username: ")

        if password == None: 
            password = self.ask_user("Password: ", secret=True)

        self.sat = xmlrpclib.Server("http://" + server + "/rpc/api", verbose=verbose)
        self.key = self.sat.auth.login(username, password)

    def new_snapshot(self, original, name):

        # Create base channel clone
        base = self.create_clone(original, name)

        # Create children clone
        for child in self.sat.channel.software.listChildren(self.key, original):
            self.create_clone(child["label"], name, parent=base)

    def create_clone(self, original, name, parent=None):
        labelPrefix = "sc-" + "-".join(name.split(" ")).lower()
        namePrefix = "Spaceclone - " + name + " - "

        sourceDetails = self.sat.channel.software.getDetails(self.key, original)

        newChannel = { "name": namePrefix + " " + sourceDetails["name"],
                       "label": labelPrefix + "-" + sourceDetails["label"],
                       "summary": "New Snapshot" }

        if parent:
            newChannel["parent_label"] = parent

        print "Cloning %s to %s..." % (original, newChannel["label"])
        newId = self.sat.channel.software.clone(self.key, sourceDetails["label"], newChannel, False)

        # Set description
        newChannel["source"] = original
        newChannel["sc-name"] = "-".join(name.split(" ")).lower()
        newChannel["created"] = datetime.datetime.now()
        description = "$spaceclone$" + base64.b64encode(pickle.dumps(newChannel)) + "$"
        description = re.sub("(.{70})", "\\1\n", description, 0, re.DOTALL)
        self.sat.channel.software.setDetails(self.key, newId, { "description": description })

        return newChannel["label"]

    def get_clones(self):
        clones = []
        channels = self.sat.channel.listAllChannels(self.key)
        for channel in channels:
            details = self.sat.channel.software.getDetails(self.key, channel["label"])
            details["description"] = re.sub("\n", "", details["description"])
            if details["parent_channel_label"] == '' and re.match("\$spaceclone\$.*\$", details["description"]):
                decoded = pickle.loads(base64.b64decode(re.search("\$spaceclone\$(.*)\$", details["description"]).group(1)))
                decoded["id"] = details["id"]
                decoded["systems"] = channel["systems"]
                clones.append(decoded)

        return clones

    def list_clones(self):
        clones = self.get_clones()
        cloneRows = []

        for clone in clones:
                cloneRows.append([clone["sc-name"], clone["source"], clone["created"].strftime("%d %b %Y"), clone["systems"]])

        table = PrettyTable(["Spaceclone", "Original Base Channel", "Created On", "Systems"])
        table.align = "l"
        for row in cloneRows:
            table.add_row(row)

        return table

    def show_clone(self, clone):
        result = "\nSpaceclone Name:\t" + clone + "\n\n"

        clones = self.get_clones()
        for clone in clones:
            #if clone["sc-name"] == clone:
            result = result + self.get_tree(clone["label"])
            #else:
            #    result = None

        return result

    def get_tree(self, label):
        tree = label
        for child in self.sat.channel.software.listChildren(self.key, label):
            tree = tree + "\n  \.." + child["label"]
        tree = tree + "\n"

        return tree

    def ask_user(self, prompt, secret=False):
        if secret:
            result = getpass.getpass(prompt + "\t")
        else:
            result = raw_input(prompt + "\t")

        return result
