FROM ubuntu:20.04 as base
ARG DEBIAN_FRONTEND=noninteractive

WORKDIR /yolo_orbslam3

# Install necessary dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    git \
    wget \
    unzip \
    software-properties-common

# install opencv
RUN apt-get install -y \
    libgtk2.0-dev \
    pkg-config \ 
    libavcodec-dev \
    libavformat-dev \
    libswscale-dev \
    python-dev \
    python-numpy \ 
    libtbb2 \ 
    libtbb-dev \
    libjpeg-dev \
    libpng-dev \
    libtiff-dev 
  
RUN apt-get install -y \
    libdc1394-22-dev 

RUN apt-get install -y \
    libopenjp2-7-dev

RUN git clone https://github.com/opencv/opencv.git && \
    cd opencv/ && \
    git checkout 4.2.0 && \
    mkdir build && \
    cd build && \
    cmake -D CMAKE_BUILD_TYPE=Release -D CMAKE_INSTALL_PREFIX=/usr/local ..  && \
    make install

# install eigen
RUN git clone https://gitlab.com/libeigen/eigen.git && \
    cd eigen/ && \
    git checkout 3.3.9 && \
    mkdir build && \
    cd build && \
    cmake .. && \
    make install
# Add repository for GCC 11 and install it
RUN add-apt-repository ppa:ubuntu-toolchain-r/test && \
    apt-get update && \
    apt-get install -y \
    gcc-11 \
    g++-11

# Set GCC 11 as default
RUN update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-11 100 && \
    update-alternatives --install /usr/bin/g++ g++ /usr/bin/g++-11 100


# install pangolin
RUN apt-get install -y \ 
    libglew-dev \
    libboost-dev \
    libboost-thread-dev \
    libboost-filesystem-dev \
    libpython2.7-dev 
    
RUN git clone https://github.com/stevenlovegrove/Pangolin.git && \
    cd Pangolin/ && \
    git checkout v0.6 && \
    mkdir build && \
    cd build && \
    cmake .. -DCMAKE_C_COMPILER=gcc-11 -DCMAKE_CXX_COMPILER=g++-11 -DCMAKE_CXX_FLAGS="-Wno-catch-value -Wno-deprecated-declarations" -DOpenGL_GL_PREFERENCE=LEGACY && \    
    make -j4 && \
    make install

# install libtorch
RUN wget https://download.pytorch.org/libtorch/cpu/libtorch-cxx11-abi-shared-with-deps-1.11.0%2Bcpu.zip && \
    unzip libtorch-cxx11-abi-shared-with-deps-1.11.0+cpu.zip && \
    mv libtorch /yolo_orbslam3/Thirdparty

RUN apt-get install pip -y
RUN pip install torch torchvision

# install extra libraries
RUN apt-get install libssl-dev -y  


# Set the Torch_DIR environment variable
RUN export Torch_DIR=/yolo_orbslam3/Thirdparty/libtorch/share/cmake/Torch
ENV CMAKE_PREFIX_PATH=${CMAKE_PREFIX_PATH}:/yolo_orbslam3/Thirdparty/libtorch

# copy repository into container
COPY /YOLO_ORB_SLAM3 /yolo_orbslam3

RUN cd /yolo_orbslam3
RUN chmod +x build.sh
RUN ./build.sh

CMD ["/bin/bash"]