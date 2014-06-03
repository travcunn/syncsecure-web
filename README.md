syncsecure-web
==============

linux tweaks to support higher load:
http://code.mixpanel.com/2010/10/29/gevent-the-good-the-bad-the-ugly/

other tweaks:
https://github.com/rebill/storm/blob/master/README.md


Docker images
=============
**Building:**

The Docker containers can be found in /server-images.

Each service runs in a separate Docker container.
To build all of the Docker images, run:

    make build
    
To build an individual image, you can "make" any of them:

    make webserver
