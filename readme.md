# gst-conan
This is a tool for building [Gstreamer](https://gstreamer.freedesktop.org/) components as [Conan](https://conan.io/) packages
using the [Meson](https://mesonbuild.com/) build system via [gst-build](https://github.com/GStreamer/gst-build).

This tool is expected to work on the same platforms as [gst-build](https://github.com/GStreamer/gst-build), so most Linux
distros are covered (we guess).

First time users should look at the [machine setup instructions](#machine-setup-instructions).

## Usage
Read all about it.

```bash
git clone https://github.com/Panopto/gst-conan
cd gst-conan
./gst-conan --help
```

For example, create several conan packages for Gstreamer `1.14.2` like this.

```bash
./gst-conan create --rev 1.14.2 --version 1.14.2 --user my_user_name --channel my_channel
```

## Contributions are welcome
Your pull requests are welcome.

## Roadmap
This is a new project.  We are hoping to make some improvements.

### Create samples which consume the Conan packages
Currently, we don't know whether our packages can be used properly.  We don't have any sample code which pulls in
the Conan packages being built here.

### Follow best practices for Conan
We would like to follow the best practices for Conan.

Currently, we are only using Conan for the packaging step.  We are building the source outside of Conan because many of
the Meson projects will not build unless they are under the parent-project of [gst-build](https://github.com/GStreamer/gst-build).
We would like to figure out how to get around this limitation (of being forced to build the parent project) so that we
can use Conan to drive each individual Meson build.

## Machine setup instructions

Below are instructions which cover the distros that we have tried.

### Ubuntu 18.04, Mint 19 (and maybe Debian)
There are two steps to get `gst-conan` working on your machine. 

#### 1. Edit `~/.bashrc`
Put this at the bottom of the file.

```bash
# This is where pip3 installs `--user` executables (such as meson)
PATH=$PATH:$HOME/.local/bin
```

Restart your terminal or execute `source ~/.bashrc`.

#### 2. Install stuff
```bash
sudo apt update
sudo apt install --yes git python-pip python3-pip ninja-build build-essential libmount-dev libselinux-dev gobject-introspection libglib2.0-dev libgirepository1.0-dev libxml2-dev libavfilter-dev
pip3 install setuptools wheel
pip3 install --user meson
pip3 install conan
```

## Legal disclaimer
The contents of this repo are licensed under [LGPL](license).

We (the maintainers of this repository) are not responsible for accurately representing the licensing status of third
party components (Gstreamer or otherwise).  If **you** use these scripts to build anything, then **you** are responsible
for doing **your own** research about legal restrictions regarding the components being built.

We believe that most of Gstreamer is under an LGPL license of some kind, but we aren't 100% sure.

Gstreamer may have components which are legally restrictive (not covered by LGPL).  For example, many
components of [gst-plugins-ugly](https://github.com/GStreamer/gst-plugins-ugly) are especially restrictive.

Gstreamer may also depend on third party components which are legally restrictive in some way (we haven't checked).

We encourage users to do their own research into legal matters.