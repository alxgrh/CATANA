#!/bin/sh

rm -rf CATANA
git clone https://github.com/alxgrh/CATANA > /dev/null

cd CATANA/
git checkout devel_2020
git pull

export DEBIAN_FRONTEND=noninteractive
apt-get update > /dev/null

apt-get install -y \
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
        ffmpeg > /dev/null

	apt-get clean && \
	apt-get autoremove && \
	rm -rf /var/lib/apt/lists/* 

apt-get update && apt-get install -y \
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


apt-get update && apt-get install -y python3-opencv 


echo Install NVIDIA CUDA
sudo apt-get purge nvidia*
sudo apt-get autoremove
sudo apt-get autoclean
sudo apt-key adv --fetch-keys http://developer.download.nvidia.com/compute/cuda/repos/ubuntu1804/x86_64/7fa2af80.pub
echo "deb https://developer.download.nvidia.com/compute/cuda/repos/ubuntu1804/x86_64 /" | sudo tee /etc/apt/sources.list.d/cuda.list

sudo apt-get update 
sudo apt-get -o Dpkg::Options::="--force-overwrite" install cuda-10-0 cuda-drivers

wget 'https://www.dropbox.com/s/wttt99al6y3qo2k/libcudnn7_7.6.5.32-1%2Bcuda10.0_amd64.deb'
dpkg -i libcudnn7_7.6.5.32-1+cuda10.0_amd64.deb 


pip3 install numpy scipy matplotlib scikit-image scikit-learn ipython

pip3 --no-cache-dir install -U -r requirements.txt

pip3 install -U ./src 


pip3 uninstall  -qqq  tensorflow
pip3 uninstall  -qqq tensorflow-gpu
pip3 install --no-cache-dir -qqq tensorflow-gpu==1.14.0

cd ..
cd CATANA/src/face_recognition/cython_full
python3 setup.py install


cd -
