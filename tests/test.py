#!/usr/bin/python3

import unittest
import time
import subprocess
import sys
import os

logfiles = []
with open(os.path.join(os.path.dirname(sys.argv[0]), "blockade.yml")) as f:
    for line in f:
        tup = [x.strip() for x in line.split(':', 1)]
        if len(tup) < 2:
            continue
        k, v = tup
        if k == 'LOG':
            filename = v.strip("'")
            print('will also log to %s' % filename)
            logfiles.append(filename)

def log_to_everybody(line):
    for filename in logfiles:
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

def log_is_ok(filename):
    if 'client' in filename:
        longest = 0
        fail_streak = 0
        with open(filename) as f:
            for line in f:
                if 'query failed' in line:
                    fail_streak += 1
                    if fail_streak > longest:
                        longest = fail_streak
                elif ' = ' in line:
                    fail_streak = 0
        print("%s longest fail streak = %d" % (filename, longest))
        return longest < 2
    elif 'server' in filename:
        return True
    else:
        return False

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

        for filename in logfiles:
            self.assertTrue(log_is_ok(filename))

if __name__ == '__main__':
    unittest.main()

# vim: ai ts=4 sts=4 et sw=4
