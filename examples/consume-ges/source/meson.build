project('consume-ges', 'cpp',
        version : '0.0.0',
        meson_version: '>= 0.47.0',
        default_options: [ 'buildtype=debug',
                           'cpp_std=c++17',
                           'warning_level=1']
)

pkg_name = 'consume-ges'
pkg_version = '0.0.0'

cdata = configuration_data()
cdata.set('VERSION', '"@0@"'.format(pkg_version))
cdata.set('PACKAGE', '"@0@"'.format(pkg_name))
cdata.set('PACKAGE_NAME', '"@0@"'.format(pkg_name))
cdata.set('PACKAGE_VERSION', '"@0@"'.format(pkg_version))
cdata.set('LICENSE', '"LGPL v3"')

includeFolder = include_directories('include')

executable(
    pkg_name,
    [ 'src/main.cpp'                              # all source files
    ],
    include_directories: includeFolder,
    dependencies:
    [   dependency('gst-editing-services-1.0')    # Use name of *.pc file (without extension).
    ],
    name_prefix: ''
)