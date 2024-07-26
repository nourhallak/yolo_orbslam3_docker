FROM ubuntu:20.04 as base
ARG DEBIAN_FRONTEND=noninteractive

WORKDIR /yolo_orbslam3

# install nesseccery dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    git \
    wget \
    unzip 

# clone repository 
RUN git clone https://github.com/YWL0720/YOLO_ORB_SLAM3.git 

RUN cd

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

RUN cd 

# install pangolin
RUN apt-get install libglew-dev \
    libboost-dev \
    libboost-thread-dev \
    libboost-filesystem-dev \
    libpython2.7-dev
RUN git clone https://github.com/stevenlovegrove/Pangolin.git && \
    cd Pangolin/ && \
    git checkout v0.5 && \
    mkdir build && \
    cd build && \
    cmake .. && \
    make -j4 && \
    make install

# install eigen
#Eigen
RUN git clone https://gitlab.com/libeigen/eigen.git && \
    cd eigen/ && \
    git checkout 3.3.9 && \
    mkdir build && \
    cd build && \
    cmake .. && \
    make install


CMD ["/bin/bash"]