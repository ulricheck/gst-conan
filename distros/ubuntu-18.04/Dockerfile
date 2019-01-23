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
RUN adduser --disabled-password --shell /bin/bash --gecos "User" default_user --uid $USER_UID --home $CONAN_USER_HOME
RUN addgroup sudoers
RUN usermod --append --groups sudoers default_user
RUN echo "\ndefault_user ALL=(ALL) NOPASSWD: ALL\n" >> /etc/sudoers

USER default_user

# install stuff with pip (saves time for the development cycle of gst-conan codebase)
RUN pip3 install setuptools wheel
RUN pip3 install --user meson

RUN pip3 install conan==$CONAN_VERSION

USER root

# Make the relevant folder.
RUN mkdir -p "$CONAN_USER_HOME/.conan/data"
RUN chown -R default_user:default_user "$CONAN_USER_HOME/.conan"

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