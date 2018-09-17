from conans import ConanFile

import os
import sys

# ----------------
# Import the gst_conan package
# ----------------
# When loaded via gst-conan, the GST_CONAN_FOLDER variable gives the location of the `gst_conan` package.
# Otherwise, when loaded from within the `exports` folder, the `gst_conan` package is next to conanfile.py
gstConanParentFolder = os.getenv("GST_CONAN_FOLDER", os.path.dirname(__file__))
sys.path.insert(0, os.path.dirname(gstConanParentFolder))
import gst_conan

# ----------------
# Implement the ConanFile
# ----------------
class GstRtspServerConan(ConanFile):
    name = "gst-rtsp-server"
    license = "?"
    url = "https://github.com/gstreamer/gst-rtsp-server"
    description = "A Gstreamer library for building an RTSP server."
    settings = "os", "compiler", "build_type", "arch"
    options = \
    {   "shared": [True, False], \
        "meson_buildtype": gst_conan.build.mesonBuildTypes()\
    }
    default_options = "shared=False", "meson_buildtype=debug"
    generators = "pkg_config"

    def __init__(self, output, runner, user, channel):
        ConanFile.__init__(self, output, runner, user, channel)

        self.binFiles = []
        self.libFiles = []
        self.pcFiles = []

        # These environment variables only exist when the package is created with gst-conan
        self.repoFolder = os.getenv('GST_BUILD_REPO_FOLDER', None)
        self.outputFolder = os.getenv('GST_BUILD_OUTPUT_FOLDER', None)

        if self.repoFolder:
            self.repoFolder = os.path.join(self.repoFolder, "subprojects", self.name)

        if self.outputFolder:
            self.outputFolder = os.path.join(self.outputFolder, "subprojects", self.name)

    def build(self):
        # FIXME:  We are building the project separately, in violation of best practices for Conan.

        # This is how we would follow best practices for Conan.  Unfortunately this does not work because the current
        # Meson project takes dependencies from the parent project (gst-build).
        #
        # from conans import Meson
        # meson = Meson(self)
        # meson.configure(source_folder=self.name, build_folder="build")
        # meson.build()

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

        # copy gst_conan to `export` folder
        exportFolder = os.path.join(os.path.dirname(os.path.dirname(self.build_folder)), "export")
        srcFolder = os.path.join(gstConanParentFolder, "gst_conan")
        destFolder = os.path.join(exportFolder, "gst_conan")
        gst_conan.base.copytree(srcFolder=srcFolder, destFolder=destFolder)

    def package_info(self):
        self.cpp_info.includedirs = ["include"]
        self.cpp_info.libs = gst_conan.base.basenames(self.libFiles)

        self.cpp_info.libdirs = ["lib"]
        self.cpp_info.bindirs = ["bin"]

    def requirements(self):
        self.requires(f"gstreamer/{self.version}@{os.environ['GST_CONAN_USER']}/{os.environ['GST_CONAN_CHANNEL']}")

    def source(self):
        # WARNING:  Conan will be unable to build from sources with the current recipe.  But we provide the sources anyway.

        # We could pull down the sources like this.
        # self.run(f"git clone --recurse-submodules https://github.com/gstreamer/{self.name}.git -b {os.environ['GST_CONAN_REVISION']}")
        # self.run(f"cd {self.name}")

        # However we have already used gst-build to pull down the sources, so this is faster.
        if self.repoFolder != None:
            gst_conan.base.copytree(srcFolder=self.repoFolder, destFolder=self.source_folder)