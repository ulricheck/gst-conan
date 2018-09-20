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
class GstPluginsBadConan(ConanFile):
    name = "gst-plugins-bad"
    license = "LGPL"
    url = "https://github.com/gstreamer/gst-plugins-bad"
    description = "Bad Gstreamer plugins and helper libraries."
    settings = "os", "compiler", "build_type", "arch"
    options = {}
    default_options = None

    # We are supposed to be able to export the gst_conan package as follows, but it doesn't seem to work.
    #exports = "../../gst_conan"

    def __init__(self, output, runner, user, channel):
        ConanFile.__init__(self, output, runner, user, channel)

        #  The names of executable files without any possible file extension
        self.execNames =[
        ]

        #  The key is the names of the pkgconfig files (without the *.pc extension)
        #  The value is an object with multiple fields.
        #      value.lib = the name of the shared library file (without the *.so or *.dll extension)
        #      value.gir = the name of the *.gir and *.typelib files (without the extension)
        self.pcMap = {
        }

        # The names of the plugin files (without the *.so or *.dll extension)
        self.pluginNames = [
            "libgstlegacyrawparse",
            "libgstfestival",
            "libgstvmnc",
            "libgstadpcmdec",
            "libgstinter",
            "libgstsdpelem",
            "libgstremovesilence",
            "libgstmxf",
            "libgstfrei0r",
            "libgstgeometrictransform",
            "libgstvideoframe_audiolevel",
            "libgstvideofiltersbad",
            "libgstspeed",
            "libgstmpegpsmux",
            "libgstivtc",
            "libgstjp2kdecimator",
            "libgstfaceoverlay",
            "libgstautoconvert",
            "libgstaudiofxbad",
            "libgstaudiobuffersplit",
            "libgstsmooth",
            "libgstmpegtsdemux",
            "libgstdvdspu",
            "libgstpcapparse",
            "libgstfieldanalysis",
            "libgstvideosignal",
            "libgstmpegpsdemux",
            "libgstpnm",
            "libgstcoloreffects",
            "libgstmidi",
            "libgstaiff",
            "libgstfreeverb",
            "libgstaudiomixmatrix",
            "libgsttimecode",
            "libgstsegmentclip",
            "libgstivfparse",
            "libgstnetsim",
            "libgstdebugutilsbad",
            "libgstaudiolatency",
            "libgstgdp",
            "libgstinterlace",
            "libgstsubenc",
            "libgstproxy",
            "libgstaudiovisualizers",
            "libgstrtponvif",
            "libgstasfmux",
            "libgstcompositor",
            "libgstaccurip",
            "libgstrfbsrc",
            "libgstadpcmenc",
            "libgstgaudieffects",
            "libgstyadif",
            "libgstid3tag",
            "libgsty4mdec",
            "libgstmpegtsmux",
            "libgstsiren",
            "libgstjpegformat",
            "libgststereo",
            "libgstvideoparsersbad",
            "libgstdvbsuboverlay",
            "libgstbayer",
            "libgstcamerabin",
            "libgstdtls",
            "libgstdashdemux",
            "libgstcurl",
            "libgstsmoothstreaming",
            "libgstopenglmixers",
            "libgsthls",
            "libgstkms",
            "libgstdecklink",
            "libgstshm",
            "libgstfbdevsink",
            "libgstdvb",
            "libgstipcpipeline",
            "libgstcodecparsers-1.0",
            "libgstbadvideo-1.0",
            "libgsturidownloader-1.0",
            "libgstbadaudio-1.0",
            "libgstadaptivedemux-1.0",
            "libgstisoff-1.0",
            "libgstbasecamerabinsrc-1.0",
            "libgstwebrtc-1.0",
            "libgstmpegts-1.0",
            "libgstphotography-1.0",
            "libgstinsertbin-1.0",
            "libgstplayer-1.0"
        ]

        # The names of the static library files (without the *.a or *.lib extension)
        self.staticLibNames = [
            "libparser"
        ]

        # Environment variables that only exist when `conan` is called through gst-conan
        self.gstRevision = os.getenv("GST_CONAN_REVISION", "master")

        if gst_conan.DEBUG_MODE:
            self.output.info("--------------------------")
            self.output.info("GstPluginsBadConan.__init__")
            self.output.info(json.dumps(self.__dict__, indent=4, sort_keys=True, skipkeys=True, default=lambda x: None))
            self.output.info("--------------------------")

    def build(self):
        if gst_conan.DEBUG_MODE:
            self.output.info("--------------------------")
            self.output.info("GstPluginsBadConan.build")
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
            self.output.info("GstPluginsBadConan.package")
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
        self.copy("*.h", dst="include", src=f"{self.name}")

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

    def package_info(self):
        '''
        I am not sure if this method is necessary since GstPluginsGood is using pkgconfig.
        '''

        if gst_conan.DEBUG_MODE:
            self.output.info("--------------------------")
            self.output.info("GstPluginsBadConan.package_info")
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
            self.output.info("GstPluginsBadConan.source")
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