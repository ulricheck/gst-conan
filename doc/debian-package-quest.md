# The quest for the right debian packages 
I struggled to find the correct set of debian packages to make this work on `ubuntu-18.04`.

## The current set of debian packages
I determined the current set of debian packages by executing the following command on Linux Mint 19.1 (equivalent to Ubuntu 18.04).

```bash
sudo apt-get build-dep --simulate gstreamer1.0 gstreamer1.0-libav gstreamer1.0-plugins-{base,good,bad,ugly} ges1.0-tools
```

This yielded a large set of packages which I modified as described below.

### minus (packages removed)

```text
gstreamer1.0-doc
gstreamer1.0-plugins-base-doc
libgstreamer-plugins-base1.0-dev
libgstreamer-plugins-good1.0-dev
libgstreamer1.0-dev
```

### plus (packages added)

```text
bison
build-essential
cmake
flex
g++
intltool
libasound2-dev
libavfilter-dev
libfaac-dev
libfaad-dev
liborc-0.4-dev
libpulse-dev
libx264-dev
libxv-dev
ninja-build
pkg-config
```

## Another different set which might have worked
I put together the set of packages below through careful analysis of the meson build output and through
[package searching](https://packages.ubuntu.com/).   This set might have worked but I never checked it.  I abandoned
this approach when I hit a [build problem](https://gitlab.freedesktop.org/gstreamer/gst-plugins-bad/issues/867) which
(as it turns out) had nothing to do with the set of packages that were installed.

We should refer to this set later if we find problems with our current set of packages.

```text
autoconf
automake
autopoint
autotools-dev
bison
bluez
build-essential
cmake
curl
debhelper
devscripts
doxygen
dpkg-dev
fakeroot
flex
g++
gettext
git
glib-networking
gperf
gtk-doc-tools
intltool
jack
libasound2-dev
libass-dev
libavc1394-dev
libavfilter-dev
libcairo-gobject2
libcairo2-dev
libcdio-dev
libcdparanoia-dev
libcgroup-dev
libchromaprint-dev
libcurl4-gnutls-dev
libdbus-glib-1-dev
libdca-dev
libde265-dev
libdirectfb-dev
libdv4-dev
libdvdnav-dev
libdvdread-dev
libegl1-mesa-dev
libexif-dev
libfaac-dev
libfaad-dev
libfdk-aac-dev
libfl-dev
libflac-dev
libfluidsynth-dev
libgdk-pixbuf2.0-dev
libgirepository1.0-dev
libgl1-mesa-dev
libgles2-mesa-dev
libglib2.0-dev
libglu1-mesa-dev
libgraphene-1.0-dev
libgsl-dev
libgtk-3-dev
libgudev-1.0-dev
libiec61883-dev
libjpeg-turbo8-dev
libjson-glib-dev
libkate-dev
liblilv-dev
liblrdf0-dev
libmjpegtools-dev
libmms-dev
libmount-dev
libmpeg2-4-dev
libmpg123-dev
libnice-dev
libogg-dev
libopencore-amrnb-dev
libopencv-dev
libopenjp2-7-dev
libopus-dev
liborc-0.4-dev
libpango1.0-dev
libpangocairo-1.0-0
libpng-dev
libpulse-dev
libquartz-java
libraptor2-dev
libraw1394-dev
librsvg2-dev
librtmp-dev
libsbc-dev
libselinux-dev
libshout3-dev
libsoundtouch-dev
libspandsp-dev
libspeex-dev
libsrtp2-dev
libssh2-1-dev
libtag1-dev
libtheora-dev
libtool
libtwolame-dev
libunwind-dev
libusb-1.0-0-dev
libva-dev
libvisual-0.4-dev
libvo-aacenc-dev
libvorbis-dev
libvorbisidec-dev
libvpx-dev
libwavpack-dev
libwebp-dev
libwebrtc-audio-processing-dev
libx11-dev
libx264-dev
libx265-dev
libxcomposite-dev
libxdamage-dev
libxext-dev
libxfixes-dev
libxi-dev
libxml-simple-perl
libxml2-dev
libxrandr-dev
libxrender-dev
libxtst-dev
libxv-dev
libzbar-dev
make
nettle-dev
ninja-build
pkg-config
python-dev
python-pip
python3-dev
python3-pip
qt5ct
r-cran-gbm
texinfo
transfig
valgrind
wayland-protocols
wget
x11proto-record-dev
xutils-dev
yasm
```