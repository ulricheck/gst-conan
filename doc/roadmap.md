# Roadmap

We have several items on our radar.

## Follow best practices for Conan

We would like to follow the best practices for Conan (we are still learning).

### Run unit tests through Conan

We should be able to run unit tests through Conan.

## Machine setup instructions for other Linux distros besides Mint 19

Presumably these scripts will work on other Linux distros besides Mint 19, Ubuntu 18.04, and related Debian distros.
It's just a matter of figuring out which packages to install.

We need to expand the `gst-conan setup` command to work on other popular distros.

## Proper distro packages based on Conan packages

It is theoretically possible to convert a set of Conan packages into a set of packages which can be installed on each
distro (perhaps using `snap` or something like that).  In anticipation of moving towards this goal, the conan packages
already contain `pkg-config` files for a typical target installation.  There is also a Python `PkgConfigFile` class
which we can use to modify the `pkg-config` files easily.

## Extend functionality to Windows and Darwin (Mac) Platform

We have heard that the community is working on making the `meson.build` scripts work for Windows (and with a VS compiler).
Presumably [cerbero](https://github.com/gstreamer/cerbero) will be required for that.  Once it's working through cerbero
we will want to make it work here.

We have no idea about Darwin (Mac).