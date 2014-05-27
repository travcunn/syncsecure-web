# Pull base image.
FROM syncsecure/python-base

MAINTAINER Travis Cunningham <travcunn@umail.iu.edu>

# Install app some packages
RUN apt-get install -y python-all python-pip
ADD . /webapp

ENV HOME /webapp
WORKDIR /webapp

EXPOSE 5000

CMD ./production.sh
