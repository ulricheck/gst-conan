# Roadmap
We have several items on our radar. 

## Follow best practices for Conan
We would like to follow the best practices for Conan.

### Build through conan
Currently, we are only using Conan for the packaging step.  We are building the source outside of Conan because many of
the Meson projects will not build unless they are under the parent-project of [gst-build](https://github.com/GStreamer/gst-build).
We would like to figure out how to get around this restriction (of being forced to use the parent project) so that we
can use Conan itself to link the inter-project dependencies and to drive each Meson build individually.

### Run tests through Conan
We should be able to run unit tests through Conan.

### Install through Conan
It is theoretically possible to convert a set of Conan packages into a set of packages for each distro (perhaps using
`snap`).  We want to move towards this goal.  

## Extend functionality to Windows Platform
Currently this only works on Linux (we guess).

## Extend functionaltiy to Darwin (Mac) Platform
Currently this only works on Linux (we guess).