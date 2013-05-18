import select
from subprocess import Popen, PIPE
import sys
import time
from optparse import OptionParser

if __name__ == '__main__':
	parser = OptionParser()
	parser.add_option('-s', '--sleep-time', dest="sleep_time", action="store", type="float")
	parser.add_option('-c', '--command', dest="command", action="store")
	options, _ = parser.parse_args()
	while True:
		time.sleep(options.sleep_time)
		lines = []
		while sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
			lines.append(sys.stdin.readline())
		Popen(
			[options.command],
			shell=True,
			stdin=PIPE,
		).communicate(''.join(lines))
