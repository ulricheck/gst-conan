from conans import ConanFile, Meson

import os
import shutil
import sys

# ----------------
# Import helper methods under gst_conanfile
# ----------------
sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)))
import gst_conanfile

# ----------------
# Implement the ConanFile
# ----------------
class GstreamerConan(ConanFile):
    name = "gstreamer"
    license = "LGPL"
    url = "https://github.com/gstreamer/gstreamer"
    description = "GStreamer open-source multimedia framework core library"
    settings = "os", "compiler", "build_type", "arch"
    options = {}
    default_options = None

    # We are supposed to be able to export the gst_conan package as follows, but it doesn't seem to work.
    # Soft links don't work either.  See https://github.com/conan-io/conan/issues/3591.
    #exports = "../../gst_conan"

    exports = "gst_conanfile/*"

    def __init__(self, output, runner, user, channel):
        ConanFile.__init__(self, output, runner, user, channel)

        #  The names of executable files without any possible file extension
        self.execNames =[
            "gst-inspect-1.0",
            "gst-launch-1.0",
            "gst-stats-1.0",
            "gst-typefind-1.0",
            "gst-plugin-scanner"
        ]

        #  The key is the names of the pkgconfig files (without the *.pc extension)
        #  The value is an object with multiple fields.
        #      value.lib = the name of the shared library file (without the *.so or *.dll extension)
        #      value.gir = the name of the *.gir and *.typelib files (without the extension)
        self.pcMap = {
            "gstreamer-1.0" : {
                "lib" : "libgstreamer-1.0",
                "gir" : "Gst-1.0"
            },
            "gstreamer-base-1.0" : {
                "lib" : "libgstbase-1.0",
                "gir" : "GstBase-1.0"
            },
            "gstreamer-check-1.0" : {
                "lib" : "libgstcheck-1.0",
                "gir" : "GstCheck-1.0"
            },
            "gstreamer-controller-1.0" : {
                "lib" : "libgstcontroller-1.0",
                "gir" : "GstController-1.0"
            },
            "gstreamer-net-1.0" : {
                "lib" : "libgstnet-1.0",
                "gir" : "GstNet-1.0"
            }
        }

        # The names of the plugin files (without the *.so or *.dll extension)
        self.pluginNames = [
            "libgstcoreelements",
            "libgstcoretracers"
        ]

        # The names of the static library files (without the *.a or *.lib extension)
        self.staticLibNames = [
            "libcheck",
            "libgstprintf"
        ]

        # Environment variables that only exist when `conan` is called through gst-conan
        self.gstRevision = os.getenv("GST_CONAN_REVISION", self.version)

    def build(self):
        meson = Meson(self)
        meson.configure(source_folder=self.name, build_folder="build")
        meson.build()

    def package(self):
        isLinux = False
        if str(self.settings.os).lower().startswith("win"):
            extExe = ".exe"
            extSo = ".dll"
            extLib = ".lib"
        elif str(self.settings.os).lower().startswith("lin"):
            isLinux = True
            extExe = ""
            extSo = ".so"
            extLib = ".a"
        else:
            raise Exception(f"Unsupported os: {self.settings.os}")

        # this is where the build output goes
        buildFolder = os.path.join(self.build_folder, "build")

        # include files
        self.copy("*.h", dst="include/gst", src=f"{self.name}/gst")
        self.copy("*.h", dst="include/gst", src=f"{self.name}/libs/gst")
        self.copy("*.h", dst="include/gst", src= "build/gst")       # auto-generated files (I guess)
        self.copy("*.h", dst="include/gst", src= "build/libs/gst")  # auto-generated files (I guess)

        # bin folder
        os.makedirs(os.path.join(self.package_folder, "bin"), exist_ok=True)

        # executables go into bin folder
        for execName in self.execNames:
            gst_conanfile.copyOneFile(f"{execName}{extExe}",
                                       srcFolder=buildFolder,
                                       destFolder=os.path.join(self.package_folder, "bin"),
                                       keepPath=False)

        # static libs go into lib folder
        destLibFolder = os.path.join(self.package_folder, "lib")
        for staticLibName in self.staticLibNames:
            gst_conanfile.copyOneFile(f"{staticLibName}{extLib}", buildFolder, destLibFolder, keepPath=False)

        # core plugins go into plugins folder
        srcPluginFolder = os.path.join(buildFolder, "plugins")
        destPluginFolder = os.path.join(self.package_folder, "plugins")
        for pluginName in self.pluginNames:
            if isLinux:
                gst_conanfile.copyOneSharedObjectFileGroup(pluginName, srcPluginFolder, destPluginFolder, keepPath=False)
            else:
                gst_conanfile.copyOneFile(f"{pluginName}{extSo}", srcPluginFolder, destPluginFolder, keepPath=False)

        # pkg-config files and associated files (libs, girs, and typelibs)
        srcPcFolder = os.path.join(buildFolder, "pkgconfig")
        destPcFolder = os.path.join(self.package_folder, "pc-installed")
        os.makedirs(destPcFolder, exist_ok=True)
        destGirFolder = os.path.join(self.package_folder, "data", "gir-1.0")
        destTypelibFolder = os.path.join(self.package_folder, "lib", "girepository-1.0")
        for pcName, otherNames in self.pcMap.items():
            libName = otherNames["lib"]
            girName = otherNames["gir"]

            if None != libName:
                if isLinux:
                    gst_conanfile.copyOneSharedObjectFileGroup(libName, buildFolder, destLibFolder, keepPath=False)
                else:
                    gst_conanfile.copyOneFile(f"{libName}{extSo}", buildFolder, destLibFolder, keepPath=False)

            if None != girName:
                gst_conanfile.copyOneFile(f"{girName}.gir", buildFolder, destGirFolder, keepPath=False)
                gst_conanfile.copyOneFile(f"{girName}.typelib", buildFolder, destTypelibFolder, keepPath=False)

            # Copy the original pkg-config file
            shutil.copy2(src=os.path.join(srcPcFolder, f"{pcName}.pc"), dst=destPcFolder)

            # Load the pkg-config file, modify, and save
            pcFile = gst_conanfile.PkgConfigFile()
            pcFile.load(os.path.join(srcPcFolder, f"{pcName}.pc"))

            pcFile.variables["prefix"] = self.package_folder
            pcFile.variables["exec_prefix"] = "${prefix}"
            pcFile.variables["libdir"] = "${prefix}/lib"
            pcFile.variables["includedir"] = "${prefix}/include"

            if pcName == "gstreamer-1.0":
                pcFile.variables["pluginsdir"] = "${prefix}/plugins"

            if pcName == "gstreamer-plugins-base-1.0" or pcName == "gstreamer-gl-1.0":
                pcFile.variables["pluginsdir"] = "${prefix}/plugins"
            else:
                pcFile.variables["datarootdir"] = "${prefix}/data"
                pcFile.variables["datadir"] = "${datarootdir}"
                pcFile.variables["girdir"] = "${datadir}/gir-1.0"
                pcFile.variables["typelibdir"] = "${libdir}/girepository-1.0"

            # This is where conan's cmake generator expects the *.pc files to be.
            pcFile.save(os.path.join(self.package_folder, f"{pcName}.pc"))

    def package_info(self):
        '''
        I am not sure if this method is necessary since Gstreamer is using pkgconfig.
        '''

        self.cpp_info.bindirs = ["bin"]             # executables
        self.cpp_info.includedirs = ["include"]     # headers
        self.cpp_info.libdirs = ["lib"]             # libs (shared + static)

        if str(self.settings.os).lower().startswith("win"):
            extSo = ".dll"
            extLib = ".lib"
        elif str(self.settings.os).lower().startswith("lin"):
            extSo = ".so"
            extLib = ".a"
        else:
            raise Exception(f"Unsupported os: {self.settings.os}")

        self.cpp_info.libs = []
        for pcName, otherNames in self.pcMap.items():
            libName = otherNames["lib"]
            if None != libName:
                self.cpp_info.libs.append(f"{libName}{extSo}")

        for staticLibName in self.staticLibNames:
            self.cpp_info.libs.append(f"{staticLibName}{extLib}")

    def source(self):
        # This is what actually belongs here.
        self.run(f"git clone --recurse-submodules https://github.com/gstreamer/{self.name}.git -b {self.gstRevision}")
        self.run(f"cd {self.name}")