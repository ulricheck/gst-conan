from . import base
from . import build
from . import configuration

import os
import shutil
import subprocess

def copy_exports_workaround() -> None:
    '''
    This command is a temporary bug workaround for https://github.com/conan-io/conan/issues/3591.
    :return:
    '''

    config = configuration.getCurrent()

    srcFolder1 = os.path.join(base.gstConanFolder(), "gst_conan")
    srcFolder2 = os.path.join(base.gstConanFolder(), "config")
    packagesFolder = os.path.join(base.gstConanFolder(), "packages")

    for packageName, packageInfo in config.packages.items():
        destFolder1 = os.path.join(packagesFolder, packageName, "gst_conan")
        destFolder2 = os.path.join(packagesFolder, packageName, "config")

        shutil.rmtree(destFolder1, ignore_errors=True)
        shutil.rmtree(destFolder2, ignore_errors=True)

        shutil.copytree(srcFolder1, destFolder1, symlinks=True)
        shutil.copytree(srcFolder2, destFolder2, symlinks=True)

def create(packagesFolder:str, revision:str, version:str, build_type:str, user:str, channel:str, extraArgs:list) -> None:
    '''
    Wraps the execution of `conan create` for all packages.  Throws on error.
    :param packagesFolder:  The folder which contains the conanfiles for all packages.
    :param revision: The revision to pull from all Gstreamer repos.  This can be a branch name, a sha, or a tag.
    :param version: The version of Gstreamer being packaged, and part of the conan package id.
    :param build_type:  The conan build_type setting ("Debug" or "Release").
    :param user: The user which is part of the conan package id.
    :param channel: The channel which is part of the conan package id.
    :param extraArgs:  A list of extra arguments to be passed to conan over the command line.
    :return: Nothing.
    '''

    config = configuration.getCurrent()

    # Extra args to be appended to the end of the `conan create ` command
    xargs = ""
    if extraArgs != None or len(extraArgs) > 0:
        xargs = subprocess.list2cmdline(extraArgs)

    env = os.environ.copy()
    env['GST_CONAN_REVISION'] = revision

    for packageName, packageInfo in config.packages.items():
        packageFolder = os.path.join(packagesFolder, packageName)
        cmd = f"conan create {packageFolder} {packageName}/{version}@{user}/{channel} -s build_type={build_type} {xargs}"
        base.execute(cmd, env=env)

def setup(optionals:bool) -> None:
    '''
    Sets up the machine to build conan packages
    :param optionals:  If true, install the dependencies for optional plugins.
    :return: Throws an exception if problems occur.
    '''

    if not base.currentUserIsPrivileged():
        base.raiseError("Root privileges are required.")

    #  FIXME:  I wonder if it is possible to install dpkg on a non-debian distro.
    isDebian = (0 == base.execute("dpkg --version &>/dev/null", throwable=False))

    isFedora = -1
    if isDebian:
        isFedora = 0
    else:
        #  We know that `rpm` can be installed on a debian distro, but here we know that we're not running debian.
        isFedora = (0 == base.execute("rpm --version &>/dev/null", throwable=False))

    if isDebian:
        print("Debian-ish distro detected")
        setupDebian(optionals)
    elif isFedora:
        print("Fedora-ish distro detected")
        base.raiseError("Only debian-ish distros are supported right now (FIXME).")
    else:
        base.raiseError("Only debian-ish distros are supported right now (FIXME).")

def setupDebian(optionals:bool) -> None:
    '''
    Sets up the debian machine to build conan packages
    :param optionals:  If true, install the dependencies for optional plugins.
    :return: Throws an exception if problems occur.
    '''

    config = configuration.getCurrent()
    debianPackages = config.debianRequirements(optionals)

    base.execute("apt update")
    base.execute("apt install --yes " + " ".join(debianPackages))

    #   The following pip commands should not be executed as a privileged user (unless that is the user who logged in).
    user = base.evaluate("logname")
    base.execute(f"sudo su - {user} -c 'pip3 install setuptools wheel'")
    base.execute(f"sudo su - {user} -c 'pip3 install --user meson'")
    base.execute(f"sudo su - {user} -c 'pip3 install conan'")

    #   DONE
    print("")
    print("Setup completed successfully")
    print("")
    print("")
    print("-----------------------")
    print("TO DO:  You have 1 manual step to complete.")
    print("-----------------------")
    print("Put the following at the bottom of your '~/.bashrc' file, then `source ~/.bashrc`.")
    print("")
    print("# This is where pip3 installs '--user' executables (such as meson)")
    print("PATH=$PATH:$HOME/.local/bin")
    print("")
    print("")
