# gst-conan
This is a tool for building [Gstreamer](https://gstreamer.freedesktop.org/) components as [Conan](https://conan.io/) packages
using the [Meson](https://mesonbuild.com/) build scripts included in the Gstreamer repositories.

This tool is expected to work on most Linux distros (we guess).  In the future it may work on Mac and Windows (pending)
work by other contributors in other Gstreamer repositories.

First time users should look at the [machine setup instructions](#machine-setup-instructions).

## Status
This is a very new project and there is much work to be done.

Currently I have 3 conan packages and an example which consumes them:
 * gstreamer
 * gst-plugins-base
 * gst-editing-services 

Currently, none of the plugins are being packaged; but I'll be working on it.

## How to use `gst-conan`
Clone it and read the `--help` info. 

```bash
git clone https://github.com/Panopto/gst-conan
cd gst-conan
./gst-conan --help
```

You can get help for each verb.  For example:
```bash 
./gst-conan create --help
```

### How to create the Conan packages
Use `gst-conan` to create several conan packages for Gstreamer `1.14.2` as follows.  The packages are published in your
local Conan repo.

```bash
./gst-conan create --rev 1.14.2 --version 1.14.2 --buildtype debug --user my_user_name --channel my_channel
```

## Contributions are welcome
This repo is moderated by Panopto's media developers.  Your pull requests into this repo are welcome.

If you are unhappy with our moderation, you are welcome to fork the repo and moderate things differently.

## Roadmap
There is plenty of room for [improvements](doc/roadmap.md) here.

## Machine setup instructions

Below are instructions which cover the distros that we have tried.

[Ubuntu, Mint , and probably Debian](doc/setup-ubuntu.md)

## Legal stuff
Here is our [legal disclaimer](doc/legal-disclaimer.md).