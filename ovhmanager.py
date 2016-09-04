# -*- encoding: utf-8 -*-

import ovh, requests, ssl, json
import ovh.exceptions as oexcept

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    # Legacy Python that doesn't verify HTTPS certificates by default
    pass
else:
    # Handle target environment that doesn't support HTTPS verification
    ssl._create_default_https_context = _create_unverified_https_context

class OvhManager:
	def __init__(self, **kwargs):
		self.action = {}

		if kwargs.get('AK') and kwargs.get('AS') and kwargs.get('CK'):
			self.api = ovh.Client(
				endpoint='ovh-eu', 
				application_key = kwargs.get('AK'),
				application_secret = kwargs.get('AS'),
				consumer_key = kwargs.get('CK')
			)
		else:
			raise Exception('Please, fill correctly the config file config.cfg.')


		if kwargs.get('email'):
			self.mail = kwargs.get('email')
		else:
			raise Exception('Please, provide an email address.')


		#aliases = self.api.get('/email/exchange/organization-pa87097-1/service/hosted-pa87097-1/account/hello@anthonypradal.com/alias/')
		#print aliases

		self._findApiPath()
		#self.deleteAlias("test2@anthonypradal.com")

	def _findApiPath(self):
		#  /email/exchange
		email = None
		for org in self.api.get('/email/exchange'):
			# /email/exchange/{organizationName}/service
			for service in self.api.get('/email/exchange/{}/service'.format(org)):
				# /email/exchange/{organizationName}/service/{exchangeService}/account
				for mail in self.api.get('/email/exchange/{}/service/{}/account'.format(org, service)):
					if self.mail == mail:
						self.organization = org
						self.service = service
						email = mail

		if not email:
			raise Exception('Exchange account unknow.')


	def getAlias(self):
		self.alias = []
		alias = self.api.get('/email/exchange/{}/service/{}/account/{}/alias/'.format(
			self.organization, self.service, self.mail))

		for al in alias:
			#  /email/exchange/{organizationName}/service/{exchangeService}/account/{primaryEmailAddress}/alias/{alias}
			details = self.api.get('/email/exchange/{}/service/{}/account/{}/alias/{}'.format(
				self.organization, self.service, self.mail, al))


			# Check status (0: OK, 1: Add, 2: Del, 3: Unk)
			status = 0
			print self.action, al
			try:
				if details['taskPendingId'] == 0: status = 0
				elif self.action[al.split("@")[0]] == "deleting": status = 2
				else: status = 1
			except:
				status = 3

			self.alias.append([al.split("@")[0], al.split("@")[1], status])

		return self.alias



	def addAlias(self, post_alias):
		# /email/exchange/{organizationName}/service/{exchangeService}/account/{primaryEmailAddress}/alias
		try:
			result = self.api.post('/email/exchange/{}/service/{}/account/{}/alias'.format(
				self.organization, self.service, self.mail), alias = "{}@{}".format(post_alias, self.mail.split("@")[1]))
			self.action[post_alias] = "adding"
		except oexcept.ResourceConflictError:
			return 409 # Conflict Error
		return 200


	def deleteAlias(self, alias):
		print "Deleting", alias
		# /email/exchange/{organizationName}/service/{exchangeService}/account/{primaryEmailAddress}/alias/{alias}
		try:
			result = self.api.delete('/email/exchange/{}/service/{}/account/{}/alias/{}@{}'.format(
				self.organization, self.service, self.mail, alias, self.mail.split("@")[1]))

			self.action[alias] = "deleting"
		except oexcept.ResourceConflictError:
			return 408 # ConflictError, Pending task or invalid alias

		print json.dumps(result, indent=4)
















	