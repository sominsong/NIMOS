FROM ubuntu:latest

ARG DEBIAN_FRONTEND=noninteractive
COPY . /home
WORKDIR /home

RUN apt-get update && \
    apt-get install -y ghostscript
