FROM ubuntu:latest

ARG DEBIAN_FRONTEND=noninteractive
COPY . /home
WORKDIR /home

RUN bash
RUN apt-get update && \
    apt-get install -y apt-utils qalc
