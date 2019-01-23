FROM ubuntu:18.04

ENV DEBIAN_FRONTEND noninteractive

# The following parameters must match the user's system.
ARG CONAN_USER_HOME
ARG CONAN_VERSION
ARG USER_UID=1000

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
RUN adduser --disabled-password --shell /bin/bash --gecos "User" default_user --uid $USER_UID --gid $USER_UID
RUN usermod --append --groups sudoers default_user
RUN echo "\ndefault_user ALL=(ALL) NOPASSWD: ALL\n" >> /etc/sudoers

USER default_user

# install stuff with pip (saves time for the development cycle of gst-conan codebase)
RUN pip3 install setuptools wheel
RUN pip3 install --user meson

ENV CONAN_USER_HOME "$CONAN_USER_HOME"

RUN pip3 install conan==$CONAN_VERSION

USER root

# make this folder exists and is owned by default_user
#     otherwise it would be owned by root when mounted from a `docker run` command.
RUN mkdir -p "$CONAN_USER_HOME"
RUN chown -R default_user "$CONAN_USER_HOME"

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

ENTRYPOINT ["bash", "--login", "-c"]
CMD ["echo", "hello world"]