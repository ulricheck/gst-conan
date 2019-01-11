# Machine Setup
Currently, I have only used `gst-conan` on `Linux Mint 19`.

## Ubuntu 18.04, Mint 19 (and similar Debians)

Install Docker.

```bash
apt-get update && apt-get install --yes python3 python3-pip

pip3 install setuptools wheel
pip3 install --user meson 
pip3 install conan
``` 