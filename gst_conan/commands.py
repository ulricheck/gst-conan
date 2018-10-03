from . import base
from . import build

import os
import shutil
import subprocess

def copy_gst_conanfile() -> None:
    '''
    This command is a temporary bug workaround for https://github.com/conan-io/conan/issues/3591.
    :return:
    '''

    # The list of gstreamer packages
    packageList = build.gstreamerPackageList()

    packagesFolder = os.path.join(base.gstConanFolder(), "packages")
    srcFolder = os.path.join(packagesFolder, "gstreamer", "gst_conanfile")

    for package in packageList:
        if package == "gstreamer":
            continue
        destFolder = os.path.join(packagesFolder, package, "gst_conanfile")

        shutil.rmtree(destFolder, ignore_errors=True)
        shutil.copytree(srcFolder, destFolder, symlinks=True)

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

    # The list of packages in order of when they should be created.
    packageList = build.gstreamerPackageList()

    # Extra args to be appended to the end of the `conan create ` command
    xargs = ""
    if extraArgs != None or len(extraArgs) > 0:
        xargs = subprocess.list2cmdline(extraArgs)

    env = os.environ.copy()
    env['GST_CONAN_REVISION'] = revision

    for package in packageList:
        packageFolder = os.path.join(packagesFolder, package)
        cmd = f"conan create {packageFolder} {package}/{version}@{user}/{channel} -s build_type={build_type} {xargs}"
        base.execute(cmd, env=env)

def setup() -> None:
    '''
    Sets up the machine to build conan packages
    :return: Throws an exception if problems occur.
    '''

    if not base.currentUserIsPrivileged():
        base.raiseError("Root privileges are required.")

    #  FIXME:  I'm assuming this works but I haven't really tried it on a non-Debian distro.
    isDebian = (0 == base.execute("dpkg --version", throwable=False))
    if isDebian:
        print("Debian distro detected")
        setupDebian()
    else:
        base.raiseError("Only debian distros are supported right now (FIXME).")

def setupDebian() -> None:

    debianPackages = [
        "autoconf",
        "automake",
        "autopoint",
        "autotools-dev",
        "bison",
        "build-essential",
        "cmake",
        "curl",
        "debhelper",
        "devscripts",
        "doxygen",
        "dpkg-dev",
        "fakeroot",
        "flex",
        "g++",
        "gettext",
        "git",
        "glib-networking",
        "gperf",
        "gtk-doc-tools",
        "intltool",
        "libasound2-dev",
        "libavfilter-dev",
        "libcurl4-openssl-dev",
        "libdbus-glib-1-dev",
        "libegl1-mesa-dev",
        "libgirepository1.0-dev",
        "libgl1-mesa-dev",
        "libgles2-mesa-dev",
        "libglib2.0-dev",
        "libglu1-mesa-dev",
        "libjpeg-turbo8-dev",
        "libmount-dev",
        "libpulse-dev",
        "libselinux-dev",
        "libtool",
        "libx11-dev",
        "libxcomposite-dev",
        "libxdamage-dev",
        "libxext-dev",
        "libxfixes-dev",
        "libxi-dev",
        "libxml-simple-perl",
        "libxml2-dev",
        "libxrandr-dev",
        "libxrender-dev",
        "libxtst-dev",
        "libxv-dev",
        "make",
        "ninja-build",
        "pkg-config",
        "python-dev",
        "python3-dev",
        "python-pip",
        "python3-pip",
        "texinfo",
        "transfig",
        "wget",
        "x11proto-record-dev",
        "xutils-dev",
        "yasm"
    ]

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
