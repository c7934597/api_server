# Path: deploy/Dockerfile.prod
# FROM nvcr.io/nvidia/cuda:11.7.1-cudnn8-devel-ubuntu20.04 as prod
FROM python:3.12.0-slim-bullseye as prod

# Set the timezone non-interactively
ENV TZ=Asia/Taipei
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Update the package list in the container and install the build dependencies for Python
RUN apt-get update && apt-get install -y \
    build-essential \
    wget \
    zlib1g-dev \
    libncurses5-dev \
    libgdbm-dev \
    libnss3-dev \
    libssl-dev \
    libreadline-dev \
    libffi-dev \
    libsqlite3-dev \
    libbz2-dev \
    liblzma-dev \
    tk-dev \
    libdb-dev \
    libbluetooth-dev \
    libdb5.3-dev \
    libdb5.3++-dev \
    libgpm-dev \
    libxslt1-dev \
    libxml2-dev \
    libxslt-dev \
    libzstd-dev \
    libffi-dev

# Download and install the source code for Python 3.12.0
WORKDIR /tmp
RUN wget https://www.python.org/ftp/python/3.12.0/Python-3.12.0.tgz &&\
    tar -xf Python-3.12.0.tgz && \
    rm -rf Python-3.12.0.tgz &&\
    # Download and install the source code for Python 3.12.0
    ./Python-3.12.0/configure --enable-optimizations &&\
    make -j$(nproc) &&\
    make altinstall &&\
    pip3.12 install --upgrade pip &&\
    pip3.12 install poetry==1.5.1 &&\
    # Configuring poetry
    poetry config virtualenvs.create false

# Working directory
WORKDIR /app/src

# Copying actuall application and requirements of a project
COPY . /app/src/

# Installing requirements
RUN poetry install

EXPOSE 8000

CMD ["/usr/local/bin/python3.12", "-m", "api_server"]
