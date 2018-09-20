from collections import OrderedDict as odict

import os

class PkgConfigFile:
    '''
    Represents the data stored in a pkg-config file.

    Keyword Fields:
    * Name (self.name)  A human-readable name for the library or package. This does not affect usage of the pkg-config
        tool, which uses the name of the .pc file.
    * Description (self.description) A brief description of the package.
    * URL (self.url) An informational URL
    * Version (self.version) The package version
    * Requires (self.requires) A comma-separated list of packages required by this package. The versions of these packages
        may be specified using the comparison operators =, <, >, <= or >=.
    * Requires.private (self.requiresPrivate)  A list of private packages required by this package but not exposed to
        applications. The version specific rules from the Requires field also apply here.
    * Conflicts (self.conflicts)  An optional field describing packages that this one conflicts with. The version specific
        rules from the Requires field also apply here. This field also takes multiple instances of the same package.
        E.g., Conflicts: bar < 1.2.3, bar >= 1.3.0.
    * Cflags (self.cflags) The compiler flags specific to this package and any required libraries that don't support
        pkg-config. If the required libraries support pkg-config, they should be added to Requires or Requires.private.
    * Libs (self.libs)
        The link flags specific to this package and any required libraries that don't support pkg-config. The same rule
        as Cflags applies here.
    * Libs.private (self.libsPrivate)
        The link flags for private libraries required by this package but not exposed to applications. The same rule as
        Cflags applies here.

    Variables:
    * self.variables
    '''

    def __init__(self):
        # Keyword fields
        self.name = None
        self.description = None
        self.url = None
        self.version = None
        self.requires = None
        self.requiresPrivate = None
        self.conflicts = None
        self.cflags = None
        self.libs = None
        self.libsPrivate = None

        # Variables
        self.variables = odict()

    def load(self, filename:str):
        with open(filename, "r") as reader:
            for rawLine in reader:
                line = rawLine.strip()
                if len(line) > 0 and not line.startswith("#"):
                    iColon = line.find(":")
                    iEquals = line.find("=")

                    lineIsKeyword = False # if not a keyword, then it's a variable

                    if iColon == 0 or iEquals == 1:
                        raise Exception(f"Pkg-config line starts with ':' or '=' character:  {rawLine}")

                    if iColon == -1 and iEquals == -1:
                        raise Exception(f"Pkg-config line could not be interpreted:  {rawLine}")
                    elif iColon == -1:
                        lineIsKeyword = False
                    elif iEquals == -1:
                        lineIsKeyword = True
                    else:
                        lineIsKeyword = iColon < iEquals

                    if lineIsKeyword:
                        key = line[0:iColon]
                        value = line[iColon+1:].strip()
                    else:
                        key = line[0:iEquals]
                        value = line[iEquals+1:]

                    if lineIsKeyword:
                        # FIXME:  Remove comments at end of `value` string.

                        if key=="Name":
                            self.name = value
                        elif key=="Description":
                            self.description = value
                        elif key=="URL":
                            self.url = value
                        elif key=="Version":
                            self.version = value
                        elif key=="Requires":
                            self.requires = value
                        elif key=="Requires.private":
                            self.requiresPrivate = value
                        elif key=="Conflicts":
                            self.conflicts = value
                        elif key=="Cflags":
                            self.cflags = value
                        elif key=="Libs":
                            self.libs = value
                        elif key=="Libs.private":
                            self.libsPrivate = value
                        else:
                            raise Exception(f"Pkg-config line starts with unrecognized keyword:  {rawLine}")
                    else:
                        # FIXME:  Remove comments at end of `value` string.
                        # See implementation of `os.path.expandvars` for hints about parsing the line.
                        self.variables[key] = value

    def save(self, filename:str):
        # ensure the parent folder exists
        parentFolder = os.path.dirname(filename)
        os.makedirs(parentFolder, exist_ok=True)

        # open the file for writing
        with open(filename, "w") as writer:
            # write variables
            for key, value in self.variables.items():
                writer.write(f"{key}={value}\n")

            writer.write("\n")

            # write keywords
            if self.name != None:
                writer.write(f"Name: {self.name}\n")
            if self.description != None:
                writer.write(f"Description: {self.description}\n")
            if self.url != None:
                writer.write(f"URL: {self.url}\n")
            if self.version != None:
                writer.write(f"Version: {self.version}\n")
            if self.requires != None:
                writer.write(f"Requires: {self.requires}\n")
            if self.requiresPrivate != None:
                writer.write(f"Requires.private: {self.requiresPrivate}\n")
            if self.conflicts != None:
                writer.write(f"Conflicts: {self.conflicts}\n")
            if self.cflags != None:
                writer.write(f"Cflags: {self.cflags}\n")
            if self.libs != None:
                writer.write(f"Libs: {self.libs}\n")
            if self.libsPrivate != None:
                writer.write(f"Libs.private: {self.libsPrivate}\n")
