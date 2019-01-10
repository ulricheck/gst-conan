from .. import base

from .PackageInfo import PackageInfo

from   collections import OrderedDict as odict
import json
import os

class Config:
    '''
    This instance encapsulates data loaded from the `config` folder, and relevant functionality.
        self.packages: Information about each conan package.
    '''

    def __init__(self):
        self.packages = odict() # packages.json

    def conanDataFolder(self) -> str:
        output = os.path.expanduser(os.getenv("CONAN_USER_HOME", "~/.conan/data"))
        return output

    @staticmethod
    def load(configFolder:str=None) -> 'Config':
        if configFolder == None:
            configFolder = base.gstConanConfigFolder()

        output = Config()

        output.packages = base.loadJsonObject(os.path.join(configFolder, "packages.json"), True)
        for key, val in output.packages.items():
            output.packages[key] = PackageInfo(val)

        return output
