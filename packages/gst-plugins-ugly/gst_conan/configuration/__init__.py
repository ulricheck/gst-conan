from .Config import Config

# Holds the current configuration values.
__currentConfig = None

def getCurrent() -> Config:
    # The 'global' declaration allows us to refer to the module-scoped variable.
    global __currentConfig
    if __currentConfig == None:
        __currentConfig = Config.load()

    return __currentConfig

def setCurrent(value:Config) -> None:
    # The 'global' declaration allows us to refer to the module-scoped variable.
    global __currentConfig
    __currentConfig = value