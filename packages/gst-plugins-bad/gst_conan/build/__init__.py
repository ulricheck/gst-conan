from   collections import OrderedDict as odict
from   conans import ConanFile
import fnmatch
import glob
import os
import re
import shutil
import sys
import traceback

from .PkgConfigFile import PkgConfigFile

from .. import base
from .. import configuration

def conanBuildTypes() -> list:
    '''
    These are the conan build types that we allow.
    :return: The list of types allowed.
    '''
    return ["Debug", "Release"]

def conanVersion() -> str:
    # Here we don't use conans.__version__ because the library version may be different than the version on the path.
    spew = base.evaluate("conan --version")
    idx = spew.rfind(" ")+1
    output = spew[idx:]
    return output

def conanStorageFolder() -> str:
    return base.evaluate("conan config get storage.path")

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

def dockerfileChoices() -> list:
    '''
    The list of choices for docker containers which can be used to build the conan packages.  This is basically
    the list of folders under `gst-conan/dockers` (where each folder contains a dockerfile).
    :return:
    '''
    dockersFolder = base.gstConanDockersFolder()

    output = list(set(glob.glob(dockersFolder + "/*/Dockerfile")))
    for i, dockerfile in enumerate(output):
        output[i] = os.path.basename(os.path.dirname(dockerfile))

    output.sort()

    return output

def doConanPackage(conanfile:ConanFile, packageInfo:configuration.PackageInfo, buildOutputFolder:str) -> None:
    '''
    This is typically called from the conanfile during from the `package` function.  This method executes most of the
    logic around copying build output, but it does not copy header files.  The caller must do that.
    :param conanfile: The conanfile at the time whent the `package` function is being called.
    :param packageInfo: The package information.
    :param buildOutputFolder: The folder where build output can be found.
    :return: Nothing.
    '''

    try:
        #if conanfile.settings.os == "Windows":
        #    extExe = ".exe"
        #    extLib = ".lib"
        #    extSo = ".dll"
        #elif conanfile.settings.os == "Linux":
        #    extExe = ""
        #    extLib = ".a"
        #    extSo = ".so"
        #else:
        #    raise Exception("Unsupported OS: " + str(conanfile.settings.os))
        extExe = ""
        extLib = ".a"
        extSo = ".so"

        # Copy executables to 'bin' folder
        for exe in packageInfo.executables:
            copyOneFile(f"{exe}{extExe}",
                        srcFolder=buildOutputFolder,
                        destFolder=os.path.join(conanfile.package_folder, "bin"),
                        keepPath=False)

        # Copy static libs to 'lib' folder
        for lib in packageInfo.staticlibs:
            copyOneFile(f"{lib}{extLib}",
                        srcFolder=buildOutputFolder,
                        destFolder=os.path.join(conanfile.package_folder, "lib"),
                        keepPath=False)

        # Copy plugins to 'plugins' folder
        if packageInfo.plugins:
            for pluginName, pluginInfo in packageInfo.plugins.items():
                if pluginInfo.get("optional"):
                    doPlugin = eval(f"conanfile.options.{pluginName}")
                else:
                    doPlugin = True

                if doPlugin:
                    lib = pluginInfo.get("lib")
                    if lib:
                        lib = f"{lib}"
                    else:
                        lib = f"libgst{pluginName}"

                    destFolder = os.path.join(conanfile.package_folder, "plugins")

                    try:
                        if conanfile.settings.os == "Linux":
                            copyOneSharedObjectFileGroup(lib, buildOutputFolder, destFolder, keepPath=False)
                        else:
                            copyOneFile(f"{lib}{extSo}", buildOutputFolder, destFolder, keepPath=False)
                    except Exception:
                        conanfile.output.error(f"Failed to find the file {lib}{extSo}.")
                        conanfile.output.error(f"You may need to install some packages on your machine.")
                        conanfile.output.error(f"Look for machine setup instructions:  https://github.com/Panopto/gst-conan")
                        innerException = sys.exc_info()[0]
                        raise Exception(f"Failed to find the file {lib}{extSo}.") from innerException

        # Start a list of sharedlibs to be copied.
        if packageInfo.sharedlibs:
            sharedlibs = packageInfo.sharedlibs.copy()
        else:
            sharedlibs = []

        # Run through pkg-config files
        if packageInfo.pkgconfigs:
            srcPcFolder = os.path.join(buildOutputFolder, "pkgconfig")
            destGirFolder = os.path.join(conanfile.package_folder, "data", "gir-1.0")
            destPcFolder = os.path.join(conanfile.package_folder, "pc-installed")
            destTypelibFolder = os.path.join(conanfile.package_folder, "lib", "girepository-1.0")

            os.makedirs(destPcFolder)

            for pcName, pcInfo in packageInfo.pkgconfigs.items():
                lib = pcInfo.get("lib")
                if lib != None:
                    sharedlibs.append(lib)

                gir = pcInfo.get("gir")
                if gir != None:
                    copyOneFile(f"{gir}.gir", buildOutputFolder, destGirFolder, keepPath=False)
                    copyOneFile(f"{gir}.typelib", buildOutputFolder, destTypelibFolder, keepPath=False)

                # Copy the original pkg-config file
                shutil.copy2(src=os.path.join( srcPcFolder, f"{pcName}.pc"),
                             dst=os.path.join(destPcFolder, f"{pcName}.pc"))

                # Load the pkg-config file, modify, and save
                pcFile = PkgConfigFile()
                pcFile.load(os.path.join(srcPcFolder, f"{pcName}.pc"))

                pcFile.variables["prefix"] = conanfile.package_folder
                pcFile.variables["exec_prefix"] = "${prefix}"
                pcFile.variables["libdir"] = "${prefix}/lib"
                pcFile.variables["includedir"] = "${prefix}/include"

                if pcFile.variables.get("pluginsdir"):
                    pcFile.variables["pluginsdir"] = "${prefix}/plugins"

                if pcFile.variables.get("toolsdir"):
                    pcFile.variables["toolsdir"] = "${prefix}/bin"

                if pcFile.variables.get("datarootdir"):
                    pcFile.variables["datarootdir"] = "${prefix}/data"

                if pcFile.variables.get("datadir"):
                    pcFile.variables["datadir"] = "${prefix}/data"

                if pcFile.variables.get("girdir"):
                    pcFile.variables["girdir"] = "${prefix}/data/gir-1.0"

                if pcFile.variables.get("typelibdir"):
                    pcFile.variables["typelibdir"] = "${libdir}/girepository-1.0"

                # This is where conan's cmake generator expects the *.pc files to be.
                pcFile.save(os.path.join(conanfile.package_folder, f"{pcName}.pc"))

        # Copy shared libs to 'lib' folder
        for lib in sharedlibs:
            if conanfile.settings.os == "Linux":
                copyOneSharedObjectFileGroup(lib,
                                             srcFolder=buildOutputFolder,
                                             destFolder=os.path.join(conanfile.package_folder, "lib"),
                                             keepPath=False)
            else:
                copyOneFile(f"{lib}{extSo}",
                            srcFolder=buildOutputFolder,
                            destFolder=os.path.join(conanfile.package_folder, "lib"),
                            keepPath=False)
    except:
        conanfile.output.error(traceback.format_exc())
        raise

def doConanPackageInfo(conanfile:ConanFile, packageInfo:configuration.PackageInfo) -> None:
    '''
    This is typically called from the conanfile during from the `package_info` function.  This method executes
    all of the logic around attaching user_info and cpp_info to the conan package.
    :param conanfile: The conanfile at the time whent the `package_info` function is being called.
    :param packageInfo: The package information.
    :param buildOutputFolder: The folder where build output can be found.
    :return: Nothing.
    '''

    try:
        conanfile.cpp_info.bindirs = ["bin"]
        conanfile.cpp_info.includedirs = ["include"]
        conanfile.cpp_info.libdirs = ["lib"]

        #if conanfile.settings.os == "Windows":
        #    extSo = ".dll"
        #    extLib = ".lib"
        #elif conanfile.settings.os == "Linux":
        #    extSo = ".so"
        #    extLib = ".a"
        #else:
        #    raise Exception(f"Unsupported OS: {conanfile.settings.os}")
        extSo = ".so"
        extLib = ".a"

        conanfile.cpp_info.libs = []

        for pcName, pcInfo in packageInfo.pkgconfigs.items():
            lib = pcInfo.get("lib")
            if lib != None:
                conanfile.cpp_info.libs.append(f"{lib}{extSo}")

        for lib in packageInfo.sharedlibs:
            conanfile.cpp_info.libs.append(f"{lib}{extSo}")

        for lib in packageInfo.staticlibs:
            conanfile.cpp_info.libs.append(f"{lib}{extLib}")

        if packageInfo.plugins and len(packageInfo.plugins) > 0:
            conanfile.user_info.plugins = os.path.join(conanfile.cpp_info.rootpath, "plugins")

    except:
        conanfile.output.error(traceback.format_exc())
        raise

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

def mesonBuildTypes() -> list:
    return ["plain", "debug", "debugoptimized", "release"]