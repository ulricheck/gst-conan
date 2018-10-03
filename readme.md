# gst-conan

This is a tool for building [Gstreamer](https://gstreamer.freedesktop.org/) components as [Conan](https://conan.io/) packages
using the [Meson](https://mesonbuild.com/) build scripts which are included in the Gstreamer repositories.

## Machine setup instructions

First time users should look at the [machine setup instructions](doc/machine-setup.md).

This tool is expected to work on most Linux distros (we guess), but it has only been tested on Mint 19.

In the future it may work on Mac and Windows, but this is a long ways off.

## Status

This tool can create 6 conan packages:

 * [gstreamer](https://github.com/gstreamer/gstreamer)
 * [gst-plugins-base](https://github.com/gstreamer/gst-plugins-base)
 * [gst-editing-services](https://github.com/gstreamer/gst-editing-services)
 * [gst-plugins-good](https://github.com/gstreamer/gst-plugins-good)
 * [gst-plugins-bad](https://github.com/gstreamer/gst-plugins-bad)
 * [gst-plugins-ugly](https://github.com/gstreamer/gst-plugins-ugly)
 * [gst-libav](https://github.com/gstreamer/gst-libav)

I also have two example projects which show how to consume the conan packages.
 * [a meson project](examples/consume-ges-meson).
 * [a cmake project](examples/consume-ges-cmake).

## How to use `gst-conan`

Clone it and read the `--help` info. 

```bash
git clone https://github.com/Panopto/gst-conan
cd gst-conan
./gst-conan --help
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

## Legal stuff

Here is our [legal disclaimer](doc/legal-disclaimer.md).