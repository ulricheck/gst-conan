# consume-ges
In this example, we create a C++ project which consumes `gst-editing-services`.  Before running the example, it is
necessary to create the conan packages first.  You can do this from the shell as follows.

```bash
# From the root folder of this repo:
./gst-conan create --rev 1.14.3 --version 1.14.3 --build_type Debug --user my_conan_user --channel my_conan_channel

```

The values in the command above must match the values at the top of the `conanfile.py` in this folder.
 
```python
# Top of conanfile.py for consume-ges example
GST_CONAN_VERSION="1.14.3"
GST_CONAN_USER="my_conan_user"
GST_CONAN_CHANNEL="my_conan_channel"
```

To build the example:

```bash
cd examples/consume-ges
conan install . -s build_type=Debug
conan build .
```

Once the example is built, you should be able to execute the program that you just built.

```bash
build/run.sh
```

You should see that GES has initialized successfully.