from conans import ConanFile, Meson

import os
import shutil
import sys
if sys.version_info[0] < 3:
    raise Exception("The version of Python must be 3 or greater.")

# ----------------
# Import helper methods under gst_conan
# ----------------
sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)))
import gst_conan

# ----------------
# Implement the ConanFile
# ----------------
class GstEditingServicesConan(ConanFile):
    name = "gst-editing-services"
    license = "LGPL"
    url = ["https://github.com/Panopto/gst-conan", "https://github.com/gstreamer/gst-editing-services"]
    description = "A base layer of code for GStreamer plugins with helper libraries"
    settings = {
        "os": ["Linux"],
        "compiler": None,
        "build_type": None,
        "arch": None
    }
    options = {}
    default_options = None

    # It would be nice to export like this ...

    #   exports = "../../gst_conan/*", "../../config/*"
    #
    # ... but it doesn't work.  Soft links don't work either.  See https://github.com/conan-io/conan/issues/3591.
    #
    # So these folders have been copied multiple times within the repo.
    exports = "gst_conan/*", "config/*"

    def build(self):
        pcPaths = [
            self.deps_cpp_info["gstreamer"].rootpath,
            self.deps_cpp_info["gst-plugins-base"].rootpath,
            self.deps_cpp_info["gst-plugins-bad"].rootpath,
            self.deps_cpp_info["gst-plugins-good"].rootpath
        ]

        meson = Meson(self)
        meson.configure(source_folder=self.name, build_folder="build", pkg_config_paths=pcPaths)
        meson.build()

    def build_requirements(self):
        self.build_requires(f"gst-plugins-bad/{self.version}@{self.user}/{self.channel}")
        self.build_requires(f"gst-plugins-good/{self.version}@{self.user}/{self.channel}")

    def configure(self):
        # Environment variables that only exist when `conan` is called through gst-conan
        self.gstRevision = os.getenv("GST_CONAN_REVISION", self.version)

        # Load configuration info.
        self.config = gst_conan.configuration.getCurrent()
        self.packageInfo = self.config.packages[self.name]

    def package(self):

        # package include files
        self.copy("*.h", dst="include/ges", src=f"{self.name}/ges")
        self.copy("*.h", dst="include/ges", src="build/ges")

        # package the rest
        buildOutputFolder = os.path.join(self.build_folder, "build")
        gst_conan.build.doConanPackage(self, self.packageInfo, buildOutputFolder)

    def package_info(self):
        gst_conan.build.doConanPackageInfo(self, self.packageInfo)

    def requirements(self):
        self.requires(f"gstreamer/{self.version}@{self.user}/{self.channel}")
        self.requires(f"gst-plugins-base/{self.version}@{self.user}/{self.channel}")

    def source(self):
        # This is what actually belongs here.
        self.run(f"git clone --recurse-submodules https://github.com/gstreamer/{self.name}.git -b {self.gstRevision}")
        self.run(f"cd {self.name}")