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
class GstPluginsGoodConan(ConanFile):
    name = "gst-plugins-good"
    license = "LGPL"
    url = "https://github.com/gstreamer/gst-plugins-good"
    description = "Good Gstreamer plugins and helper libraries."
    settings = "os", "compiler", "build_type", "arch"
    options = {}
    default_options = None

    # We are supposed to be able to export the gst_conan package as follows, but it doesn't seem to work.
    # Soft links don't work either.  See https://github.com/conan-io/conan/issues/3591.
    # exports = "../../gst_conan"

    exports = "gst_conanfile/*"

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
            "libgsteffectv",
            "libgstrtp",
            "libgstmultipart",
            "libgstwavenc",
            "libgstrtsp",
            "libgstmultifile",
            "libgstid3demux",
            "libgstudp",
            "libgstvideomixer",
            "libgstvideofilter",
            "libgstspectrum",
            "libgstflv",
            "libgstinterleave",
            "libgstvideocrop",
            "libgstequalizer",
            "libgstsmpte",
            "libgstimagefreeze",
            "libgstdtmf",
            "libgstgoom",
            "libgstwavparse",
            "libgstmatroska",
            "libgstnavigationtest",
            "libgstdebug",
            "libgstapetag",
            "libgstshapewipe",
            "libgsticydemux",
            "libgstaudiofx",
            "libgstisomp4",
            "libgstavi",
            "libgstflxdec",
            "libgstmulaw",
            "libgstalaw",
            "libgstlevel",
            "libgstautodetect",
            "libgstgoom2k1",
            "libgstdeinterlace",
            "libgstaudioparsers",
            "libgstauparse",
            "libgstcutter",
            "libgstreplaygain",
            "libgstvideobox",
            "libgsty4menc",
            "libgstalphacolor",
            "libgstalpha",
            "libgstmonoscope",
            "libgstrtpmanager",
            "libgstpulseaudio",
            "libgstjpeg",
            "libgstvideo4linux2",
            "libgstossaudio",
            "libgstoss4",
            "libgstximagesrc"
        ]

        # The names of the static library files (without the *.a or *.lib extension)
        self.staticLibNames = [
            "liblibparser"
        ]

        # Environment variables that only exist when `conan` is called through gst-conan
        self.gstRevision = os.getenv("GST_CONAN_REVISION", self.version)

    def build(self):
        pcPaths = [
            os.path.join(self.deps_cpp_info["gstreamer"].rootpath),
            os.path.join(self.deps_cpp_info["gst-plugins-base"].rootpath)
        ]

        meson = Meson(self)
        meson.configure(source_folder=self.name, build_folder="build", pkg_config_paths=pcPaths)
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
        self.copy("*.h", dst="include", src=f"{self.name}")

        # static libs go into lib folder
        destLibFolder = os.path.join(self.package_folder, "lib")
        for staticLibName in self.staticLibNames:
            gst_conanfile.copyOneFile(f"{staticLibName}{extLib}", buildFolder, destLibFolder, keepPath=False)

        # core plugins go into plugins folder
        destPluginFolder = os.path.join(self.package_folder, "plugins")
        for pluginName in self.pluginNames:
            if isLinux:
                gst_conanfile.copyOneSharedObjectFileGroup(pluginName, buildFolder, destPluginFolder, keepPath=False)
            else:
                gst_conanfile.copyOneFile(f"{pluginName}{extSo}", buildFolder, destPluginFolder, keepPath=False)

    def package_info(self):
        '''
        I am not sure if this method is necessary since GstPluginsGood is using pkgconfig.
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

    def requirements(self):
        self.requires(f"gstreamer/{self.version}@{self.user}/{self.channel}")
        self.requires(f"gst-plugins-base/{self.version}@{self.user}/{self.channel}")

    def source(self):
        # This is what actually belongs here.
        self.run(f"git clone --recurse-submodules https://github.com/gstreamer/{self.name}.git -b {self.gstRevision}")
        self.run(f"cd {self.name}")
