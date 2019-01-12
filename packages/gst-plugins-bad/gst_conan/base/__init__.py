'''
A 'base' layer of utility methods.
'''

from   collections import OrderedDict as odict
import ctypes
import logging
import json
import os
import shlex
import subprocess
import sys

def basenames(filenames:list) -> list:
    '''
    Executes `os.path.basename` on each element of the input to provide each element of the output.
    :param filenames: The input filenames.
    :return: The return value of `os.path.basename` for each of the input filenames.
    '''

    output = []
    for filename in filenames:
        output.append(os.path.basename(filename))

    return output

def currentUserIsPrivileged() -> bool:
    '''
    Determines whether the user has root (on linux) or administrative (on windows) privileges.
    :return: [bool]  On Linux, returns true if the effective user ID is 0 (meaning `root`), false otherwise.
    '''
    if isWindows():
        return 1 == ctypes.windll.shell32.IsUserAnAdmin()
    else:
        return 0 == os.geteuid()

def evaluate(cmd:str, throwable:bool=True, verbose:bool=True, workingFolder:str=None, fake:bool=False, env:dict=None) -> str:
    '''
    Executes the specified shell command and captures the console output.
    :param cmd:  The shell command.
    :param throwable:  If true, an exception is thrown if the command generates an error.
    :param verbose:  If true, the executed command is printed to the console.
    :param workingFolder:  The working folder for command execution.
    :param fake: If true, the command is not actually executed.  A stub message is sent to stdout.
    :param env:  The environment variables.  If None, the default environment variables are used (from os.environ).
    :return: The captured console output
    '''

    win = isWindows()

    if fake:
        if workingFolder == None:
            print("Fake command execution:")
        else:
            print("Fake command execution from "+workingFolder+":")
        print("\t" + cmd)
        return 0

    if verbose:
        if workingFolder == None:
            print("Executing command:")
        else:
            print("Executing command from "+workingFolder+":")
        print("\t" + cmd)

    sys.stdout.flush()

    try:
        if win:
            # windows will lex the command
            cmdLex = cmd
        else:
            cmdLex = shlex.split(cmd)
    except:
        if throwable:
            raise Exception("Unable to lex the command string:  " + cmd)
        return None

    if workingFolder != None:
        priorWorkingFolder = os.getcwd()
        os.chdir(workingFolder)

    try:
        if env is None:
            output = subprocess.check_output(cmdLex, shell=win)
        else:
            output = subprocess.check_output(cmdLex, shell=win, env=env)

        if (sys.version_info[0] >= 3):
            output = output.decode("utf-8", errors='replace')

        if win and len(output) >= 2:
            output = output[:-2]  # it always ends with "\r\n"
        elif len(output) >= 1:
            output = output[:-1]  # it always ends with "\n"

        return output
    except:
        if throwable:
            raise
        else:
            return None
    finally:
        if workingFolder != None:
            os.chdir(priorWorkingFolder)

def execute(cmd:str, throwable:bool=True, verbose:bool=True, workingFolder:str=None, fake:bool=False, env:dict=None) -> int:
    '''
    Executes the specified shell command.
    :param cmd:  The shell command.
    :param throwable:  If true, an exception is thrown if the command generates an error.
    :param verbose:  If true, the executed command is printed to the console.
    :param workingFolder:  The working folder for command execution.
    :param fake: If true, the command is not actually executed.  A stub message is sent to stdout.
    :param env:  The environment variables.  If None, the default environment variables are used (from os.environ).
    :return: The exit code of the function call.
    '''

    win = isWindows()

    if fake:
        if workingFolder == None:
            print("Fake command execution:")
        else:
            print("Fake command execution from "+workingFolder+":")
        print("\t" + cmd)
        return 0

    if verbose:
        if workingFolder == None:
            print("Executing command:")
        else:
            print("Executing command from "+workingFolder+":")
        print("\t" + cmd)

    sys.stdout.flush()

    try:
        if win:
            cmdLex = cmd
        else:
            cmdLex = shlex.split(cmd)
    except:
        if throwable:
            raise Exception("Unable to lex the command string:  " + cmd)
        return 1

    if workingFolder != None:
        priorWorkingFolder = os.getcwd()
        os.chdir(workingFolder)

    try:
        if throwable:
            if env is None:
                return subprocess.check_call(cmdLex, shell=win)
            else:
                return subprocess.check_call(cmdLex, shell=win, env=env)
        else:
            if env is None:
                return subprocess.call(cmdLex, shell=win)
            else:
                return subprocess.call(cmdLex, shell=win, env=env)
    finally:
        if workingFolder != None:
            os.chdir(priorWorkingFolder)

def getEnv(name:str) -> str:
    '''
    Gets the environment variable, where any internal variables are already decoded.
    :param name: The name of the variable.
    :return:  The value of the decoded variable.
    '''

    if isWindows():
        # Nested variables don't always resolve with `os.environ.get()` on Windows
        output = evaluate("echo %" + name + "%", verbose=False)
    else:
        output = os.environ.get(name)

    return output

def gstConanConfigFolder() -> str:
    '''
    Gets the folder inside which the `gst-conan/config` data is located
    :return: The absolute folder path.
    '''
    output = os.path.join(gstConanFolder(), "config")
    return output

def gstConanDockersFolder() -> str:
    '''
    Gets the folder inside which the `gst-conan/dockers` Dockerfiles are stored.
    :return: The absolute folder path.
    '''
    output = os.path.join(gstConanFolder(), "dockers")
    return output

def gstConanFolder() -> str:
    '''
    Gets the folder inside which the `gst-conan` script is located (i.e. the root folder of this repo) unless called
    from a conan package, in which case this is the "exports" folder (which contains the conanfile).
    :return: The absolute folder path.
    '''
    output = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
    return output

def isDarwin() -> bool:
    '''
    Determines whether the platform is Darwin (mac).
    :return: [bool] True if the platform is Darwin, false otherwise.
    '''
    return sys.platform.startswith("darwin")

def isLinux() -> bool:
    '''
    Determines whether the platform is Linux.
    :return: [bool] True if the platform is Linux, false otherwise.
    '''
    return sys.platform.startswith("linux")

def isWindows() -> bool:
    '''
    Determines whether the platform is Windows.
    :return: [bool] True if the platform is Windows, false otherwise.
    '''
    return sys.platform.startswith("win")

def loadJsonObject(jsonFile:str, raiseError:bool=True) -> odict:
    if not os.path.isfile(jsonFile):
        if raiseError:
            raise Exception('The file "' + jsonFile + '" does not exist.')
        else:
            return None

    output = None
    with open(jsonFile) as jsonFileHandle:
        output = json.load(jsonFileHandle, object_pairs_hook=odict)

    return output

def raiseError(message:str) -> None:
    logging.error(message)
    print("")
    print("")
    raise Exception(message)

def readNonEmptyLines(filename:str) -> list:
    '''
    Reads lines from a file.  Strips the newline character from each line.  Ignores empty lines.
    :param filename: The file from which entries are read.
    :return: A list where each entry is a non-empty line of the file.
    '''
    output = []
    with open(filename, "r") as f:
        for line in f:
            txt = line.rstrip("\n").rstrip("\r")
            if len(txt) > 0:
                output.append(txt)

    return output