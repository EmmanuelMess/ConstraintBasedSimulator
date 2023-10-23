FROM teeks99/clang-ubuntu:17

ARG DEBIAN_FRONTEND=noninteractive

# Setup compilation deps
RUN apt-get update \
  && apt install -y gdb ninja-build git clang-tidy cppcheck \
  && apt-get clean

# Setup Qt deps
RUN apt update \
  && apt install -y build-essential libgl1-mesa-dev libgstreamer-gl1.0-0 libpulse-dev \
                 libxcb-glx0 libxcb-icccm4 libxcb-image0 libxcb-keysyms1 libxcb-randr0 \
                 libxcb-render-util0 libxcb-render0 libxcb-shape0 libxcb-shm0 libxcb-sync1 \
                 libxcb-util1 libxcb-xfixes0 libxcb-xinerama0 libxcb1 libxkbcommon-dev \
                 libxkbcommon-x11-0 libxcb-xkb-dev \
  && apt install -y libx11-* libx11* libxcb-* libxcb* libxkbcommon-dev libxkbcommon-x11-dev \
  && apt install -y libxcb-cursor0  \
  && apt clean

#install cmake
RUN apt purge -y cmake
ADD https://cmake.org/files/v3.21/cmake-3.21.7-linux-x86_64.sh /cmake-Linux-x86_64.sh
RUN mkdir /opt/cmake
RUN sh /cmake-Linux-x86_64.sh --prefix=/opt/cmake --skip-license
RUN ln -s /opt/cmake/bin/cmake /usr/bin/cmake
RUN cmake --version

# Set the locale
RUN apt update  \
  && apt install -y locales  \
  && apt clean
RUN sed -i '/en_US.UTF-8/s/^# //g' /etc/locale.gen && \
    locale-gen
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8

RUN useradd -ms /bin/bash user

USER user
WORKDIR /home/user