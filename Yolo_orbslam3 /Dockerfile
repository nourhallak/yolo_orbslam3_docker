FROM ubuntu:20.04 as base

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

# install opencv
RUN apt install -y \
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
    libtiff-dev \
    libjasper-dev \
    libdc1394-22-dev
RUN git clone https://github.com/opencv/opencv.git && \
    cd opencv/ && \
    git checkout 4.2 && \
    mkdir build && \
    cd build && \
    cmake -D CMAKE_BUILD_TYPE=Release -D CMAKE_INSTALL_PREFIX=/usr/local ..  && \
    make install

CMD ["/bin/bash", "/run.sh"]