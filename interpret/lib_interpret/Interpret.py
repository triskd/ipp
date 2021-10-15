#!/usr/bin/env

import sys
from xml.dom import minidom

from lib_interpret.Instruction import Instruction
from lib_interpret.Frame import Frame
from lib_interpret.Variable import Variable
from lib_interpret.Killer import Killer


"""

------------------------------------------------------------
|			 				Interpret						|
-------------------------------------------------------------
	- stale atributy:
		- GF  			: globalni ramec, Frame()
		- scriptArgv	: pole vstupnich argumentu scriptu
		- XML 			: XML objekt, reprezentace kodu
		- prog 			: pole instanci instrukci
		- labels		: dictionary {'label_name' : order_instrukce}
		- frameStack 	: zasobnik lokalnich ramcu
		- dataStack		: zasobnik dictionary {'value' : 'hodnota', 'type' : 'datovy_typ'}
		- callStack 	; zasobnik int, poradi instrukci na ktere se ma vratit
		- nextInstr 	: pocitadlo urcujici, ktera instrukce se ma nyni vykonat, nastaveno na vychozi hodnotu 1

	- nestale atrubuty:
		- sourceArg 	: src vstupniho XML souboru
		- inputArg		: src vstupniho input souboru
		- input 		: pole s nactenymi vstupy ze souboru, jedna polozka je jeden radek
		- LF 			: odkaz na vrchol zasobniku ramcu
		- TF			: docasny ramec
-------------------------------------------------------------

"""
class Interpret:

	def __init__(self):
		self.GF = Frame()
		self.scriptArgv = sys.argv
		self.handleScriptArgs() 
		self.loadXML()
		self.loadINPUTFromFile()
		self.nextInstr = 1
		self.prog = []
		self.prog.append('')		#prvni instrukce ma order i index 1
		self.labels = {}
		self.frameStack = []
		self.dataStack = []
		self.callStack = []
		self.unpackXML()


	# zkontrolu, rozdeli, extrahuje vstupni argumenty scripu
	def handleScriptArgs(self):
		
		helpB = False # pokud byl zadan parametr --help
		inputB = False # pokud byl zadan parametr  --input
		sourceB = False # pokud byl zadan paramet --source

		for arg in self.scriptArgv:
			
			if arg == "--help":
				helpB = True
			
			if "--source=" in arg:
				sourceB = True
				self.sourceArg =  arg.split('=')[1]
			
			if  "--input=" in arg:
				inputB = True
				self.inputArg = arg.split('=')[1]

		if(helpB and (sourceB or inputB)):
			Killer(10, "Chybna kombinace argumentu scriptu, argument --help nelze kombinovat s dalsimi")
		
		if(not sourceB and not inputB and not helpB):
			Killer(10, "Chybna kombinace scriptu, jeden z argumentu --source= nebo --input= musi byt vzdy zadan")
			
	# nacte xml soubor 
	def loadXML(self):
		#pouze pokud je zadan argument --source=
		if hasattr(self, "sourceArg"):
			
			try: #kontrola zda jde soubor otevrit	
				file = open(self.sourceArg)
			except:
				Killer(11, "Chyba pri otevirani vstupni --source souboru: " + self.sourceArg)

			try: #kontrola validniho xml 
				self.XML = minidom.parse(file)
			except:
				Killer(31, "Spatne formatovany XML vstupni soubor, --source")
		else:
			xmlStr = ''
			try:
				for line in sys.stdin:
					xmlStr += line
			except:
				Killer(10, "Nepodarilo se nacist XML vstupni soubor z stdin")

			#ulozeni validniho XML objektu
			try:
				self.XML = minidom.parseString(xmlStr)
			except:
				Killer(31, "Spatne formatovany XML vstupni soubor, z stdin")


	def loadINPUTFromFile(self):
		#pouze pokud je zadan argument --input=
		if hasattr(self, "inputArg"):
			#pokud jde soubor otevrit
			try:
				file = open(self.inputArg)
				self.input = []
			except:
				Killer(11, "Chyba pri otevirani vstupniho --input souboru: " + self.inputArg)

			#ulozeni radku po radku
			for line in file:
				self.input.append(line.rstrip('\n'))

	# rozbali xml objekt na jenotlive instrukce, vytvori objekty instrukci, ulozi 
	# ulozi vsechny labely, pokud narazi na duplicitni label chyba - 52
	def unpackXML(self):

		#kontrola korenoveho elementu
		programDom = self.XML.getElementsByTagName('program')
		if programDom[0].getAttribute('language').lower() != 'ippcode20':
			Killer(31, "Spatny atribut 'language' korenoveho elementu <program>, podporovan pouze jazyk IPPcode20")

		instrukce = self.XML.getElementsByTagName('instruction')

		for i in instrukce:
			#ulozeni instrukce
			instIstr = Instruction(i)
			self.prog.insert(instIstr.ord, instIstr)
			
			#ulozeni labelu
			if instIstr.pattern['opcode'] == 'LABEL':
				#kontrola unikatnosti labelu
				if self.labels.__contains__(instIstr.arguments[0]['value']):
					Killer(52, "Pokus o redefinici navesti. Instrukce - " + instIstr.pattern['opcode'] + " order("+str(instIstr.ord)+")")
				else:
					self.labels[instIstr.arguments[0]['value']] = { 'order' : instIstr.ord}

	#zkontroluje zda ramec zadany parametrem frameName existuje, pokud ano vraci true jinak false
	def existFrame(self, frameName):
		if frameName.upper() == 'GF' or frameName.upper() == 'LF' or frameName.upper() == 'TF':
			if hasattr(self, frameName):
				return True
		return False

	#vrati ramec
	def getFrame(self, frameName):
		if self.existFrame(frameName) == True:
			if frameName == 'GF':
				return self.GF
			if frameName == 'LF':
				return self.LF
			if frameName == 'TF':
				return self.TF
		return None		

	#umisti konstantu (dicctionary) zadanou argumentem value {'value' : hodnota, 'type' : datovy typ} na vrchol datoveho zasobniku
	def pushDataStack(self, value):
		try:
			value['value']
			value['type']
		except:
			Killer(99, "Vnitrni chyba prekladace Interpret.pushDataStack()")

		#kontrola, zda se typ shoduje s hodnotou
		if Variable.checkValueIsType(value) == True:
			self.dataStack.insert(0, value)
		else:
			Killer(99, "Vnitrni chyba prekladace - data nejsou uvedeneho datoveho typu Interpret.pushDataStack()")


	# vraci dictionary {'value' : , 'type' : }, ktery je na vrcholu datoveho zasobniku
	# pokud je datovy zasobnik prazdny -> chyba 56
	def popDataStack(self):
		try:
			val = self.dataStack[0]
			del self.dataStack[0]
			return val
		except:
			Killer(56, "Pokus o vyjmuti hodnoty (pop) nad prazdnym datovym zasobnikem")

	# na zasobnik volanik uklada hodnotu NASLEDUJICI instrukce, ktera se ma po vyjmuti provadet
	def pushCallStack(self, intVal):
		if type(intVal) == int:
			self.callStack.insert(0, intVal)
		else:
			Killer(99, "Vnitrni chyba prekladace, pokus vlozeni ne-int hodnoty na zasobnik volani, Interpret.pushCallStack()")
	
	# vraci int hodnotu na vrcholu zasobniku volani, pokud je zasobnik prazdny -> chyba 56
	def popCallStack(self):
		try:
			val = self.callStack[0]
			del self.callStack[0]
			return val
		except:
			Killer(56, "Pokus o vyjmuti hodnoty (pop) nad prazdnym zasobnikem volani zasobnikem")
	
	#vykonani instrukci
	def run(self):
		self.nextInstr = 1

		#odhaleni skutecnych indexu vsech navesti
		for instr in self.prog:
			#kvuli tomu, ze jsem na 0 index dal prazdnej string :D 
			try:
				if instr.pattern['opcode'] == 'LABEL':
					instr.run(self)
			except:
				True
		

		while self.nextInstr < len(self.prog):
			jump = False

			opcode = self.prog[self.nextInstr].pattern['opcode']

			if opcode == 'JUMP' or opcode == 'JUMPIFEQ' or opcode == 'JUMPIFNEQ' or opcode == 'CALL' or opcode == 'RETURN':
				jump = True

			self.prog[self.nextInstr].run(self)

			if jump == False:
				self.nextInstr += 1


	#vytiskne info
	def prnt(self):
		print("----------------------------------------------------")
		print("GF:")
		self.GF.prnt()
		print("----------------------------------------------------")

		if hasattr(self, "LF"):
			print("----------------------------------------------------")
			print("LF:")
			self.LF.prnt()
			print("----------------------------------------------------")

		if hasattr(self, 'TF'):
			print("----------------------------------------------------")
			print("TF:")
			self.TF.prnt()
			print("----------------------------------------------------")


		print("----------------------------------------------------")
		print("frameStack:")
		print("  TOP->")
		for frame in self.frameStack:
			frame.prnt()
			print("=====================================================")

		print("----------------------------------------------------")

		print("----------------------------------------------------")
		print("dataStack:")
		print("  TOP->")
		for el in self.dataStack:
			print(el)
		print("----------------------------------------------------")

		print("----------------------------------------------------")
		print("callStack:")
		print("  TOP->")
		for el in self.callStack:
			print(el)
		print("----------------------------------------------------")

