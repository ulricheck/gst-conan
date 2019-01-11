### `packages.json`
Information about each conan package.

## bug workaround
This same exact folder exists next to every `conanfile.py` in this repo because we are working around a known
[bug](https://github.com/conan-io/conan/issues/3591).

See also the `copy_exports_workaround` command in the command-line API.