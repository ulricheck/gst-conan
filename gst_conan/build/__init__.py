def conanBuildTypes() -> list:
    '''
    These are the conan build types that we allow.
    :return: The list of types allowed.
    '''
    return ["Debug", "Release"]

def gstreamerPackageList() -> list:
    return [ "gstreamer",
             "gst-plugins-base",
             "gst-editing-services",
             "gst-plugins-good",
             "gst-plugins-bad",
             "gst-plugins-ugly",
             "gst-libav"]

def mesonBuildTypes() -> list:
    return ["plain", "debug", "debugoptimized", "release"]