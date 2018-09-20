# gst-conan
This is a tool for building [Gstreamer](https://gstreamer.freedesktop.org/) components as [Conan](https://conan.io/) packages
using the [Meson](https://mesonbuild.com/) build scripts which are included in the Gstreamer repositories.

This tool is expected to work on most Linux distros (we guess).  In the future it may work on Mac and Windows (pending)
work by other contributors in other Gstreamer repositories.

First time users should look at the [machine setup instructions](#machine-setup-instructions).

## Status
This is a very new project and there is much work to be done.

This tool can create 6 conan packages:

 * [gstreamer](https://github.com/gstreamer/gstreamer)
 * [gst-plugins-base](https://github.com/gstreamer/gst-plugins-base)
 * [gst-editing-services](https://github.com/gstreamer/gst-editing-services)
 * [gst-plugins-good](https://github.com/gstreamer/gst-plugins-good)
 * [gst-plugins-bad](https://github.com/gstreamer/gst-plugins-bad)
 * [gst-libav](https://github.com/gstreamer/gst-libav)

There also is [an example project](examples/consume-ges) which consumes the packages above.

I omitted [gst-plugins-ugly](https://github.com/gstreamer/gst-plugins-ugly) because I didn't want to sit and figure out
which libraries I needed to install to get it working.

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
Use `gst-conan` to create several conan packages for Gstreamer `1.14.3` as follows.  The packages are published in your
local Conan repo.

```bash
./gst-conan create --rev 1.14.3 --version 1.14.3 --build_type Debug --user my_conan_user --channel my_conan_channel
```

## Contributions are welcome
This repo is moderated by Panopto's media developers.  Your pull requests into this repo are welcome.

If you are unhappy with our moderation, you are welcome to fork the repo and moderate things differently.

## Roadmap
We have a [roadmap](doc/roadmap.md) for things that we'd like to improve, but we might not have time in the immediate
future.

## Machine setup instructions

Below are instructions which cover the distros that we have tried.

[Ubuntu, Mint , and probably Debian](doc/setup-ubuntu.md)

## Legal stuff
Here is our [legal disclaimer](doc/legal-disclaimer.md).