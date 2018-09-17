from . import base
from . import build

import os
import shutil
import subprocess

def clean() -> None:
    buildFolder = os.path.join(base.messFolder(), "gst-build-output")
    shutil.rmtree(buildFolder)

def create(packagesFolder:str, revision:str, version:str, buildtype:str, user:str, channel:str, extraArgs:list) -> None:
    '''
    Wraps the execution of `conan create` for all packages.  Throws on error.
    :param packagesFolder:  The folder which contains the conanfiles for all packages.
    :param revision: The revision to pull from all Gstreamer repos.  This can be a branch name, a sha, or a tag.
    :param version: The version of Gstreamer being packaged, and part of the conan package id.
    :param buildtype:  The meson build type.  The value passed to meson after the `--buildtype` flag.
    :param user: The user which is part of the conan package id.
    :param channel: The channel which is part of the conan package id.
    :param extraArgs:  A list of extra arguments to be passed to conan over the command line.
    :return: Nothing.
    '''

    # The list of packages in order of when they should be created.
    packageList = \
    [   "gstreamer",\
        "gst-plugins-base",\
        "gst-plugins-good", \
        "gst-plugins-bad",\
        "gst-plugins-ugly",\
        "gst-editing-services", \
        "gst-rtsp-server", \
        "gst-libav" \
    ]

    # Checkout the relevant revision of gst-build, then build it
    gstBuildFolder = os.path.join(base.messFolder(), "gst-build")
    buildFolder    = os.path.join(base.messFolder(), "gst-build-output")
    build.checkout(gstBuildFolder, revision)
    build.build(gstBuildFolder, buildFolder)

    # Extra args to be appended to the end of the `conan create ` command
    xargs = ""
    if extraArgs != None or len(extraArgs) > 0:
        xargs = subprocess.list2cmdline(extraArgs)

    env = os.environ.copy()
    env['GST_BUILD_REPO_FOLDER'] = gstBuildFolder
    env['GST_BUILD_OUTPUT_FOLDER'] = buildFolder
    env['GST_CONAN_FOLDER'] = base.gstConanFolder()
    env['GST_CONAN_VERSION'] = version
    env['GST_CONAN_USER'] = user
    env['GST_CONAN_CHANNEL'] = channel

    for package in packageList:
        packageFolder = os.path.join(packagesFolder, package)
        cmd = f"conan create {packageFolder} {package}/{version}@{user}/{channel} -s build_type=None -o meson_buildtype={buildtype} {xargs}"
        base.execute(cmd, env=env)