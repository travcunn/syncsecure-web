# Pull base image.
FROM syncsecure/python-base

MAINTAINER Travis Cunningham <travcunn@umail.iu.edu>

# Install app some packages
ADD . /webapp

ENV HOME /webapp
WORKDIR /webapp

EXPOSE 5000

RUN pip install -r requirements.txt
CMD ./production.sh
