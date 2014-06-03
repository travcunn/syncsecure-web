# Pull base image.
FROM syncsecure/python-base

MAINTAINER Travis Cunningham <travcunn@umail.iu.edu>

# Install app
ADD . /webapp
# Install stats collector
ADD ../../monitoring/stats/stats_collector.py /stats
ADD ../../monitoring/stats/requirements.txt /stats
RUN pip install -r /stats/requirements.txt

# Set the default directory for our environment
ENV HOME /webapp
WORKDIR /webapp

EXPOSE 8000

RUN apt-get install libzmq-dev -y

RUN pip install circus
RUN pip install -r requirements.txt

CMD ["circus.ini"]
ENTRYPOINT ["/usr/local/bin/circusd"]
