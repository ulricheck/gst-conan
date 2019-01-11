# Roadmap

There is plenty of room for improvement.

## Follow best practices for Conan

We would like to follow the best practices for Conan (we are still learning).

In a perfect world, the only pre-requisites for building Conan packages should be other Conan packages.  But in this
world, Gstreamer depends on a number of packages which have not been Conan-ized yet; and we we have a *machine setup*
step which allows this to be built on *some* Linux distros.  We would like to communiity help to Conan-ize all of the
Debian packages on which Gstreamer depends.  

## Packaging for other Linux Distros
We have only verified `gst-conan` packages on Mint 19 (equivalent to Ubuntu 18.04).  We are not certain to what extent
the conan packages we build will work on other Linux distros.  Presumably they will "just work" but we have never
tried.

## Packaging for Windows and Darwin (Mac) Platform
We do not build packages for Windows and Darwin (Mac), only Linux.

We have heard that the community is working on making the `meson.build` scripts work for Windows (and with a VS compiler).
Presumably [cerbero](https://github.com/gstreamer/cerbero) will be required for that.  Once it's working through cerbero
we will want to make it work here.

We have no idea about Darwin (Mac).
