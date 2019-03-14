FROM nvidia/cudagl:10.0-devel-ubuntu18.04

ENV DEBIAN_FRONTEND noninteractive

# install python3
RUN apt-get update \
    && apt-get install --yes apt-utils python3 python3-pip sudo

# install all debian packages up front (saves time for the development cycle of gst-conan codebase)
COPY distros/ubuntu-18.04/debians-build.txt /tmp/debians-build.txt
RUN apt-get update && apt-get install --yes $(cat /tmp/debians-build.txt | tr '\r\n' ' ' | tr '\n' ' ')
RUN sudo apt-get clean
RUN rm /tmp/debians-build.txt

# meson will not run as the 'root' user so we need to create another user
RUN addgroup sudoers
RUN adduser --disabled-password --shell /bin/bash --gecos "User" default_user
RUN usermod --append --groups sudoers default_user
RUN echo "\ndefault_user ALL=(ALL) NOPASSWD: ALL\n" >> /etc/sudoers

USER default_user

# install stuff with pip (saves time for the development cycle of gst-conan codebase)
RUN pip3 install setuptools wheel
RUN pip3 install --user meson

# The following 'conan' args must match the user's system.  We need to install the same version of conan as the user.
# We must use the same storage folder as the user so that conan packages can be debugged by the consumer (debug symbols
# will point to absolute paths on the system where compilation occurred).
ARG CONAN_STORAGE_PATH
ARG CONAN_VERSION

ENV CONAN_STORAGE_PATH "$CONAN_STORAGE_PATH"

RUN pip3 install conan==$CONAN_VERSION

USER root

# make this folder exists and is owned by default_user
#     otherwise it would be owned by root when mounted from a `docker run` command.
RUN mkdir -p "$CONAN_STORAGE_PATH"
RUN chown -R default_user "$CONAN_STORAGE_PATH"

# deploy gst-conan
COPY config/ /opt/gst-conan/config
COPY gst_conan/ /opt/gst-conan/gst_conan
COPY packages/ /opt/gst-conan/packages
COPY gst-conan /opt/gst-conan/gst-conan
RUN chmod 755 /opt/gst-conan/gst-conan

USER default_user

# setup path
RUN echo "\n\nPATH=\${HOME}/.local/bin:\${PATH}\n" >> ~/.bashrc
ENV PATH=${PATH}:/opt/gst-conan

# setup conan storage path
RUN bash --login -c "conan config set storage.path=\"$CONAN_STORAGE_PATH\""
RUN bash --login -c "conan user"
RUN bash --login -c "conan remote add bincrafters \"https://api.bintray.com/conan/bincrafters/public-conan\""
RUN bash --login -c "conan remote add camposs \"https://conan.campar.in.tum.de/api/conan/conan-camposs\""
RUN bash --login -c "conan remote add ubitrack \"https://conan.campar.in.tum.de/api/conan/conan-ubitrack\""
RUN bash --login -c "conan remote add vendor \"https://conan.campar.in.tum.de/api/conan/conan-vendor\""
RUN bash --login -c "conan profile new default --detect"
RUN bash --login -c "conan profile update settings.compiler.libcxx=libstdc++11 default"

ENTRYPOINT ["bash", "--login", "-c"]
CMD ["echo", "hello world"]