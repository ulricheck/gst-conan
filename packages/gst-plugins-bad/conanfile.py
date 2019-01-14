from conans import ConanFile, Meson

import os
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
class GstPluginsBadConan(ConanFile):
    name = "gst-plugins-bad"
    license = "LGPL"
    url = ["https://github.com/Panopto/gst-conan", "https://github.com/gstreamer/gst-plugins-bad"]
    description = "Bad Gstreamer plugins and helper libraries."
    settings = {
        "os": ["Linux"],
        "compiler": None,
        "build_type": None,
        "arch": None
    }
    options = {"faac": [False, True],
               "faad": [False, True],
    }
    default_options = (
        "faac=True",
        "faad=True"
    )
    build_policy = "outdated"

    # It would be nice to export like this ...

    #   exports = "../../gst_conan/*", "../../config/*"
    #
    # ... but it doesn't work.  Soft links don't work either.  See https://github.com/conan-io/conan/issues/3591.
    #
    # So these folders have been copied multiple times within the repo.
    exports = "gst_conan/*", "config/*", "patches/*"

    def build(self):
        # ---------------------------
        # Apply patches
        # * 0001-disable-webrtc-example.patch
        #   * fixes https://gitlab.freedesktop.org/gstreamer/gst-plugins-bad/issues/867
        # ---------------------------
        repoFolder = os.path.join(self.build_folder, self.name)
        gst_conan.base.execute("git config user.email gst_conan@panopto.com", workingFolder=repoFolder)
        gst_conan.base.execute("git config user.name  gst_conan", workingFolder=repoFolder)

        patchFolder = os.path.join(self.build_folder, "patches")
        if os.path.isdir(patchFolder):
            for file in os.listdir(patchFolder):
                patchPath = os.path.join(patchFolder, file)
                if file.endswith(".patch") and os.path.isfile(patchPath):
                    self.output.info(f"Applying patch {file}")
                    gst_conan.base.execute(f"git am {patchPath}", workingFolder=repoFolder)

        # ---------------------------
        # Build as usual
        # ---------------------------
        pcPaths = [
            self.deps_cpp_info["gstreamer"].rootpath,
            self.deps_cpp_info["gst-plugins-base"].rootpath
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
        # include files
        self.copy("*.h", dst="include", src=f"{self.name}")

        # package the rest
        buildOutputFolder = os.path.join(self.build_folder, "build")
        gst_conan.build.doConanPackage(self, self.packageInfo, buildOutputFolder)

    def package_info(self):
        gst_conan.build.doConanPackageInfo(self, self.packageInfo)

    def requirements(self):
        self.requires(f"gstreamer/{self.version}@{self.user}/{self.channel}")
        self.requires(f"gst-plugins-base/{self.version}@{self.user}/{self.channel}")

    def source(self):
        # Clone
        self.run(f"git clone --recurse-submodules https://github.com/gstreamer/{self.name}.git -b {self.gstRevision}")
        self.run(f"cd {self.name}")
