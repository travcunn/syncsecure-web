# Pull base image.
FROM syncsecure/python-base

MAINTAINER Travis Cunningham <travcunn@umail.iu.edu>

# Install app
ADD . /webapp
# Install statd worker
ADD ../statsd_scripts/stats_collector.py /stats

ENV HOME /webapp
WORKDIR /webapp

EXPOSE 8000

RUN apt-get install libzmq-dev -y

RUN pip install circus
RUN pip install -r requirements.txt

CMD ["circus.ini"]
ENTRYPOINT ["/usr/local/bin/circusd"]
