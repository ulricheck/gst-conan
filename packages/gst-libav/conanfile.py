from conans import ConanFile

import os
import sys

gstConanFolder = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.insert(0, gstConanFolder)
import gst_conan

class GstLibavConan(ConanFile):
    name = "gst-libav"
    version = f"{os.environ['GST_CONAN_VERSION']}"
    license = "LGPL"
    url = "https://github.com/gstreamer/gst-libav"
    description = "A high level library for media composition."
    settings = "os", "compiler", "build_type", "arch"
    options = \
    {   "shared": [True, False], \
        "meson_buildtype": gst_conan.build.mesonBuildTypes()\
    }
    default_options = "shared=False", "meson_buildtype=debug"
    generators = "pkg_config"

    def __init__(self, output, runner, user, channel):
        ConanFile.__init__(self, output, runner, user, channel)
        self.repoFolder = os.path.join(os.environ['GST_BUILD_REPO_FOLDER'], "subprojects", self.name)
        self.outputFolder = os.path.join(os.environ['GST_BUILD_OUTPUT_FOLDER'], "subprojects", self.name)
        self.binFiles = []
        self.libFiles = []
        self.pcFiles = []

    def build(self):
        # We already built it
        pass

    def package(self):
        # include
        self.copy("*.h", dst="include/gst", src=os.path.join(self.repoFolder, "gst"))

        # bin
        self.binFiles = self.copy("*.dll", dst="bin", src=self.outputFolder, keep_path=False)
        self.binFiles = self.binFiles + self.copy("*.so", dst="bin", src=self.outputFolder, keep_path=False)

        # lib
        self.libFiles = self.copy("*.lib", dst="lib", src=self.outputFolder, keep_path=False)
        self.libFiles = self.libFiles + self.copy("*.dylib", dst="lib", src=self.outputFolder, keep_path=False)
        self.libFiles = self.libFiles + self.copy("*.a", dst="lib", src=self.outputFolder, keep_path=False)

        # pc
        self.pcFiles = self.copy("*.pc", dst="pc", src=self.outputFolder, keep_path=False, excludes="*-uninstalled.pc")

    def package_info(self):
        self.cpp_info.includedirs = ["include"]
        self.cpp_info.libs = gst_conan.base.basenames(self.libFiles)

        self.cpp_info.libdirs = ["lib"]
        self.cpp_info.bindirs = ["bin"]

    def requirements(self):
        self.requires(f"gstreamer/{self.version}@{os.environ['GST_CONAN_USER']}/{os.environ['GST_CONAN_CHANNEL']}")
        self.requires(f"gst-plugins-base/{self.version}@{os.environ['GST_CONAN_USER']}/{os.environ['GST_CONAN_CHANNEL']}")

    def source(self):
        # We are building packages without the sources.
        with open("readme.txt", "w") as txt:
            txt.write("No sources are provided because multiple packages must be built together.\n\n" \
                      "To build this package, go to the following repository.\n\n"
                      "https://github.com/Panopto/gst-conan")
            txt.close()