#!/usr/bin/python3

import unittest
import time
import subprocess

def log_to_everybody(line):
    for name in 'client-hello client-world server-10 server-20 server-30'.split():
        filename = '/tmp/%s.log' % name
        with open(filename, 'a') as f:
            print(line, file=f)
    print(line)

def blockade_partition(name):
    log_to_everybody("=== partition %s away" % name)
    subprocess.check_call(['blockade','partition', name])
    subprocess.check_call(['blockade','status'])
    log_to_everybody("=== %s partitioned away" % name)

def blockade_join():
    log_to_everybody("=== join the network")
    subprocess.check_call(['blockade','join'])
    subprocess.check_call(['blockade','status'])
    log_to_everybody("=== the network joined")

def blockade_up():
    log_to_everybody("=== set up blockade")
    subprocess.check_call(['blockade','up'])
    log_to_everybody('=== blockade is up')

def blockade_destroy():
    log_to_everybody("=== destroy blockade")
    subprocess.check_call(['blockade','destroy'])
    log_to_everybody("=== blockade destroyed")

class PartitionTest(unittest.TestCase):
    def test_node_partition(self):
        log_to_everybody("=== test_node_partition")
        blockade_up()
        try:
            time.sleep(20)

            for serverid in range(1,4):
                name = "server%d" % serverid
                blockade_partition(name)
                time.sleep(10)
                blockade_join()
                time.sleep(10)
        finally:
            blockade_destroy()

if __name__ == '__main__':
    unittest.main()

# vim: ai ts=4 sts=4 et sw=4
