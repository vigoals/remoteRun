#coding=utf-8
import sys
import optparse
import json

class OptionParser:
	def __init__(self):
		parser = optparse.OptionParser(usage="usage:./main.py [optinos] env")
		parser.add_option('-c', '--configure',
				action = 'store',
				type = 'string',
				dest = 'configure',
				default = 'REMOTERUN.json',
				help="配置文件"
				)
		parser.add_option('-s', '--hostname',
			action = 'store',
			type = 'string',
			dest = 'hostname',
			default = None,
			help="远程主机"
			)
		options, args = parser.parse_args(sys.argv[1:])
		self.optinos = options.__dict__
		self.load(options.configure)

	def byteify(self, input):
		if isinstance(input, dict):
			return {self.byteify(key): self.byteify(value)
					for key, value in input.iteritems()}
		elif isinstance(input, list):
			return [self.byteify(element) for element in input]
		elif isinstance(input, unicode):
			return input.encode('utf-8')
		else:
			return input

	def get(self, key, default=None):
		if self.options.has_key(key):
			return self.options[key]
		elif default is not None:
			self.options[key] = default
			return default
		else:
			return None

	def set(self, key, value):
		self.options[key] = value

	def load(self, configure):
		try:
			f = open(configure, 'r')
			conf = json.load(f)
			conf = self.byteify(conf)
			self.hosts = conf['hosts']
			self.tasks = conf['tasks']
			f.close()
		except IOError:
			print "WARNING: 载入 %s 出错" % configure
			exit()
