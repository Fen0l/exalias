#!/usr/bin/env python2.7
# -*- encoding: utf-8 -*-

import os.path
import random, time

import ConfigParser, os

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

import ovhmanager as ovhm

from tornado.options import define, options
define("port", default=8888, help="run on the given port", type=int)

from tornado.log import enable_pretty_logging
enable_pretty_logging()

class IndexHandler(tornado.web.RequestHandler):
	def get(self):
		# Deleting alias
		try:
			if self.get_argument('delete'):
				API_OVH.deleteAlias(self.get_argument('delete'))
		except: pass

		# Adding alias
		try:
			if self.get_argument('add'):
				API_OVH.addAlias(self.get_argument('add'))
		except: pass

		self.email = config.get('Exchange', 'account')
		self.alias = API_OVH.getAlias()
		self.render('index.html', exchange_email = self.email, alias = self.alias)

if __name__ == '__main__':
	# Parse config file
	config = ConfigParser.ConfigParser()
	config.readfp(open('config.cfg'))

	API_OVH = ovhm.OvhManager(
		AK = config.get('OVH_API', 'application_key'),
		AS = config.get('OVH_API', 'application_secret'),
		CK = config.get('OVH_API', 'consumer_key'),
		email = config.get('Exchange', 'account'))

	## Launch Tornado
	tornado.options.parse_command_line()
	app = tornado.web.Application(
		handlers=[(r'/', IndexHandler)],
		template_path = os.path.join(os.path.dirname(__file__), "templates"),
		static_path = os.path.join(os.path.dirname(__file__), "static"),
		debug = True 
	)

	http_server = tornado.httpserver.HTTPServer(app)
	http_server.listen(options.port)
	tornado.ioloop.IOLoop.instance().start()





