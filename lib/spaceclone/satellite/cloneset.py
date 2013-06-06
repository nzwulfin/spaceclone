import base64
import re
import pickle
import sys
from clone import Clone

class Cloneset:
    """
    A collection of Clones
    """

    def __init__(self, rhn, prefix=None, origin=None, target=None):
        self.base = None
        self.children = []
        self.rhn = rhn

        if [prefix, origin, target] != [None, None, None]:
            self.base = self.new(prefix, origin, target)

            for child in self.rhn.channel_info(self.base.source)["children"]:
                self.children.append(self.new(prefix, child["label"], target, parent=self.base.label))

    def new(self, prefix, origin, target, parent=None):

        desc = re.sub("\n", "", self.rhn.channel_info(origin)["description"])
        if re.match(".*\$sc\$.*\$.*", desc):
            decoded = pickle.loads(base64.b64decode(re.search("\$sc\$(.*)\$", desc).group(1)))
            basename = decoded.basename
            baselabel = decoded.baselabel
        else:
            basename = self.rhn.channel_info(origin)["name"]
            baselabel = origin

        clone = { 
                  "source": origin,
                  "prefix": prefix,
                  "cloneset": target,
                  "baselabel": baselabel,
                  "basename": basename,
                 }

        if parent:
            clone["parent"] = parent
           
        return Clone(**clone)

    def add(self, child):
        self.children.append(child)

    def create(self):
        print "\nCreating clone channels:"
        for clone in [self.base] + self.children:
            sys.stdout.write("\t\t" + clone.label + "...")
            sys.stdout.flush()
            clone.create(self.rhn)
            sys.stdout.write("  [ OK ]\n")
            sys.stdout.flush()

    def delete(self):
        for clone in self.children + [self.base]:
            sys.stdout.write("Deleting clone channel: " + clone.label + " ...")
            sys.stdout.flush()
            clone.delete(self.rhn)
            sys.stdout.write("  [ OK ]\n")
            sys.stdout.flush()

    @property
    def tree(self):
        tree = self.base.label
        for child in self.children:
            tree = tree + "\n  \.." + child.label
        tree = tree + "\n"

        return tree
