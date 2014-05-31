# Dockerfile for the base image

# Pull base image.
FROM ubuntu:14.04

MAINTAINER Travis Cunningham <travcunn@umail.iu.edu>

# Update OS
RUN sed -i 's/# \(.*multiverse$\)/\1/g' /etc/apt/sources.list
RUN  apt-get update
RUN apt-get -y upgrade
