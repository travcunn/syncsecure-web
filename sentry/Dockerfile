FROM syncsecure/python-base


RUN apt-get install -y openssh-server git-core libxml2-dev curl python build-essential make gcc python-dev wget
RUN apt-get install -y postgresql-client-9.1 postgresql-client-common libpq5
RUN apt-get install -y libpq-dev
RUN apt-get install -y mysql-client
RUN apt-get install -y libmysqlclient-dev

RUN pip install psycopg2
RUN pip install sentry
RUN pip install MySQL-python

EXPOSE 9000

ADD sentry.conf.py /sentry.conf.py
ADD admin_user.json /initial_data.json

ENTRYPOINT ["/usr/local/bin/sentry", "--config=/sentry.conf.py"]

CMD ["start"]
