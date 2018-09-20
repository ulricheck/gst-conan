#!/usr/bin/python3

import sys
if sys.version_info[0] < 3:
    raise Exception("The version of Python must be 3 or greater.")

import argparse
import gst_conan
import os

def test1():
    pcFile = gst_conan.build.PkgConfigFile()
    pcFile.load(os.path.expanduser("~/Desktop/pc/gstreamer/gstreamer-1.0.pc"))
    pcFile.save(os.path.expanduser("~/Desktop/pc/gstreamer/not-gstreamer-1.0.pc"))

def test2():
    pluginFolder = os.path.expanduser("~/Desktop/build-gstreamer/build/plugins")
    fname = "libgstcoreelements.so"
    found = gst_conan.base.findFiles(pluginFolder, fname)
    print(found)

def test3():
    fname = "libgstcoreelements.so"
    srcFolder = "/home/ding/.conan/data/gstreamer/1.14.2/ding/unstable/build/69f10d1e6d78c1962fbe8fb80440f32b1fdf8423/build/plugins"
    destFolder = "/home/ding/.conan/data/gstreamer/1.14.2/ding/unstable/package/69f10d1e6d78c1962fbe8fb80440f32b1fdf8423/lib/plugins"

    gst_conan.base.copyOneFile(fname, srcFolder, destFolder, keepPath=False)

def test4():
    fnames = [
        "z.so",
        "z.so.0",
        "z.so.1",
        "liba.so",
        "liba.so.0",
        "liba.so.0.123",
        "liba.so.1",
        "liba.so.1.456.789",
        "libb.so",
        "libb.so.0",
        "libb.so.0.123",
        "libb.so.7559",
        "libc.so",
        "libc.so.0",
        "libc.so.0.123",
        "libd.so"
    ]

    fnames.sort()
    groups = gst_conan.base.groupSoFiles(fnames)

    print(groups)

def test5():
    pluginName = "libgstcoreelements"
    srcPluginFolder = "/home/ding/.conan/data/gstreamer/1.14.2/ding/unstable/build/69f10d1e6d78c1962fbe8fb80440f32b1fdf8423/build/plugins"
    destPluginFolder = "/home/ding/.conan/data/gstreamer/1.14.2/ding/unstable/package/69f10d1e6d78c1962fbe8fb80440f32b1fdf8423/lib/plugins"
    print(gst_conan.base.copyOneSharedObjectFileGroup(pluginName, srcPluginFolder, destPluginFolder, keepPath=False))

def test6():
    libName = "libgstreamer-1.0"
    buildFolder = "/home/ding/.conan/data/gstreamer/1.14.2/ding/unstable/build/69f10d1e6d78c1962fbe8fb80440f32b1fdf8423/build"
    destLibFolder = "/home/ding/.conan/data/gstreamer/1.14.2/ding/unstable/package/69f10d1e6d78c1962fbe8fb80440f32b1fdf8423/lib"
    gst_conan.base.copyOneSharedObjectFileGroup(libName, buildFolder, destLibFolder, keepPath=False)

def test7():
    text='gst/gst@@gstreamer-1.0@sha/libgstreamer-1.0.so.0.1402.0.symbols'

    import re
    rePattern = re.compile('.+\.so\.[0-9\.]*\d+$')
    print(rePattern.fullmatch(text))

if '__main__' == __name__:
    test7()