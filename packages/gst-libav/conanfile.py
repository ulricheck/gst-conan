from conans import ConanFile, Meson, tools

import os
import sys
if sys.version_info[0] < 3:
    raise Exception("The version of Python must be 3 or greater.")

# ----------------
# Import helper methods under gst_conan
# ----------------
sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)))
import gst_conan


ffmpeg_wrap_src = """project('FFmpeg', 'c', 'cpp')

cc = meson.get_compiler('c')

ffmpeg = dependency('ffmpeg')


libavfilter_dep = declare_dependency(
  version : '7.16.100',
  dependencies : [cc.find_library('avfilter', dirs : '{libdir}'), ffmpeg],
  include_directories : include_directories('{incdir}'))

libavformat_dep = declare_dependency(
  version: '58.12.100',
  dependencies : [cc.find_library('avformat', dirs : '{libdir}'), ffmpeg],
  include_directories : include_directories('{incdir}'))

libavutil_dep = declare_dependency(
  version: '56.14.100',
  dependencies : [cc.find_library('avutil', dirs : '{libdir}'), ffmpeg],
  include_directories : include_directories('{incdir}'))

libavcodec_dep = declare_dependency(
  version: '58.18.100',
  dependencies : [cc.find_library('avcodec', dirs : '{libdir}'), ffmpeg],
  include_directories : include_directories('{incdir}'))
"""


# ----------------
# Implement the ConanFile
# ----------------
class GstLibav(ConanFile):
    name = "gst-libav"
    license = "LGPL"
    url = ["https://github.com/Panopto/gst-conan", "https://github.com/gstreamer/gst-libav"]
    description = "Gstreamer plugin for libav."
    settings = {
        "os": ["Linux"],
        "compiler": None,
        "build_type": None,
        "arch": None
    }
    options = {"nvenc": [False, True],}
    default_options = ("nvenc=True",)
    build_policy = "outdated"
    generators = "pkg_config"

    # It would be nice to export like this ...

    #   exports = "../../gst_conan/*", "../../config/*"
    #
    # ... but it doesn't work.  Soft links don't work either.  See https://github.com/conan-io/conan/issues/3591.
    #
    # So these folders have been copied multiple times within the repo.
    exports = "gst_conan/*", "config/*"

    def build(self):
        pcPaths = [
            self.build_folder,
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
        self.requires(f"ffmpeg/[>=4.1]@{self.user}/{self.channel}")
        self.requires(f"gstreamer/{self.version}@{self.user}/{self.channel}")
        self.requires(f"gst-plugins-base/{self.version}@{self.user}/{self.channel}")

    def source(self):
        # This is what actually belongs here.
        self.run(f"git clone --recurse-submodules https://github.com/gstreamer/{self.name}.git -b {self.gstRevision}")
        self.run(f"cd {self.name}")
        # workaround to accept generated pkgconfig files
        tools.mkdir(f"{self.name}/subprojects/FFmpeg")
        tools.save(f"{self.name}/subprojects/FFmpeg/meson.build", ffmpeg_wrap_src.format(
            libdir=os.path.join(self.deps_cpp_info["ffmpeg"].rootpath, 'lib'),
            incdir=os.path.join(self.deps_cpp_info["ffmpeg"].rootpath, 'include'),
            ))

