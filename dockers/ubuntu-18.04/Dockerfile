FROM ubuntu:18.04

# install python3
RUN apt-get update \
    && apt-get install --yes apt-utils python3 python3-pip sudo

# install all debian packages up front (saves time for the development cycle of gst-conan codebase)
ENV DEBIAN_FRONTEND noninteractive
COPY dockers/ubuntu-18.04/debians.txt /tmp/debians.txt
RUN apt-get install --yes $(cat /tmp/debians.txt | tr '\r\n' ' ' | tr '\n' ' ')
RUN sudo apt-get clean
RUN rm /tmp/debians.txt

# meson will not run as the 'root' user so we need to create another user
RUN addgroup sudoers
RUN adduser --disabled-password --shell /bin/bash --gecos "User" default_user
RUN usermod --append --groups sudoers default_user
RUN echo "\ndefault_user ALL=(ALL) NOPASSWD: ALL\n" >> /etc/sudoers

USER default_user

# install stuff with pip (saves time for the development cycle of gst-conan codebase)
RUN pip3 install setuptools wheel
RUN pip3 install --user meson
RUN pip3 install conan

# make this folder owned by default_user
#     otherwise, when it gets mounted during `docker run` the folder will be owned by root.
RUN mkdir -p ~/.conan/data

USER root

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
CMD ["bash"]