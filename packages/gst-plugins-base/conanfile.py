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
class GstPluginsBaseConan(ConanFile):
    name = "gst-plugins-base"
    license = "LGPL"
    url = ["https://github.com/Panopto/gst-conan", "https://github.com/gstreamer/gst-plugins-base"]
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

    @staticmethod
    def applyWorkaround537(pkgConfigFile):
        '''
        # workaround for https://gitlab.freedesktop.org/gstreamer/gst-plugins-base/issues/537
        # There is a problem with the `gstreamer-pbutils-1.0.pc` file
        :param pkgConfigFile: The path to the file to be repaired.
        '''
        pc = gst_conan.build.PkgConfigFile()
        pc.load(pkgConfigFile)

        pc.ensureRequires(["gstreamer-audio-1.0", "gstreamer-base-1.0", "gstreamer-video-1.0", "gstreamer-tag-1.0"])

        #requirements = ["gstreamer-tag-1.0"]
        #for requirement in requirements:
        #    if pc.requiresPrivate == None or len(pc.requiresPrivate) == 0:
        #        pc.requiresPrivate = requirement
        #    elif requirement not in pc.requiresPrivate:
        #        pc.requiresPrivate += (" " + requirement)

        pc.save(pkgConfigFile)

    def build(self):
        pcPaths = [
            self.deps_cpp_info["gstreamer"].rootpath
        ]

        meson = Meson(self)
        meson.configure(source_folder=self.name, build_folder="build", pkg_config_paths=pcPaths)
        meson.build()

    def configure(self):
        # Environment variables that only exist when `conan` is called through gst-conan
        self.gstRevision = os.getenv("GST_CONAN_REVISION", self.version)

        # Load configuration info.
        self.config = gst_conan.configuration.getCurrent()
        self.packageInfo = self.config.packages[self.name]

    def package(self):

        # package include files
        self.copy("*.h", dst="include/gst", src=f"{self.name}/gst")
        self.copy("*.h", dst="include/gst", src=f"{self.name}/gst-libs/gst")
        self.copy("*.h", dst="include/gst", src="build/gst")  # might catch some auto-generated files (I guess)
        self.copy("*.h", dst="include/gst", src="build/gst-libs/gst")  # might catch some auto-generated files (I guess)

        # package the rest
        buildOutputFolder = os.path.join(self.build_folder, "build")
        gst_conan.build.doConanPackage(self, self.packageInfo, buildOutputFolder)

        # workaround for https://gitlab.freedesktop.org/gstreamer/gst-plugins-base/issues/537
        # There is a problem with the `gstreamer-pbutils-1.0.pc` file

        self.__class__.applyWorkaround537(os.path.join(self.package_folder, "gstreamer-pbutils-1.0.pc"))
        self.__class__.applyWorkaround537(os.path.join(self.package_folder, "pc-installed", "gstreamer-pbutils-1.0.pc"))

    def package_info(self):
        gst_conan.build.doConanPackageInfo(self, self.packageInfo)

    def requirements(self):
        self.requires(f"gstreamer/{self.version}@{self.user}/{self.channel}")

    def source(self):
        # This is what actually belongs here.
        self.run(f"git clone --recurse-submodules https://github.com/gstreamer/{self.name}.git -b {self.gstRevision}")
        self.run(f"cd {self.name}")
