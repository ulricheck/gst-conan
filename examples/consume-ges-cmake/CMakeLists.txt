cmake_minimum_required(VERSION 3.10)
project(consume-ges)

# Pull stuff from conan
include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()

# Workaround for cmake bug https://gitlab.kitware.com/cmake/cmake/issues/18150
set(ENV{PKG_CONFIG_PATH} "$ENV{PKG_CONFIG_PATH}:${CONAN_GST-EDITING-SERVICES_ROOT}:${CONAN_GST-PLUGINS-BASE_ROOT}:${CONAN_GSTREAMER_ROOT}")

# Link to GES via pkg-config
find_package(PkgConfig REQUIRED)
pkg_check_modules(PKG_GES REQUIRED gst-editing-services-1.0)

# The rest
add_executable(consume-ges source/src/main.cpp)

target_include_directories(consume-ges PUBLIC source/include)
target_include_directories(consume-ges PUBLIC ${PKG_GES_INCLUDE_DIRS})

target_link_libraries(consume-ges ${CONAN_LIBS})
target_link_libraries(consume-ges ${PKG_GES_LIBRARIES})