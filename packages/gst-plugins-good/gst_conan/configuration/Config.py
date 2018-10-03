from .. import base

from .PackageInfo import PackageInfo

from   collections import OrderedDict as odict
import json
import os

class Config:
    '''
    This instance encapsulates data loaded from the `config` folder, and relevant functionality.
        self.debians:  A list of non-optional debian-ish packages to be installed (required for the build on debian-ish systems).
        self.fedoras:  A list of non-optional fedora-ish packages to be installed (required for the build on fedora-ish systems).
        self.packages: Information about each conan package.
    '''

    def __init__(self):
        self.debians  = []      # debians.json
        self.fedoras  = []      # fedoras.json
        self.packages = odict() # packages.json

    def debianRequirements(self, optionals: bool) -> list:
        '''
        Get the debian packages required for setting up the build.
        :param optionals:  If true, packages supporting all optional plugins are included.
        :return: The list of required debian packages.
        '''
        output = self.debians.copy()

        for packageName, packageInfo in self.packages.items():
            for pluginName, pluginInfo in packageInfo.plugins.items():
                debs = pluginInfo.get("debians")
                if debs != None:
                    op = pluginInfo.get("optional")
                    if op == None:
                        op = False

                    if optionals or not op:
                        output += debs

        return output


    def fedoraRequirements(self, optionals: bool) -> list:
        '''
        Get the fedora rpm packages required for setting up the build.
        :param optionals:  If true, optional packages are included.
        :return: The list of required fedora rpm packages.
        '''
        output = self.fedoras.copy()

        for packageName, packageInfo in self.packages.items():
            for pluginName, pluginInfo in packageInfo.plugins.items():
                rpms = pluginInfo.get("fedoras")
                if rpms != None:
                    op = pluginInfo.get("optional")
                    if op == None:
                        op = False

                    if optionals or not op:
                        output += rpms

        return output

    @staticmethod
    def load(configFolder:str=None) -> 'Config':
        if configFolder == None:
            configFolder = base.gstConanConfigFolder()

        output = Config()

        output.packages = base.loadJsonObject(os.path.join(configFolder, "packages.json"), True)
        for key, val in output.packages.items():
            output.packages[key] = PackageInfo(val)

        with open(os.path.join(configFolder, "debians.json")) as fileReader:
            output.debians = json.load(fileReader)

        with open(os.path.join(configFolder, "fedoras.json")) as fileReader:
            output.fedoras = json.load(fileReader)

        return output
