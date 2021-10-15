#!/usr/bin/env

from lib_interpret.Killer import Killer


class Variable:

	# v argumentu dic {'value' : , 'type'} kontroluje zda hodnota value je datoveho typu type
	# vraci True pokud kontrola je v poradku, jinak false
	@staticmethod
	def checkValueIsType(dic):
		try: 
			dic['value']
			dic['type']
		except:
			Killer(99, "Spatny argument funkce Variable.checkValueIsType()")

		if dic['type']	== 'int':
			if type(dic['value']) == int:
				return True
			else:
				try:
					int(dic['value'])
					return True
				except:
					return False

		if dic['type'] == 'string':
			if type(dic['value']) == str:
				return True

		if dic['type'] == 'bool':
			if dic['value'] == 'true' or dic['value'] == 'false':
				return True

		if dic['type'] == 'nil' and dic['value'] == 'nil':
			return True

		if dic['type'] == 'var' and len(dic['value'].split('@')) == 2:
			return True 

		if dic['type'] == 'type' and (dic['value'] == 'int' or dic['value'] == 'bool' or dic['value'] == 'string'):
			return True

		if dic['type'] == 'label' and type(dic['value']) == str:
			return True

		return False

	@staticmethod
	def splitFrame(varLongName):
		try:
			return varLongName.split('@')[0]
		except:
			Killer(99, "Vnitrni chyba prekladece staticmethod Variable.splitFrame()")

	@staticmethod
	def splitFrameAndName(varLongName):
		try:
			split = varLongName.split('@')
			ret = {'frame' : split[0], 'name' : split[1]}
			return ret
		except:
			Killer(99, "Vnitrni chyba prekladece staticmethod Variable.splitFrameAndName()")


	def __init__(self, longName):
		self.value = 'nil'
		self.type = 'nil'
		self.frame = longName.split('@')[0]
		self.name = longName.split('@')[1]
		self.longName = longName
		self.defined = False

	def getValue(self):
		return self.value

	def getType(self):
		return self.type

	def getFrame(self):
		return self.frame

	def getLongName(self):
		return self.longName

	def getName(self):
		return self.name

	#vraci 0 pokud promenna byla nastavena
	#parametr v je dict {'type': dType, 'value': hodnota}
	def set(self, v):
		try:
			v['type']
			v['value']	
		except:
			Killer(99, "Vnitrni chyba interpretu, Variabale.set()")

		if v['type'] == 'int' or v['type'] == 'string' or v['type'] == 'bool' or v['type'] == 'nil':
			#kontrola zda je value spravneho typu
			if Variable.checkValueIsType(v) == True:
				self.value = v['value']
				self.type = v['type']
				self.defined = True
			else:
				Killer(99, 'Pokus o vytvoreni promenne s neodpovijici hodnotou datovemu typu, Variable.set()')			

		else:
			Killer(99, 'Pokus o zadani neznameho typu promenne, Variable.set()')			

	#vraci hodnotu a typ promenne
	def get(self):
		return {'type' : self.getType(), 'value': self.getValue(), 'defined' : self.defined }

	def setFrame(self, frame):
		if frame == 'TF' or frame == 'LF' or frame == 'GF':
			self.frame = frame
		else:
			Killer(99, "Vnitrni chyba interpretu, Variabale.setFrame()")


	def prnt(self):
		print("jmeno promenne: " + self.getLongName())
		print("datovy typ: " + self.getType())
		print("hodnota:", end=" ")
		print(self.getValue())