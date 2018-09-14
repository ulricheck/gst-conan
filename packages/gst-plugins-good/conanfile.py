from conans import ConanFile, Meson, tools

import os

class GstPluginsGoodConan(ConanFile):
    name = "gst-plugins-good"
    version = f"{os.environ['GST_CONAN_VERSION']}"
    license = "LGPL"
    url = "https://github.com/gstreamer/gst-plugins-good"
    description = "Good Gstreamer plugins and helper libraries."
    settings = "os", "compiler", "build_type", "arch"
    options = \
    {   "shared": [True, False]
    }
    default_options = "shared=False"
    generators = "pkg_config"

    def source(self):
        self.run(f"git clone --recurse-submodules https://github.com/gstreamer/{self.name}.git -b {os.environ['GST_CONAN_REVISION']}")
        self.run(f"cd {self.name}")

    def build(self):
        meson = Meson(self)
        meson.configure(source_folder=self.name, build_folder="build")
        meson.build()

    def package(self):
        # include
        self.copy("*.h", dst="include/gst", src="gst")

        # bin
        self.copy("*.dll", dst="bin", keep_path=False)
        self.copy("*.so", dst="bin", keep_path=False)

        # lib
        self.copy("*.lib", dst="lib", keep_path=False)
        self.copy("*.dylib", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)

        # pc
        self.copy("*.pc", dst="pc", keep_path=False, excludes="*-uninstalled.pc")

    def package_info(self):
        self.cpp_info.includedirs = ["include"]
        self.cpp_info.libs = []
        self.cpp_info.libdirs = ["lib"]
        self.cpp_info.bindirs = ["bin"]

    def requirements(self):
        self.requires(f"gstreamer/{self.version}@{os.environ['GST_CONAN_USER']}/{os.environ['GST_CONAN_CHANNEL']}")
        self.requires(f"gst-plugins-base/{self.version}@{os.environ['GST_CONAN_USER']}/{os.environ['GST_CONAN_CHANNEL']}")