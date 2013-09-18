import select
from subprocess import Popen, PIPE
import sys
import time
from optparse import OptionParser


class StreamCommandRunner(object):

	def __init__(self, command, sleep_time):
		self.command = command
		self.sleep_time = sleep_time
		self.last_time = None
		self.read_last_time = True

	def _accumulate_input(self):
		time_to_stop_after = self.last_time + self.sleep_time
		lines = []
		new_time = time.time()

		while new_time < time_to_stop_after:
			if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
				lines.append(sys.stdin.readline())
				self.read_last_time = True
			elif self.read_last_time:
				self.read_last_time = False
			else:
				time.sleep(1)
			new_time = time.time()

		self.last_time = new_time

		return ''.join(lines)

	def loop_indefinitely(self):
		self.last_time = time.time()
		while True:
			Popen(
				[self.command],
				shell=True,
				stdin=PIPE,
			).communicate(self._accumulate_input())


if __name__ == '__main__':
	parser = OptionParser()
	parser.add_option('-s', '--sleep-time', dest="sleep_time", action="store", type="float", default=1.0)
	parser.add_option('-c', '--command', dest="command", action="store", default='cat')
	options, _ = parser.parse_args()
	StreamCommandRunner(options.command, options.sleep_time).loop_indefinitely()
