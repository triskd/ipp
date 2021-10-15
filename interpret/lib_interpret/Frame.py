#!/usr/bin/env

from lib_interpret.Variable import Variable
from lib_interpret.Killer import Killer


class Frame:

	createdFrames = 0

	@classmethod
	def incFramesCount(cls):
		cls.createdFrames += 1

	def __init__(self):
		self.variables = []
		self.id = Frame.createdFrames
		Frame.incFramesCount()		# pocitadlo vytvorenych ramcu

	# pokud promenna existuje v ramci vraci True jinak False
	def existVar(self, varName):
		#kontrola zda jmeno promenne bylo v dlouhem nebo kratkem tvaru
		if len(varName.split('@')) == 2:
			varName = varName.split('@')[1] # pouze kratka cast jmena

		for var in self.variables:
			if var.getName() == varName:
				return True

		return False

	def getVar(self, varName):
		if self.existVar(varName):
			splited = {}
			if '@' in varName:
				splited = Variable.splitFrameAndName(varName)
			else:
				splited['name'] = varName

			for var in self.variables:
				if splited['name'] == var.getName() or varName == var.getLongName():
					return var

		return None

	def addVar(self, varName):
		if not self.existVar(varName):
			self.variables.append(Variable(varName))
		else:
			Killer(52, "Pokus o redefinici promenne v ramci - " + varName)

	def prnt(self):
		print("Frame id: " + str(self.id))
		i = 0
		for var in self.variables:
			print(str(i) + ")")
			var.prnt()
			i += 1