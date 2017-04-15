class Command(object):
	def execute(self):
		raise NotImplementedError()

	def cancel(self):
		raise NotImplementedError()

	def name(self):
		raise NotImplementedError()