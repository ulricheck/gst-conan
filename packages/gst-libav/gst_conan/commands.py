from . import base
from . import build
from . import configuration

import os
import shlex
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

def createWithDocker(dockerRecipeId:str, createArgs:str) -> None:
    '''
    Implements `conan create` when the "--docker" flag is specified.
    :param dockerRecipeId: Identifies the docker image (and container) to be used.  Specifically this is the name of a
    folder under `gst-conan/distros` to be used for building.
    :param createArgs: The command-line arguments that are to be forwarded to the docker container.  This includes
    the 'create' verb and everything that comes after it, but it does not include the "--docker xxx" part.
    :return: Nothing.
    '''

    if 0 != base.execute("docker --version", throwable=False):
        raise Exception("Docker is not installed.")

    config = configuration.getCurrent()

    dockerImageTag = f"gst-conan_{dockerRecipeId}:latest"

    conanStorageFolder = os.path.expanduser(build.conanStorageFolder())

    # ---------------------------------

    print("[BEGIN] Docker build (setting up docker container)")

    base.execute("docker build . "
                     f"--file {base.gstConanDistrosFolder()}/{dockerRecipeId}/Dockerfile "
                     f"--tag {dockerImageTag} "
                     f"--build-arg CONAN_STORAGE_PATH={conanStorageFolder} "
                     f"--build-arg CONAN_VERSION={build.conanVersion()} ",
                 workingFolder=base.gstConanFolder())

    print("[END] Docker build (setting up docker container)")

    # ---------------------------------

    print("[BEGIN] Docker run (building conan packages)")
    gstConanCmd = "gst-conan " + createArgs
    print("    " + gstConanCmd)

    os.makedirs(conanStorageFolder, exist_ok=True)

    base.execute(
        f"docker run --runtime=nvidia --mount type=bind,src={conanStorageFolder},dst={conanStorageFolder} {dockerImageTag} " \
            + shlex.quote(gstConanCmd) )

    print("[END] Docker run (building conan packages)")

def createWithoutDocker(packagesFolder:str, revision:str, version:str,
                        build_type:str, user:str, channel:str, extraArgs:list) -> None:
    '''
    Implements `conan create` for all packages when the command is used without the "--docker" flag.
    Throws on error.
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

def setup(distro:str) -> None:
    '''
    Installs runtime dependendencies on the target machine.
    :param distro:  The distro on which dependencies are to be installed.
    :return: Returns nothing, but throws an exception if problems occur.
    '''

    if not base.currentUserIsPrivileged():
        base.raiseError("Root privileges are required.")

    distroFolder = os.path.join(base.gstConanDistrosFolder(), distro)

    if not os.path.isdir(distroFolder):
        base.raiseError(f"A folder does not exist for distro {distro}:  " + distroFolder)

    debiansFile = os.path.join(distroFolder, "debians-run.txt")
    if os.path.isfile(debiansFile):
        base.execute("apt-get update")
        debiansList = base.readNonEmptyLines(debiansFile)
        debiansStr = ' '.join(debiansList)
        env = os.environ.copy()
        env["DEBIAN_FRONTEND"] = "noninteractive"
        base.execute("apt-get install --yes " + debiansStr, env=env)