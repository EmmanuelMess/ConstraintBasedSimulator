FROM gcc:13.2.0

# Setup compilation deps
RUN apt update \
  && apt install -y cmake gdb ninja-build git clang-tidy cppcheck \
  && apt clean
  
# Setup Qt deps
RUN apt update \
  && apt install -y build-essential libgl1-mesa-dev libgstreamer-gl1.0-0 libpulse-dev \
                 libxcb-glx0 libxcb-icccm4 libxcb-image0 libxcb-keysyms1 libxcb-randr0 \
                 libxcb-render-util0 libxcb-render0 libxcb-shape0 libxcb-shm0 libxcb-sync1 \
                 libxcb-util1 libxcb-xfixes0 libxcb-xinerama0 libxcb1 libxkbcommon-dev \
                 libxkbcommon-x11-0 libxcb-xkb-dev \
  && apt clean

RUN useradd -ms /bin/bash user

USER user
WORKDIR /home/user
