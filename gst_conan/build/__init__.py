from .PkgConfigFile import  PkgConfigFile

def conanBuildTypes() -> list:
    '''
    These are the conan build types that we allow.
    :return: The list of types allowed.
    '''
    return ["Debug", "Release"]

def mesonBuildTypes() -> list:
    return ["plain", "debug", "debugoptimized", "release"]