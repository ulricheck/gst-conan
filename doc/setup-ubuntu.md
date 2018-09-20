# Machine Setup
 
## Ubuntu 18.04, Mint 19 (and maybe Debian)
There are two steps to get `gst-conan` working on your machine.  (We didn't actually try Ubuntu or Debian.) 

### 1. Edit `~/.bashrc`
Put this at the bottom of the file.

```bash
# This is where pip3 installs `--user` executables (such as meson)
PATH=$PATH:$HOME/.local/bin
```

Restart your terminal or execute `source ~/.bashrc`.

### 2. Install stuff
```bash
sudo apt update
sudo apt install --yes git python-pip python3-pip ninja-build build-essential libmount-dev libselinux-dev libasound2-dev libglib2.0-dev libgirepository1.0-dev libxml2-dev libavfilter-dev libgl1-mesa-dev libgles2-mesa-dev libxv-dev
pip3 install setuptools wheel
pip3 install --user meson
pip3 install conan
```