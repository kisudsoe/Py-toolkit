FROM ubuntu:latest
WORKDIR /

MAINTAINER Seungsoo_Kim

RUN sudo apt update -y && \
    sudo apt upgrade -y

# Install dependencies
RUN apt install -y \
    wget \
    bedtools \
    vim \
    python \
    python-pip