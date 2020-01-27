
FROM ubuntu:18.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update
RUN apt-get -y install tzdata sudo

WORKDIR /catana
COPY . /catana

RUN apt-get install -y \
		bc \
		build-essential \
		cmake \
		curl \
        pkg-config \
		g++ \
		gfortran \
		git \
        python2.7 \
        python-pip \
        python3 python3-pip python3-venv python3-dev libpython3-dev python3-setuptools \
        python-metaconfig python3-metaconfig \
        python3-virtualenv python-virtualenv virtualenv \
		libffi-dev \
		libfreetype6-dev \
		libhdf5-dev \
		libjpeg-dev \
		liblcms2-dev \
		libopenblas-dev \
		liblapack-dev \
		libpng-dev \
		libssl-dev \
		libtiff5-dev \
		libwebp-dev \
		libzmq3-dev \
		nano \
		python-dev \
		software-properties-common \
		unzip \
		vim \
		wget \
		zlib1g-dev \
		qt5-default \
		libvtk6-dev \
		zlib1g-dev \
		libjpeg-dev \
		libwebp-dev \
		libpng-dev \
		libtiff5-dev \
		libopenexr-dev \
		libgdal-dev \
		libdc1394-22-dev \
		libavcodec-dev \
		libavformat-dev \
		libswscale-dev \
		libtheora-dev \
		libvorbis-dev \
		libxvidcore-dev \
		libx264-dev \
		yasm \
		libopencore-amrnb-dev \
		libopencore-amrwb-dev \
		libv4l-dev \
		libxine2-dev \
		libtbb-dev \
		libeigen3-dev \
		python-tk \
        ffmpeg \
        && \
	apt-get clean && \
	apt-get autoremove && \
	rm -rf /var/lib/apt/lists/*

RUN  apt-get update && apt-get install -y \
		cython cython3 \
		python-nose python3-nose \
		python-h5py python3-h5py \
		python-skimage python3-skimage \
        python-protobuf python3-protobuf \
        python-openssl python3-openssl \
		python-mysqldb python3-mysqldb \
		libmysqlclient-dev \
        && \
	apt-get clean && \
	apt-get autoremove && \
	rm -rf /var/lib/apt/lists/*

# OpenCV and Dlib related packages
RUN apt-get update && apt-get install -y python3-opencv 

RUN pip3 install numpy scipy matplotlib scikit-image scikit-learn ipython
RUN pip3 --no-cache-dir install -r requirements.txt

RUN pip3 install -U /catana/src 

CMD ["/bin/sleep", "infinity"]

