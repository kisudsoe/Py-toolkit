FROM ubuntu:latest
WORKDIR /

MAINTAINER Seungsoo_Kim

RUN apt update -y && \
    apt upgrade -y

# Install dependencies
RUN apt install -y \
    wget \
    bedtools \
    vim \
    python
#python-pip