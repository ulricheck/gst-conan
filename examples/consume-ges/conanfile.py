# These parameters should match the conan packages that you have built using `gst-conan create ...`
GST_CONAN_VERSION="1.14.3"
GST_CONAN_USER="my_conan_user"
GST_CONAN_CHANNEL="my_conan_channel"

from conans import ConanFile, Meson

import json
import os

class ExampleConsumeGes(ConanFile):
    name = "gst-conan-example-consume-ges"
    license = "LGPL"
    url = "https://github.com/Panopto/gst-conan"
    description = "An example of consuming GES with a Meson project"
    settings = "os", "compiler", "build_type", "arch"
    options = {}
    default_options = None

    # We specify the sources using a relative path, so we don't need a `source(self)` method.
    export_sources = "source/*"

    # This is how we declare our dependencies to Conan.  GES will come with transitive dependencies.
    # We also need to handle the pkg_config_paths in the `build(self)` method.
    requires = f"gst-editing-services/{GST_CONAN_VERSION}@{GST_CONAN_USER}/{GST_CONAN_CHANNEL}"

    def build(self):

        # This is how we pull tell Meson about our pkg-config paths.
        # We need to wire the pkg_config_path for GES and it's transitive dependencies.
        pcPaths = []
        for depName, dep in self.deps_cpp_info.dependencies:
            pcPath = os.path.join(dep.rootpath, "pc-conan")
            if os.path.isdir(pcPath):
                pcPaths.append(pcPath)

        # Run the build with pkg-config paths from our dependencies.
        meson = Meson(self)
        meson.configure(source_folder="source", build_folder="build", pkg_config_paths=pcPaths)
        meson.build()

        # At this point, the executable has been created but it will not run without the shared object files (*.so or *.dll).
        # on it's path.  So let's get all the paths together
        libPaths = []
        for depName, dep in self.deps_cpp_info.dependencies:
            for libFolder in dep.libdirs:
                libPaths.append(os.path.join(dep.rootpath, libFolder))

        # We also need to know where all the plugins are located (so we can tell gstreamer to load them).
        pluginPaths = []
        for depName, dep in self.deps_cpp_info.dependencies:
            pluginPath = os.path.join(dep.rootpath, "plugins")
            if os.path.isdir(pluginPath):
                pluginPaths.append(pluginPath)

        # Save out the paths
        paths = {
            "lib": libPaths,
            "pc": pcPaths,
            "plugin": pluginPaths
        }
        with open("build/paths.json", "w") as writer:
            json.dump(paths, fp=writer, indent=4)


        # Make a bash script for easy execution of the target
        joinedLibPaths = ":".join(libPaths)
        joinedPluginPaths = ":".join(pluginPaths)
        with open("build/run.sh", "w") as writer:
            writer.write("#!/bin/bash\n")
            writer.write("\n")
            writer.write('thisFolder="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )"' + "\n")
            writer.write("\n")
            writer.write(f"export LD_LIBRARY_PATH={joinedLibPaths}:$LD_LIBRARY_PATH\n")
            writer.write(f"export GST_PLUGIN_PATH={joinedPluginPaths}\n")
            writer.write("\n")
            writer.write(f"exec $thisFolder/consume-ges \"$@\"\n")

        # Make the script executable
        os.chmod("build/run.sh", 0o755)

    def package(self):
        pass
