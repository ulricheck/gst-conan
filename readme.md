# gst-conan

This is a tool for building [Gstreamer](https://gstreamer.freedesktop.org/) components as [Conan](https://conan.io/) packages
using the [Meson](https://mesonbuild.com/) build scripts which are included in the Gstreamer repositories.

## Machine setup instructions

First time users should look at the [machine setup instructions](doc/machine-setup.md).

This tool is expected to work on most Linux distros (we guess), but we only have machine setup instructions for
debian-ish systems (and it has only been tested on Mint 19).

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
 * [cmake example](examples/consume-ges-cmake)
 * [meson example](examples/consume-ges-meson)

## How to use `gst-conan`

Make sure `conan` is installed.

```bash
pip3 install --user conan
```

We recommend that you have `docker` installed.

Clone the `gst-conan` repo and read the `--help` info. 

```bash
git clone https://github.com/Panopto/gst-conan
cd gst-conan
./gst-conan --help
```

### How to create the Conan packages via Docker (recommended)

Make sure `docker` is installed.

Use `gst-conan` to create several conan packages for Gstreamer `1.14.4` as follows.  The packages are published in your
local Conan repo.

```bash
./gst-conan create --docker ubuntu-18.04 --rev 1.14.4 --version 1.14.4 --build_type Debug --user my_conan_user --channel my_conan_channel --keep-source
```

#### Need to debug the build?
You can poke around inside the docker container like this:

```bash
docker run -it --mount type=bind,src=$HOME/.conan/data,dst=/home/default_user/.conan/data gst-conan_ubuntu-18.04:latest 'bash'
```

### How to create the Conan packages without Docker (not recommend)

Use `gst-conan` to create several conan packages for Gstreamer `1.14.4` as follows.  The packages are published in your
local Conan repo.

```bash
./gst-conan create --rev 1.14.4 --version 1.14.4 --build_type Debug --user my_conan_user --channel my_conan_channel --keep-source
```

### How to publish conan packages
After creating the packages, you may want to publish them to [their home on bintray](https://bintray.com/panopto-oss/gst-conan).

First, let's define some constants.

```bash
BINTRAY_API_KEY="you_find_the_key"
GSTREAMER_VERSION="1.14.4"
GIT_TAG="$GSTREAMER_VERSION@panopto/unstable"
```

Authenticate yourself.

```bash
conan remote add panopto-oss https://api.bintray.com/conan/panopto-oss/gst-conan
conan user --password $BINTRAY_API_KEY --remote panopto-oss panopto-oss
```

Do a dry run by including the `--skip-upload` flag.

```bash
conan upload --skip-upload --check --confirm --remote panopto-oss gst*/$GIT_TAG
```

Perform the upload.

```bash
conan upload --check --confirm --remote panopto-oss gst*/$GIT_TAG
```

Tag the relevant `git` commit. 

```bash
git tag $GIT_TAG
git push --tags
```

## Contributions are welcome

This repo is moderated by Panopto's media developers.  Your pull requests into this repo are welcome.

If you are unhappy with our moderation, you are welcome to fork the repo and moderate things differently.

## Roadmap

We have a [roadmap](doc/roadmap.md) for things that we'd like to improve, but we might not have time in the immediate
future.

## Legal stuff

Here is our [legal disclaimer](doc/legal-disclaimer.md).