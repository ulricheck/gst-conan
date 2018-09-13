from conans import ConanFile, Meson, tools


class GstreamerConan(ConanFile):
    name = "gstreamer"
    version = "1.14.2"
    license = "LGPL"
    url = "https://github.com/gstreamer/gstreamer"
    description = "GStreamer open-source multimedia framework core library"
    settings = "os", "compiler", "build_type", "arch"
    options = \
    {   "shared": [True, False], \
        "revision" : "ANY"
    }
    default_options = "shared=False", "revision=master"
    generators = "pkg_config"

    def source(self):
        self.run("git clone --recurse-submodules https://github.com/gstreamer/gstreamer.git -b " + str(self.options.revision))
        self.run("cd gstreamer")

    def build(self):
        meson = Meson(self)
        meson.configure(source_folder="gstreamer", build_folder="build")
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

    def package_info(self):
        bins = [ "libgstbase-1.0.so", \
                 "libgstcheck-1.0.so", \
                 "libgstcontroller-1.0.so", \
                 "libgstcoreelements.so", \
                 "libgstcoretracers.so", \
                 "libgstnet-1.0.so", \
                 "libgstreamer-1.0.so" ]
        self.cpp_info.includedirs = ["include"]
        self.cpp_info.libs = ["libcheck", "libgstprintf"]
        self.cpp_info.libdirs = ["lib"]
        self.cpp_info.bindirs = ["bin"]

