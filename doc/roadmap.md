# Roadmap

There is plenty of room for improvement.

## Follow best practices for Conan

We would like to follow the best practices for Conan (we are still learning).

### Integration with [bintray](https://bintray.com/conan/conan-center)

Unfortunately, the Conan packages defined here are not ready for bintray yet.  One challenge is that our builds
require installing various libraries using the package manager for our Linux distro.  In a perfect world, the
pre-requisites would already be available through bintray as Conan packages; but there is much work to do on
that front (more than we have time for).

## Machine setup instructions for common Linux Distros

Machine setup is done through the `gst-conan setup` command.  Currently it has only been tested for Mint 19, and we 
assume it will work for similar Debians (especially Ubuntu 18.04).

Presumably these scripts will work on most Linux distros, but some kind of package-manager setup is required.  We need
to work on `gst-conan setup` so it works on other common Linux distros.

## Packaging for Windows and Darwin (Mac) Platform

We have heard that the community is working on making the `meson.build` scripts work for Windows (and with a VS compiler).
Presumably [cerbero](https://github.com/gstreamer/cerbero) will be required for that.  Once it's working through cerbero
we will want to make it work here.

We have no idea about Darwin (Mac).