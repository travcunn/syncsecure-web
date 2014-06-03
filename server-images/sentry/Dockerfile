FROM syncsecure/base

#RUN echo "deb http://archive.ubuntu.com/ubuntu precise main universe" > /etc/apt/sources.list
#RUN apt-get update

#RUN apt-get install -y language-pack-en
#ENV LANGUAGE en_US.UTF-8
#ENV LANG en_US.UTF-8
#ENV LC_ALL en_US.UTF-8

RUN locale-gen en_US.UTF-8
RUN dpkg-reconfigure locales

RUN apt-get install -y \
    openssh-server \
    libxml2-dev \
    python \
    build-essential \
    make \
    gcc \
    python-dev \
    python-pip \
    wget

RUN pip install sentry

RUN apt-get install -y postgresql-client postgresql-client-common libpq5
RUN apt-get install -y libpq-dev

RUN pip install psycopg2

EXPOSE 9000
VOLUME ["/data"]

ADD sentry.conf.py /sentry.conf.py
ADD sentry.db /data/sentry.db

ENTRYPOINT ["/usr/local/bin/sentry", "--config=/sentry.conf.py"]
CMD ["start"]
