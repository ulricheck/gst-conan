from . import base

import os
import subprocess

def create(packagesFolder:str, revision:str, version:str, user:str, channel:str, extraArgs:list) -> None:
    '''
    Wraps the execution of `conan create` for all packages.  Throws on error.
    :param packagesFolder:  The folder which contains the conanfiles for all packages.
    :param revision: The revision to pull from all Gstreamer repos.  This can be a branch name, a sha, or a tag.
    :param version: The version of Gstreamer being packaged, and part of the conan package id.
    :param user: The user which is part of the conan package id.
    :param channel: The channel which is part of the conan package id.
    :param extraArgs:  A list of extra arguments to be passed to conan over the command line.
    :return: Nothing.
    '''

    # The list of packages in order of when they should be created.
    packageList = ["gstreamer", "gst-plugins-base", "gst-plugins-good"]

    xargs = ""
    if extraArgs != None or len(extraArgs) > 0:
        xargs = subprocess.list2cmdline(extraArgs)

    env = os.environ.copy()
    env['GST_CONAN_REVISION'] = revision
    env['GST_CONAN_VERSION'] = version
    env['GST_CONAN_USER'] = user
    env['GST_CONAN_CHANNEL'] = channel

    for package in packageList:
        packageFolder = os.path.join(packagesFolder, package)
        cmd = f"conan create {packageFolder} {user}/{channel} {xargs}"
        base.execute(cmd, env=env)