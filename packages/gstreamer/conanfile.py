from conans import ConanFile, Meson, tools

import os

class GstreamerConan(ConanFile):
    name = "gstreamer"
    version = f"{os.environ['GST_CONAN_VERSION']}"
    license = "LGPL"
    url = f"https://github.com/gstreamer/gstreamer"
    description = "GStreamer open-source multimedia framework core library"
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
        self.cpp_info.libs = [ "libcheck", \
                               "libgstprintf", \
                               "libgstbase-1.0.so", \
                               "libgstcheck-1.0.so", \
                               "libgstcontroller-1.0.so", \
                               "libgstcoreelements.so", \
                               "libgstcoretracers.so", \
                               "libgstnet-1.0.so", \
                               "libgstreamer-1.0.so" ]
        self.cpp_info.libdirs = ["lib"]
        self.cpp_info.bindirs = ["bin"]