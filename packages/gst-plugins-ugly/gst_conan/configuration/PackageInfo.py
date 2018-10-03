from .. import base

from   collections import OrderedDict as odict

class PackageInfo:

    '''
    Supplemental information about a conan package.

    self.executables = A list of executable files.

    self.pkgconfigs = A tree of information about pkg-config files, where each keyed entry is:
        key = The name of the pkg-config file without the '.pc' extension.
        value.lib = The name of the static library without the '.so' or '.dll' extension.
        value.gir = The prefix of the '.gir' and '.typelib' files (if they exist).

    self.plugins = A tree of information about plugins, where each keyed entry is:
        key = The name of the plugin.
        value.debians = The list of debian *.deb packages that must be installed so that the plugin may be built.
        value.fedoras = The list of fedora *.rpm packages that must be installed so that the plugin may be built.
        value.lib = If provided, overrides the default library name without the '.a' or '.lib' extension.
            If not provided, this value defaults to f"libgst{key}"
        value.optional = If provided, determines whether the plugin is optional.  Defaults to false.

    self.sharedlibs = A list of shared lib files which not already listed within self.pkgconfigs.  File names are listed
        without the '.so' or '.dll' extension

    self.staticlibs = A list of static lib files without the '.a' or '.lib' extension.
    '''

    def __init__(self, dictionary):
        if not isinstance(dictionary, dict):
            raise Exception("The parameter must be a dictionary.")

        self.executables = []
        self.pkgconfigs = odict()
        self.plugins = odict()
        self.sharedlibs = []
        self.staticlibs = []

        for key, val in dictionary.items():
            self.__dict__[key] = val
