import re
import pickle
import base64
import datetime


class Clone:

    def __init__(self, **kwargs):
        self.chanid = None
        self.source = None
        self.prefix = None
        self.parent = None
        self.cloneset = None
        self.basename = None
        self.baselabel = None
        self.summary = "Spaceclone Channel"
        self.created = datetime.datetime.now()

        self.__dict__.update(kwargs)

    @property
    def cloneset_label(self):
        return "-".join(self.cloneset.split(" ")).lower()

    @property
    def name(self):
        return self.prefix + " - " + self.cloneset + " - " + self.basename

    @property
    def label(self):
        return ("sc" + "-" + "-".join(self.cloneset.split(" ")) +
                "-" + self.baselabel).lower()

    @property
    def definition(self):
        definition =  { "name":      self.name,
                        "label":     self.label,
                        "summary":   self.summary }

        if self.parent:
            definition["parent_label"] = self.parent

        return definition

    @property
    def pickle(self):
        base64pickle = "$DO NOT REMOVE$sc$%s$" % base64.b64encode(pickle.dumps(self))
        return re.sub("(.{70})", "\\1\n", base64pickle, 0) + "\n"

    def create(self, rhn):
        self.chanid = rhn.sat.channel.software.clone(rhn.key, self.source, self.definition, False)
        rhn.sat.channel.software.setDetails(rhn.key, self.chanid, { "description": self.pickle })
        return self.chanid

    def delete(self, satellite):
        satellite.sat.channel.redhat.delete(satellite.key, self.baselabel)

    def promote(self, satellite):
        pass

if __name__ == "__main__":
    clone = Clone()
    clone.source = "rhel-x86_64-server-6"
    clone.prefix = "Spaceclone"
    clone.cloneset = "June 2013"
    clone.basename = "Red Hat Enterprise Linux Server (v. 6 for 64-bit x86_64)"
    clone.baselabel="rhel-x86_64-serverRed Hat Enterprise Linux Server (v. 6 for 64-bit x86_64)"
    print clone.pickle
