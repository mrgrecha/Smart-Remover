class Command(object):
	def execute(self, list, my_trash):
		raise NotImplementedError()

	def cancel(self):
		raise NotImplementedError()

	def name(self, list):
		raise NotImplementedError()