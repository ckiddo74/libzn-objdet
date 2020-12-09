FROM nvidia/cuda:10.1-runtime-ubuntu16.04

# python and basic dev support
RUN apt-get update && apt-get install -y --no-install-recommends apt-utils software-properties-common git curl wget unzip python3 python3-dev nano telnet && \
    curl https://bootstrap.pypa.io/get-pip.py -o /tmp/get-pip.py && python3 /tmp/get-pip.py && pip3 install --upgrade pip

# ZMQ
ARG ZMQ_VERSION="4.3.3"
ARG CPPZMQ_VERSION="4.7.0"
RUN apt-get install -y --no-install-recommends libtool pkg-config build-essential automake libsodium-dev && \
     git clone --depth 1 --branch v${ZMQ_VERSION} https://github.com/zeromq/libzmq.git /tmp/libzmq && \
     cd /tmp/libzmq && ./autogen.sh && ./configure --prefix=/usr && make -j all && make install && ldconfig && \
     wget https://github.com/zeromq/cppzmq/archive/v${CPPZMQ_VERSION}.tar.gz -O /tmp/cppzmq.tgz && \
     cd /tmp && tar xzvf /tmp/cppzmq.tgz && cd /tmp/cppzmq-${CPPZMQ_VERSION} && cp *.hpp /usr/include && \
     pip3 install --no-binary=:all: pyzmq

# OpenCV support + camera
RUN apt-get install -y --no-install-recommends libopencv-dev && \
    pip install opencv-python matplotlib pillow

# tensorflow + edge detection
RUN apt-get install -y libcudnn7 && \
    wget -O /tmp/protobuf.zip https://github.com/google/protobuf/releases/download/v3.0.0/protoc-3.0.0-linux-x86_64.zip && \
    unzip -d /usr /tmp/protobuf.zip && \
    pip3 install tensorflow


RUN mkdir /workspace && \
    cd /workspace && \
    git clone https://github.com/tensorflow/models.git && \
    cd /workspace/models/research && \
    protoc object_detection/protos/*.proto --python_out=.

# install zn library
RUN git clone https://github.com/ckiddo74/libzn.git /tmp/libzn && \
    cd /tmp/libzn && make install_python install_cpp

RUN echo "export PYTHONPATH=/workspace/models/research:/workspace/models/research/slim:/workspace/models/research/object_detection:/workspace" >> /root/.bashrc
RUN echo "export QT_X11_NO_MITSHM=1" >> /root/.bashrc









