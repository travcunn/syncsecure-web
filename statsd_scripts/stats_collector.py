#http://blog.jupo.org/2013/08/29/devops-eye-for-the-coding-guy-metrics/
import os
import time

import psutil
import graphitesend
from raven import Client


raven_client = Client()

g = graphitesend.init(graphite_server='192.168.0.5', graphite_port=2003)
last_disk_io  = psutil.disk_io_counters()
last_net_io   = psutil.net_io_counters()
time.sleep(1)


def io_change(last, current):
    return dict([(f, getattr(current, f) - getattr(last, f))
                 for f in last._fields])

while True:
    memory          = psutil.phymem_usage()
    disk            = psutil.disk_usage("/")
    disk_io         = psutil.disk_io_counters()
    disk_io_change  = io_change(last_disk_io, disk_io)
    net_io          = psutil.net_io_counters()
    net_io_change   = io_change(last_net_io, net_io)
    last_disk_io    = disk_io
    last_net_io     = net_io

    gauges = {
        "memory_used":        memory.used,
        "memory_free":        memory.free,
        "memory_percent":     memory.percent,
        "cpu_percent":        psutil.cpu_percent(),
        "load":               os.getloadavg()[0],
        "disk_size_used":     disk.used,
        "disk_size_free":     disk.free,
        "disk_size_percent":  disk.percent,
        "disk_read_bytes":    disk_io_change["read_bytes"],
        "disk_read_time":     disk_io_change["read_time"],
        "disk_write_bytes":   disk_io_change["write_bytes"],
        "disk_write_time":    disk_io_change["write_time"],
        "net_in_bytes":       net_io_change["bytes_recv"],
        "net_in_errors":      net_io_change["errin"],
        "net_in_dropped":     net_io_change["dropin"],
        "net_out_bytes":      net_io_change["bytes_sent"],
        "net_out_errors":     net_io_change["errout"],
        "net_out_dropped":    net_io_change["dropout"]
    }

    thresholds = {
        "memory.percent":     80,
        "disk.size.percent":  90,
        "queue.pending":      20000,
        "load":               20,
    }

    for name, value in gauges.items():
        g.send(name, value)
        threshold = thresholds.get(name, None)
        if threshold is not None and value > threshold:
            bits = (threshold, name)
            message = "Threshold of %s reached for %s" % bits
            raven_client.captureMessage(message)
    

    time.sleep(1)
