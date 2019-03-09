

class Debugger:
	is_debug_on = True
	
	@staticmethod
	def printD(*msg):
		if Debugger.is_debug_on:
			print(*msg)
		