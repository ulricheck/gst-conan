from conans import ConanFile, Meson

import os
import shutil
import sys

# ----------------
# Import the gst_conan package
# ----------------
# When loaded via gst-conan, the variable `GST_CONAN_FOLDER` gives the parent folder of the `gst_conan` package.
# Otherwise, the `gst_conan` package is next to `conanfile.py`
gstConanParentFolder = os.getenv("GST_CONAN_FOLDER", os.path.dirname(os.path.realpath(__file__)))
sys.path.insert(0, gstConanParentFolder)
import gst_conan

if gst_conan.DEBUG_MODE:
    import json

# ----------------
# Implement the ConanFile
# ----------------
class GstEditingServicesConan(ConanFile):
    name = "gst-editing-services"
    license = "LGPL"
    url = "https://github.com/gstreamer/gst-editing-services"
    description = "A base layer of code for GStreamer plugins with helper libraries"
    settings = "os", "compiler", "build_type", "arch"
    options = {}
    default_options = None

    # We are supposed to be able to export the gst_conan package as follows, but it doesn't seem to work.
    #exports = "../../gst_conan"

    def __init__(self, output, runner, user, channel):
        ConanFile.__init__(self, output, runner, user, channel)

        #  The names of executable files (without any possible file extension ... would be *.exe on windows)
        self.execNames =[
            "ges-launch-1.0"
        ]

        #  The key is the names of the pkgconfig files (without the *.pc extension)
        #  The value is an object with multiple fields.
        #      value.lib = the name of the shared library file (without the *.so or *.dll extension)
        #      value.gir = the name of the *.gir and *.typelib files (without the extension)
        self.pcMap = {
            "gst-editing-services-1.0" : {
                "lib" : "libges-1.0",
                "gir" : "GES-1.0"
            }
        }

        # The names of the plugin files (without the *.so or *.dll extension)
        self.pluginNames = [
            "libgstnle"
        ]

        # The names of the static library files (without the *.a or *.lib extension)
        self.staticLibNames = [
        ]

        # Environment variables that only exist when `conan` is called through gst-conan
        self.gstRevision = os.getenv("GST_CONAN_REVISION", "master")

        if gst_conan.DEBUG_MODE:
            self.output.info("--------------------------")
            self.output.info("GstEditingServicesConan.__init__")
            self.output.info(json.dumps(self.__dict__, indent=4, sort_keys=True, skipkeys=True, default=lambda x: None))
            self.output.info("--------------------------")

    def build(self):
        if gst_conan.DEBUG_MODE:
            self.output.info("--------------------------")
            self.output.info("GstEditingServicesConan.build")
            self.output.info(f"os = {self.settings.os}")
            self.output.info(f"compiler = {self.settings.compiler}")
            self.output.info(f"build_type = {self.settings.build_type}")
            self.output.info(f"arch = {self.settings.arch}")
            self.output.info(json.dumps(self.__dict__, indent=4, sort_keys=True, skipkeys=True, default=lambda x: None) + "")
            self.output.info("--------------------------")

        pcPaths = [
            os.path.join(self.deps_cpp_info["gstreamer"].rootpath, "pc-conan"),
            os.path.join(self.deps_cpp_info["gst-plugins-base"].rootpath, "pc-conan")
        ]

        meson = Meson(self)
        meson.configure(source_folder=self.name, build_folder="build", pkg_config_paths=pcPaths)
        meson.build()

    def package(self):
        if gst_conan.DEBUG_MODE:
            self.output.info("--------------------------")
            self.output.info("GstEditingServicesConan.package")
            self.output.info(json.dumps(self.__dict__, indent=4, sort_keys=True, skipkeys=True, default=lambda x: None) + "")
            self.output.info("--------------------------")

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
        self.copy("*.h", dst="include/ges", src=f"{self.name}/ges")
        self.copy("*.h", dst="include/ges", src= "build/ges")

        # bin folder
        os.makedirs(os.path.join(self.package_folder, "bin"), exist_ok=True)

        # executables go into bin folder
        for execName in self.execNames:
            if gst_conan.DEBUG_MODE:
                self.output.info(f"{execName}{extExe}")
                self.output.info(os.path.join(buildFolder, "tools"))
                self.output.info(os.path.join(self.package_folder, "bin"))

            gst_conan.base.copyOneFile(f"{execName}{extExe}",
                srcFolder=os.path.join(buildFolder, "tools"),
                destFolder=os.path.join(self.package_folder, "bin"),
                keepPath=False)

        # static libs go into lib folder
        destLibFolder = os.path.join(self.package_folder, "lib")
        for staticLibName in self.staticLibNames:
            gst_conan.base.copyOneFile(f"{staticLibName}{extLib}", buildFolder, destLibFolder, keepPath=False)

        # core plugins go into plugins folder
        destPluginFolder = os.path.join(self.package_folder, "plugins")
        for pluginName in self.pluginNames:
            if isLinux:
                gst_conan.base.copyOneSharedObjectFileGroup(pluginName, buildFolder, destPluginFolder, keepPath=False)
            else:
                gst_conan.base.copyOneFile(f"{pluginName}{extSo}", buildFolder, destPluginFolder, keepPath=False)

        # pkg-config files and associated files (libs, girs, and typelibs)
        srcPcFolder = os.path.join(buildFolder, "pkgconfig")
        destPcFolder = os.path.join(self.package_folder, "pc")
        destPcConanFolder = os.path.join(self.package_folder, "pc-conan")
        destGirFolder = os.path.join(self.package_folder, "data", "gir-1.0")
        destTypelibFolder = os.path.join(self.package_folder, "lib", "girepository-1.0")
        for pcName, otherNames in self.pcMap.items():
            libName = otherNames["lib"]
            girName = otherNames["gir"]

            if None != libName:
                if isLinux:
                    gst_conan.base.copyOneSharedObjectFileGroup(libName, buildFolder, destLibFolder, keepPath=False)
                else:
                    gst_conan.base.copyOneFile(f"{libName}{extSo}", buildFolder, destLibFolder, keepPath=False)

            if None != girName:
                gst_conan.base.copyOneFile(f"{girName}.gir", buildFolder, destGirFolder, keepPath=False)
                gst_conan.base.copyOneFile(f"{girName}.typelib", buildFolder, destTypelibFolder, keepPath=False)

            # Copy the original pkg-config file
            shutil.copy2(src=os.path.join(srcPcFolder, f"{pcName}.pc"), dst=destPcFolder)

            # Load the pkg-config file, modify, and save
            pcFile = gst_conan.build.PkgConfigFile()
            pcFile.load(os.path.join(srcPcFolder, f"{pcName}.pc"))

            pcFile.variables["prefix"] = self.package_folder
            pcFile.variables["exec_prefix"] = "${prefix}"
            pcFile.variables["libdir"] = "${prefix}/lib"
            pcFile.variables["includedir"] = "${prefix}/include"
            pcFile.variables["datarootdir"] = "${prefix}/data"
            pcFile.variables["datadir"] = "${datarootdir}"
            pcFile.variables["girdir"] = "${datadir}/gir-1.0"
            pcFile.variables["typelibdir"] = "${libdir}/girepository-1.0"

            if pcName == "gstreamer-1.0":
                pcFile.variables["toolsdir"] = "${prefix}/bin"
                pcFile.variables["pluginsdir"] = "${prefix}/plugins"

            pcFile.save(os.path.join(destPcConanFolder, f"{pcName}.pc"))

    def package_info(self):
        '''
        I am not sure if this method is necessary since GstEditingServices is using pkgconfig.
        '''

        if gst_conan.DEBUG_MODE:
            self.output.info("--------------------------")
            self.output.info("GstEditingServicesConan.package_info")
            self.output.info(json.dumps(self.__dict__, indent=4, sort_keys=True, skipkeys=True, default=lambda x: None) + "")
            self.output.info("--------------------------")

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

    def requirements(self):
        self.requires(f"gstreamer/{self.version}@{self.user}/{self.channel}")
        self.requires(f"gst-plugins-base/{self.version}@{self.user}/{self.channel}")

    def source(self):
        if gst_conan.DEBUG_MODE:
            self.output.info("--------------------------")
            self.output.info("GstEditingServicesConan.source")
            self.output.info(json.dumps(self.__dict__, indent=4, sort_keys=True, skipkeys=True, default=lambda x: None) + "")
            self.output.info("--------------------------")

        if gst_conan.DEBUG_MODE:
            # This is just for temporary debugging purposes
            gst_conan.base.copytree(srcFolder=os.path.expanduser(f"~/github/gstreamer/{self.name}"),
                                    destFolder=os.path.join(self.source_folder, self.name))
        else:
            # This is what actually belongs here.
            self.run(f"git clone --recurse-submodules https://github.com/gstreamer/{self.name}.git -b {self.gstRevision}")
            self.run(f"cd {self.name}")

        # WARNING:  The following will only work if called through gst-conan.
        # We do this because the attribute usage does not seem to work:  `exports = "gst_conan"`
        # This copies the gst_conan package to the `export` folder (next to the conanfile.py)
        exportFolder = os.path.join(os.path.dirname(self.source_folder), "export")
        gst_conan.base.copytree(
            srcFolder=os.path.join(gstConanParentFolder, "gst_conan"),
            destFolder=os.path.join(exportFolder, "gst_conan"),
            ignoreFolders=set(["__pycache__"]))