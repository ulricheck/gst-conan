# consume-ges
In this example, we write a C++ project which consumes `gst-editing-services`.  Before running the example, it is
necessary to create the conan packages first.  You can do this from the shell as follows.

```bash
# From the root folder of this repo:
./gst-conan create --rev 1.14.3 --version 1.14.3 --buildtype Debug --user my_conan_user --channel my_conan_channel
```

Notice how we reference the same values at the top of the `conanfile.py` file (within this folder).
The values in the file must match the values used in the expression above.
 
```python
GST_CONAN_VERSION="1.14.3"
GST_CONAN_USER="my_conan_user"
GST_CONAN_CHANNEL="my_conan_channel"
```