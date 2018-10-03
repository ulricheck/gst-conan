# Machine Setup
Currently, I have only used `gst-conan` on `Linux Mint 19`.

## Ubuntu 18.04, Mint 19 (and similar Debians)
There are two steps to get `gst-conan` working on your machine.  (I only tested this on Mint 19.) 

### 1. Edit `~/.bashrc`
Put this at the bottom of the file.

```bash
# This is where pip3 installs `--user` executables (such as meson)
PATH=$PATH:$HOME/.local/bin
```

Restart your terminal or execute `source ~/.bashrc`.

### 2. Install stuff
```bash
sudo ./gst-conan setup
```

## Other Linux Distros
This was not tested on any other Linux distros.  It should work if you can figure out how to install
the correct packages.

## Windows
This will not work on Windows, but maybe one day.

## Darwin (Mac)
This will not work on Darwin, but maybe one day.