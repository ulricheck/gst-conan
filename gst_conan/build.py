from . import base

import os
import subprocess

def build(gstBuildFolder:str, buildFolder:str) -> None:
    '''
    Builds gst-build
    :param gstBuildFolder:  The folder to which the gst-build repo has been cloned.
    :param buildFolder:  The folder to which gst-build output is written.
    :return: Nothing.  Throws on error.
    '''

    os.makedirs(buildFolder, exist_ok=True)
    base.execute(f"meson {buildFolder} -Dcustom_subprojects=gst-libav", workingFolder=gstBuildFolder)

    if not buildFolder.endswith('/') and not buildFolder.endswith('\\'):
        buildFolder = buildFolder + '/'

    base.execute(f"ninja -C {buildFolder}", workingFolder=gstBuildFolder)

def checkout(gstBuildFolder:str, revision:str) -> None:
    '''
    Checks out the specified revision of gst-build, clones if necessary.
    :param gstBuildFolder:  The folder to which the gst-build repo is cloned.
    :param revision: The specified revision of gst-build.
    :return: Nothing.  Throws on error.
    '''

    repoUrl = "https://github.com/gstreamer/gst-build.git"

    if os.path.isdir(os.path.join(gstBuildFolder, ".git")):
        # The repo exists, just checkout the relevant branch.
        base.execute("git reset --hard HEAD", workingFolder=gstBuildFolder)
        base.execute(f"git checkout --recurse-submodules {revision}", workingFolder=gstBuildFolder)
    else:
        # The repo does not exist, so clone it.
        os.makedirs(os.path.dirname(gstBuildFolder), exist_ok=True)
        base.execute(f"git clone --recurse-submodules {repoUrl} -b {revision} {gstBuildFolder}")

def mesonBuildTypes() -> list:
    return ["plain", "debug", "debugoptimized", "release"]