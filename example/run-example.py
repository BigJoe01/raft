#!/usr/bin/python3

import time
import wtfexpect

try:
	with wtfexpect.WtfExpect() as we:
		servers = 'alpha bravo conan'.split()
		clients = 'xenon yeast zebra'.split()
		serverids = {name: i for i, name in enumerate(servers)}

		cfg = []
		baseport = 6000
		for i in range(len(servers)):
			cfg.append('-r')
			cfg.append("%d:%s:%d" % (i, "127.0.0.1", baseport + i))

		for i, s in enumerate(servers):
			we.spawn(s, 'bin/server',
				'-i', str(i),
				*cfg,
			)

		for c in clients:
			time.sleep(0.333)
			we.spawn(c, 'bin/client', '-k', c, *cfg)

		while we.alive():
			timeout = 0.5
			name, line = we.readline(timeout)
			if name is None: continue

			if line is None:
				code = we.getcode(name)
				if name in servers:
					print("%d(%s) finished with code %d" % (serverids[name], name, code))
				else:
					print("%s finished with code %d" % (name, code))
			else:
				if name in servers:
					print("[%d(%s)] %s" % (serverids[name], name, line))
				else:
					print("[%s] %s" % (name, line))
except KeyboardInterrupt:
	print("killed")
