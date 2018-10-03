# The same exact file exists next to each `conanfile.py` within this repo.
# We are waiting for a Conan bug to get fixed:  https://github.com/conan-io/conan/issues/3591

# testing-3591

import sys
if sys.version_info[0] < 3:
    raise Exception("The version of Python must be 3 or greater.")

from .PkgConfigFile import PkgConfigFile

import fnmatch
import os
import re
import shutil


def copyFiles(pattern:str, srcFolder:str, destFolder:str, keepPath:bool=True) -> list:
    '''
    Copies files having a specified pattern within the source folder.  This function exists because I had problems using
    `self.copy` inside the conanfile.
    :param pattern: The wildcard filename pattern.  See the python function `fnmatch.fnmatch` for information on wildcards.
    :param srcFolder: The source folder (i.e. where the files are copied from)
    :param destFolder: The destination folder (where files are copied to).
    :param keepPath:  If true, the relative path underneath `srcFolder` will be preserved for the copy into `destFolder`.
    If false, the files are copied directly under destFolder.
    :return: The list of copied files relative to the `destFolder`.
    '''

    output = []

    files = findFiles(pattern, srcFolder)

    for file in files:
        srcFile = os.path.join(srcFolder, file)

        if keepPath:
            destFile = file
        else:
            destFile = os.path.basename(file)

        output.append(destFile)

        destFile = os.path.join(destFolder, destFile)

        parentFolder = os.path.dirname(destFile)
        if parentFolder != None and len(parentFolder) > 0:
            os.makedirs(parentFolder, exist_ok=True)

        shutil.copy2(srcFile, destFile, follow_symlinks=False)

    return output

def copyOneFile(pattern:str, srcFolder:str, destFolder:str, keepPath:bool=True) -> str:
    '''
    This is the same as `copyFile` except it throws if the number of files copied is not exactly one.
    '''
    output = copyFiles(pattern, srcFolder, destFolder, keepPath)
    if len(output) == 0:
        raise Exception(f"Failed to find {pattern} within folder: {srcFolder}")

    if len(output) > 1:
        raise Exception(f"Found multiple {pattern} within folder: {srcFolder}")

    return output[0]

def copyOneSharedObjectFileGroup(pattern:str, srcFolder:str, destFolder:str, keepPath:bool=True) -> list:
    '''
    The same as `copySharedObjectFileGroups` except there must be exactly one group, otherwise it throws.
    '''

    output = []

    groups = findSharedObjectGroups(pattern, srcFolder)

    if len(groups) == 0:
        raise Exception(f"Failed to find {pattern} within folder: {srcFolder}")

    if len(groups) > 1:
        raise Exception(f"Found multiple {pattern} groups within folder: {srcFolder}")

    for group in groups:
        for file in group:
            srcFile = os.path.join(srcFolder, file)

            if keepPath:
                destFile = file
            else:
                destFile = os.path.basename(file)

            output.append(destFile)

            destFile = os.path.join(destFolder, destFile)

            parentFolder = os.path.dirname(destFile)
            if parentFolder != None and len(parentFolder) > 0:
                os.makedirs(parentFolder, exist_ok=True)

            shutil.copy2(srcFile, destFile, follow_symlinks=False)

    return output

def copySharedObjectFileGroups(pattern:str, srcFolder:str, destFolder:str, keepPath:bool=True) -> list:
    '''
    Each *.so file can have multiple companions with a version number appended after the `.so` suffix.  The companions
    can be files or links to files.  For example:
        libwhatever.so
        libwhatever.so.0  [symlink --> libwhatever.so.0.1234.0]
        libwhatever.so.0.1234.0
        libwhatever.so.1  [symlink --> libwhatever.so.1.4321.0]
        libwhatever.so.1.4321.0

    This method finds any filename whose prefix (before the `.so`) match the given pattern.  For each pattern, the `*.so`
    file is copied with all of it's companions.

    :param pattern: The wildcard filename pattern for the prefix of the file (before the `.so`).  This should not include
    the `.so` or anything that comes after.  See the python function `fnmatch.fnmatch` for information on wildcards.
    :param srcFolder: The source folder (i.e. where the files are copied from)
    :param destFolder: The destination folder (where files are copied to).
    :param keepPath:  If true, the relative path underneath `srcFolder` will be preserved for the copy into `destFolder`.
    If false, the files are copied directly under destFolder.
    :return: The list of copied files relative to the `destFolder`.
    '''
    output = []

    groups = findSharedObjectGroups(pattern, srcFolder)

    for group in groups:
        for file in groups:
            srcFile = os.path.join(srcFolder, file)

            if keepPath:
                destFile = file
            else:
                destFile = os.path.basename(file)

            output.append(destFile)

            destFile = os.path.join(destFolder, destFile)

            parentFolder = os.path.dirname(destFile)
            if parentFolder != None and len(parentFolder) > 0:
                os.makedirs(parentFolder, exist_ok=True)

            shutil.copy2(srcFile, destFile, follow_symlinks=False)

    return output

def copytree(srcFolder:str, destFolder:str, includeSubfolders:bool=True, onlyNewerSources:bool=True, ignoreFolders:set=None):
    '''
    Copy elements under `srcFolder` to under `destFolder`.
    :param srcFolder: The source folder.
    :param destFolder:  The destination folder.
    :param includeSubfolders:  If true, subfolders are also copied (with full contents).
    :param onlyNewerSources:  If true, a file is only copied if it does not exist at the destination location, or if the
    file at the destination location is older than the file to be copied.
    :return: None
    '''

    if not os.path.isdir(srcFolder):
        raise Exception("The source folder is not valid.")

    os.makedirs(destFolder, exist_ok=True)

    for item in os.listdir(srcFolder):
        src = os.path.join(srcFolder, item)
        dest = os.path.join(destFolder, item)
        if os.path.isdir(src):
            if includeSubfolders and (ignoreFolders == None or not (item in ignoreFolders)):
                copytree(src, dest)
        else:
            doCopy = True
            if onlyNewerSources and os.path.isfile(dest):
                doCopy = os.path.getmtime(src) > os.path.getmtime(dest)
            if doCopy:
                shutil.copy2(src, dest)

def findFiles(pattern:str, folder:str, recursive:bool=True, prefix=None) -> list:
    '''
    Find a file from the given folder having the given pattern.
    :param pattern: The pattern to find.  See the python function: `fnmatch.fnmatch`
    :param folder: The folder inside which to search.  Results will be relative to this folder.
    :param recursive:  If true, sub-folders are searched.
    :param prefix: The superordinate path that is joined (prepended) to each element of the output.
    :return: The list of files discovered.
    '''
    output = []

    for item in os.listdir(folder):
        path = os.path.join(folder, item)
        if os.path.isfile(path):
            if fnmatch.fnmatch(item, pattern):
                if prefix == None:
                    output.append(item)
                else:
                    output.append(os.path.join(prefix, item))
        elif os.path.isdir(path) and recursive:
            subPrefix = item
            if prefix != None:
                subPrefix = os.path.join(prefix, subPrefix)

            output += findFiles(pattern, path, recursive=True, prefix=subPrefix)

    return output

def findSharedObjectGroups(pattern:str, folder:str, recursive:bool=True, prefix=None) -> list:
    '''
    Find a set of shared objects from the given folder having the given pattern.

    Each *.so file can have multiple companions with a version number appended after the `.so` suffix.  The companions
    can be files or links to files.  For example:
        libwhatever.so
        libwhatever.so.0  [symlink --> libwhatever.so.0.1234.0]
        libwhatever.so.0.1234.0
        libwhatever.so.1  [symlink --> libwhatever.so.1.4321.0]
        libwhatever.so.1.4321.0

    The companions of each *.so file are grouped such that the members of each group share a common character sequence
    prior to ".so".

    This method finds any filename whose prefix (before the `.so`) match the given pattern.  For each pattern, the `*.so`
    file is copied with all of it's companions.

    :param pattern: The wildcard filename pattern for the prefix of the file (before the `.so`).  This should not include
    the `.so` or anything that comes after.  See the python function `fnmatch.fnmatch` for information on wildcards.
    :param folder: The folder inside which to search.  Results will be relative to this folder.
    :param recursive:  If true, sub-folders are searched.
    :param prefix: The superordinate path that is joined (prepended) to each element of the output.
    :return: The list of lists.  Each inner list represents a single set of *.so files.
    '''
    output = []

    pattern0 = pattern + ".so"
    pattern1 = pattern + ".so.*"

    rePattern = re.compile('.+\.so\.[0-9\.]*\d+$')

    files = []

    for item in os.listdir(folder):
        path = os.path.join(folder, item)
        if os.path.isfile(path):
            if fnmatch.fnmatch(item, pattern0) \
                    or (fnmatch.fnmatch(item, pattern1) and (None != rePattern.fullmatch(item))):
                files.append(item)
        elif os.path.isdir(path) and recursive:
            subPrefix = item
            if prefix != None:
                subPrefix = os.path.join(prefix, subPrefix)

            output += findSharedObjectGroups(pattern, path, recursive=True, prefix=subPrefix)

    if len(files) > 0:
        files.sort()
        fileGroups = groupSoFiles(files)
        if prefix != None:
            for i, fileSet in enumerate(fileGroups):
                for j, file in enumerate(fileSet):
                    fileSet[j] = os.path.join(prefix, file)
                # FIXME: I don't know enough about Python to know whether this line is necessary:
                fileGroups[i] = fileSet
        output += fileGroups

    return output

def groupSoFiles(sortedList:list) -> list:
    '''
    Groups a list of *.so files into sets.

    Each *.so file can have multiple companions with a version number appended after the `.so` suffix.  The companions
    can be files or links to files.  For example:
        libwhatever.so    [symlink --> libwhatever.so.0]
        libwhatever.so.0  [symlink --> libwhatever.so.0.1234.0]
        libwhatever.so.0.1234.0
        libwhatever.so.1  [symlink --> libwhatever.so.1.4321.0]
        libwhatever.so.1.4321.0

    The companions of each *.so file are grouped such that the members of each group share a common character sequence
    prior to ".so".

    :param sortedList:  A list of filenames which has been sorted alphabetically.
    :return: A list of lists.  Each inner list is a single grouping of *.so files.
    '''

    output = []
    thisGroup = []
    thisPrefix = None

    for item in sortedList:
        if thisPrefix == None:
            idx = item.find(".so")
            thisPrefix = item[:idx]
            thisGroup = [item]
        elif item.startswith(thisPrefix):
            thisGroup.append(item)
        else:
            output.append(thisGroup)
            idx = item.find(".so")
            thisPrefix = item[:idx]
            thisGroup = [item]

    if len(thisGroup) > 0:
        output.append(thisGroup)

    return output