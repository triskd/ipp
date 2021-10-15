#!/usr/bin/env

from lib_interpret.Killer import Killer
from lib_interpret.Variable import Variable
from lib_interpret.Frame import Frame
from copy import copy, deepcopy

 

"""
---------------------------------------------
|				Instruction					|
---------------------------------------------
- stale atributy:
	- pattern 	: 	instrukcni predpis, typy a pocet arg...
	- ord 		:	poradi instrukce
	- arguments []	:	pole argumentu

- nestale atributy:
	
----------------------------------------------	
"""

class Instruction:

	order = []

	@staticmethod
	def getMethodType(i):	
		InstrSet = {
			
			'MOVE':
				{ 'opcode'	: 'MOVE', 
				  'args'	: [
				  				{'arg1' : {'aType' : 'var', 'dType': [] }  }, 
				  				{'arg2' : {'aType' : 'symb', 'dType': ['int', 'string', 'bool', 'nil'] }  } 
				  			  ]		
				},

			'CREATEFRAME':
				{ 'opcode' : 'CREATEFRAME',
				  'args'   : []			
				},

			'PUSHFRAME':
				{ 'opcode' : 'PUSHFRAME',
				  'args'   : []			
				},

			'POPFRAME':
				{ 'opcode' : 'POPFRAME',
				  'args'   : []			
				},

			'DEFVAR':
				{ 'opcode'	: 'DEFVAR', 
				  'args'	: [
				  				{'arg1' : {'aType' : 'var', 'dType': [] }  } 
				  			  ]		
				},
				
			'CALL':
				{ 'opcode'	: 'CALL', 
				  'args'	: [
				  				{'arg1'	: {'aType' : 'label', 'dType': [] } }
				  			  ]	
				},

			'RETURN':
				{ 'opcode' : 'RETURN',
				  'args'   : []			
				},

			'PUSHS':
				{ 'opcode'	: 'PUSHS',
				  'args'	: [
				  				{'arg1' : {'aType' : 'symb', 'dType' : [] } }
				  			  ]	
				},


			'POPS':
				{ 'opcode'	: 'POPS', 
				  'args'	: [
				  				{'arg1' : {'aType' : 'var', 'dType' : [] } }
				  			  ]
				},

			'ADD':
				{ 'opcode'	: 'ADD', 
				  'args'	: [
				  				{'arg1' : {'aType' : 'var', 'dType': [] }  }, 
				  				{'arg2' : {'aType' : 'symb', 'dType': ['int'] }  }, 
				  				{'arg3' : {'aType' : 'symb', 'dType': ['int'] }  } 
				  			  ]		
				},

			'SUB':
				{ 'opcode'	: 'SUB', 
				  'args'	: [
				  				{'arg1' : {'aType' : 'var', 'dType': [] }  }, 
				  				{'arg2' : {'aType' : 'symb', 'dType': ['int'] }  }, 
				  				{'arg3' : {'aType' : 'symb', 'dType': ['int'] }  } 
				  			  ]		
				},

			'MUL':
				{ 'opcode'	: 'MUL', 
				  'args'	: [
				  				{'arg1' : {'aType' : 'var', 'dType': [] }  }, 
				  				{'arg2' : {'aType' : 'symb', 'dType': ['int'] }  }, 
				  				{'arg3' : {'aType' : 'symb', 'dType': ['int'] }  } 
				  			  ]		
				},

			'IDIV':
				{ 'opcode'	: 'IDIV', 
				  'args'	: [
				  				{'arg1' : {'aType' : 'var', 'dType': [] }  }, 
				  				{'arg2' : {'aType' : 'symb', 'dType': ['int'] }  }, 
				  				{'arg3' : {'aType' : 'symb', 'dType': ['int'] }  } 
				  			  ]		
				},

			'LT':
				{ 'opcode'	: 'LT', 
				  'args'	: [
				  				{'arg1' : {'aType' : 'var', 'dType': [] }  }, 
				  				{'arg2' : {'aType' : 'symb', 'dType': ['int', 'bool', 'string'] }  }, 
				  				{'arg3' : {'aType' : 'symb', 'dType': ['int', 'bool', 'string'] }  } 
				  			  ]		
				},

			'GT':
				{ 'opcode'	: 'GT', 
				  'args'	: [
				  				{'arg1' : {'aType' : 'var', 'dType': [] }  }, 
				  				{'arg2' : {'aType' : 'symb', 'dType': ['int', 'bool', 'string'] }  }, 
				  				{'arg3' : {'aType' : 'symb', 'dType': ['int', 'bool', 'string'] }  } 
				  			  ]		
				},

			'EQ':
				{ 'opcode'	: 'EQ', 
				  'args'	: [
				  				{'arg1' : {'aType' : 'var', 'dType': [] }  }, 
				  				{'arg2' : {'aType' : 'symb', 'dType': ['int', 'bool', 'string'] }  }, 
				  				{'arg3' : {'aType' : 'symb', 'dType': ['int', 'bool', 'string'] }  } 
				  			  ]		
				},

			'AND':
				{ 'opcode'	: 'AND', 
				  'args'	: [
				  				{'arg1' : {'aType' : 'var', 'dType': [] }  }, 
				  				{'arg2' : {'aType' : 'symb', 'dType': ['bool'] }  }, 
				  				{'arg3' : {'aType' : 'symb', 'dType': ['bool'] }  } 
				  			  ]		
				},

			'OR':
				{ 'opcode'	: 'OR', 
				  'args'	: [
				  				{'arg1' : {'aType' : 'var', 'dType': [] }  }, 
				  				{'arg2' : {'aType' : 'symb', 'dType': ['bool'] }  }, 
				  				{'arg3' : {'aType' : 'symb', 'dType': ['bool'] }  } 
				  			  ]		
				},

			'NOT':
				{ 'opcode'	: 'NOT', 
				  'args'	: [
				  				{'arg1' : {'aType' : 'var', 'dType': [] }  }, 
				  				{'arg2' : {'aType' : 'symb', 'dType': ['bool'] }  }
				  			  ]		
				},
			
			'INT2CHAR':
				{ 'opcode'	: 'INT2CHAR', 
				  'args'	: [
				  				{'arg1' : {'aType' : 'var', 'dType': [] }  }, 
				  				{'arg2' : {'aType' : 'symb', 'dType': ['int'] }  } 
				  			  ]		
				},
			
			'STRI2INT':
				{ 'opcode'	: 'STRI2INT', 
				  'args'	: [
				  				{'arg1' : {'aType' : 'var', 'dType': [] }  }, 
				  				{'arg2' : {'aType' : 'symb', 'dType': ['string'] }  }, 
				  				{'arg3' : {'aType' : 'symb', 'dType': ['int'] }  } 
				  			  ]		
				},

			'READ':
				{ 'opcode'	: 'READ', 
				  'args'	: [
				  				{'arg1' : {'aType' : 'var', 'dType': [] }  }, 
				  				{'arg2' : {'aType' : 'type', 'dType': ['int', 'string', 'bool'] }  } 
				  			  ]		
				},

			'WRITE':
				{ 'opcode'	: 'WRITE', 
				  'args'	: [
				  				{'arg1' : {'aType' : 'symb', 'dType': ['int', 'string', 'bool', 'nil'] }  } 
				  			  ]		
				},

			'CONCAT':
				{ 'opcode'	: 'CONCAT', 
				  'args'	: [
				  				{'arg1' : {'aType' : 'var', 'dType': [] }  }, 
				  				{'arg2' : {'aType' : 'symb', 'dType': ['string'] }  }, 
				  				{'arg3' : {'aType' : 'symb', 'dType': ['string'] }  } 
				  			  ]		
				},

			'STRLEN':
				{ 'opcode'	: 'STRLEN', 
				  'args'	: [
				  				{'arg1' : {'aType' : 'var', 'dType': [] }  }, 
				  				{'arg2' : {'aType' : 'symb', 'dType': ['string'] }  } 
				  			  ]		
				},

			'GETCHAR':
				{ 'opcode'	: 'GETCHAR', 
				  'args'	: [
				  				{'arg1' : {'aType' : 'var', 'dType': [] }  }, 
				  				{'arg2' : {'aType' : 'symb', 'dType': ['string'] }  }, 
				  				{'arg3' : {'aType' : 'symb', 'dType': ['int'] }  } 
				  			  ]		
				},

			'SETCHAR':
				{ 'opcode'	: 'SETCHAR', 
				  'args'	: [
				  				{'arg1' : {'aType' : 'var', 'dType': ['string'] }  }, 
				  				{'arg2' : {'aType' : 'symb', 'dType': ['int'] }  }, 
				  				{'arg3' : {'aType' : 'symb', 'dType': ['string'] }  } 
				  			  ]		
				},

			'TYPE':
				{ 'opcode'	: 'TYPE', 
				  'args'	: [
				  				{'arg1' : {'aType' : 'var', 'dType': [] }  }, 
				  				{'arg2' : {'aType' : 'symb', 'dType': ['string', 'int', 'bool', 'nil'] }  } 
				  			  ]		
				},

			'LABEL':
				{ 'opcode'	: 'LABEL', 
				  'args'	: [
				  				{'arg1' : {'aType' : 'label', 'dType': ['label'] }  } 
				  			  ]		
				},			

			'JUMP':
				{ 'opcode'	: 'JUMP', 
				  'args'	: [
				  				{'arg1' : {'aType' : 'label', 'dType': ['label'] }  } 
				  			  ]		
				},

			'JUMPIFEQ':
				{ 'opcode'	: 'JUMPIFEQ', 
				  'args'	: [
				  				{'arg1' : {'aType' : 'label', 'dType': ['label'] }  }, 
				  				{'arg2' : {'aType' : 'symb', 'dType': ['int', 'string', 'bool', 'nil'] }  }, 
				  				{'arg3' : {'aType' : 'symb', 'dType': ['int', 'string', 'bool', 'nil'] }  } 
				  			  ]		
				},
			
			'JUMPIFNEQ':
				{ 'opcode'	: 'JUMPIFNEQ', 
				  'args'	: [
				  				{'arg1' : {'aType' : 'label', 'dType': ['label'] }  }, 
				  				{'arg2' : {'aType' : 'symb', 'dType': ['int', 'string', 'bool', 'nil'] }  }, 
				  				{'arg3' : {'aType' : 'symb', 'dType': ['int', 'string', 'bool', 'nil'] }  } 
				  			  ]		
				},

			'EXIT':
				{ 'opcode'	: 'EXIT', 
				  'args'	: [
				  				{'arg1' : {'aType' : 'symb', 'dType': ['int'] }  } 
				  			  ]		
				},

			
			'DPRINT':
				{ 'opcode'	: 'DPRINT', 
				  'args'	: [
				  				{'arg1' : {'aType' : 'symb', 'dType': ['int', 'string', 'bool', 'nil'] }  } 
				  			  ]		
				},

			'BREAK':
				{ 'opcode'	: 'BREAK', 
				  'args'	: []		
				}

		}

		try:
			return InstrSet[i.upper()]
		except:
			return None

	################################################################################################################################
	

	@staticmethod
	def MOVE(interp, instr):
		
		if instr.checkFrameAndVariableExist(interp) == True:		# kontrola ramcu a promennych	=> ramce i promenne existuji
			
			if instr.arguments[1]['type'] == 'var':						# pokud je druhy argument taky instrukce
				frame2Name = Variable.splitFrame(instr.arguments[1]['value'])	# vytazeni jmena ramce
				frame2 = interp.getFrame(frame2Name)			
				arg2Value = frame2.getVar(instr.arguments[1]['value']).get() # ziskani hodnoty promenne v 2.parametru
				
				#kontrola zda promenne jiz byla prirazena hodnota
				if arg2Value['defined'] == False:
					Killer(56, "Chybejici hodnota v promenne. Instrukce - " + instr.pattern['opcode'] + " order(" + str(instr.ord) + ")")

			else:														# 2.argument je konstanta
				arg2Value = instr.arguments[1] 							# ziskani konstanty v 2.parametru

			#prirazeni hodnoty to promenne v 1. parametru
			frame1Name = Variable.splitFrame(instr.arguments[0]['value'])
			frame1 = interp.getFrame(frame1Name)
			frame1.getVar(instr.arguments[0]['value']).set(arg2Value)	#nastaveni hodnoty do promenne v 1. argumentu
						

	@staticmethod
	def CREATEFRAME(interp):
		if hasattr(interp, 'TF') == True:
			del interp.TF
		interp.TF = Frame()

	@staticmethod
	def PUSHFRAME(interp):
		if hasattr(interp, 'TF') == True:
			interp.frameStack.insert(0, deepcopy(interp.TF))
			interp.LF = interp.frameStack[0]
			del interp.TF
		else:
			Killer(55, "Pokus o presunuti nedefinovane ramce TF na zasobnik ramcu")

	@staticmethod 
	def POPFRAME(interp):
		if hasattr(interp, 'LF'):
			if hasattr(interp, 'TF'): #pokud je definovan TF, dojde k jeho smazani
				del interp.TF
			interp.TF = deepcopy(interp.LF) #zkopirovani LF do TF
			del interp.LF	#odstraneni odkazu na vrchol zasobniku ramcu            
			del interp.frameStack[0] #ostraneni ramce z vrcholu zasobniku
			if len(interp.frameStack) >= 1: #pokud je na zasobniku dalsi ramec, stava se LF
				interp.LF = interp.frameStack[0]
		else:
			Killer(55, "Pokus o vyjmuti ramce z prazdneho zasobniku ramcu")

	@staticmethod
	def DEFVAR(interp, instr):
		frameName = Variable.splitFrame(instr.arguments[0]['value'])
		if interp.existFrame(frameName) == True:
			interp.getFrame(frameName).addVar(instr.arguments[0]['value'])
		else:
			Killer(55, "Pokus o definici promenne v Neexistujicim ramci - " + frameName + " instrukce - " + instr.pattern['opcode'] + " order(" + str(instr.ord) + ")")

	@staticmethod
	def CALL(interp, instr):
		try:
			labelOrder = interp.labels[instr.arguments[0]['value']]
			saved = interp.nextInstr +1
			interp.pushCallStack(saved)
			interp.nextInstr = labelOrder
		except:
			Killer(52, "Pokus o skok na nedefinovane navesti - '" + instr.arguments[0]['value'] + "', instrukce - " + instr.pattern['opcode'] + " order(" + str(instr.ord) + ")")
	
	@staticmethod
	def RETURN(interp):
		if len(interp.callStack) > 0:	#kontrola, zda zasobnik volani neni prazdny
			interp.nextInstr = interp.popCallStack()
		else:
			Killer(56, "Volani instrukce RETURN nad prazdnym zasobnikem volani")


	@staticmethod
	def PUSHS(interp, instr):
		#pokud je zadan argument instrukce
		if len(instr.arguments) == 1:
			if instr.checkFrameAndVariableExist(interp) == True:
				
				try:
					#exktrakce hodnoty z promenne
					varName = instr.getVariableArgs()
					var = interp.getFrame(varName[0]['frame']).getVar(varName[0]['name'])
					varValue = var.get()

				except:
					#extrakce hodnoty z konstanty
					varValue = instr.arguments[0]

				if 'defined' in varValue:
					#kontrola zda promenne jiz byla prirazena hodnota
					if varValue['defined'] == False:
						Killer(56, "Chybejici hodnota v promenne. Instrukce - " + instr.pattern['opcode'] + " order(" + str(instr.ord) + ")")

		#pokud budeme brat hodnotu z datoveho zasobniku
		elif len(instr.arguments) == 0:
			#kontrola zda na dotovym zasobniku je nejaka polozka
			try:
				varValue = deepcopy(interp.dataStack[0])
			except:
				Killer(56, "Pokus o pristum k hodnote datoveho zasobniku nad prazdnym zasobnikem. Instrukce - " +instr.pattern['opcode'] + " order("+str(instr.ord)+")" )
		
		#vlozeni hodnoty na datovy zasobnik
		interp.pushDataStack(varValue)

	@staticmethod
	def POPS(interp, instr):
		#kontrola zda datovy zasobnik neni prazdny
		if len(interp.dataStack) > 0:
			if instr.checkFrameAndVariableExist(interp) == True:
				#ziskani promenne kam se ma vlozit hodnota z datoveho zasobniku
				try:
					varName = instr.getVariableArgs()[0]
					var = interp.getFrame(varName['frame']).getVar(varName['name'])
					#ziskani hodnoty na vrcholu datoveho zasobniku
					value = interp.popDataStack()
					var.set(value)

				except:
					# pokud nebyla zadana promena dojde v vyjmuti hodnoty ze zasobniku a jeji zpetne vlozeni, tzn nic se nedeje
					True

		else:
			Killer(56, "Pokus o pristum k hodnote datoveho zasobniku nad prazdnym zasobnikem. Instrukce - " +instr.pattern['opcode'] + " order("+str(instr.ord)+")" )

	@staticmethod
	def ADD(interp, instr):
		if instr.checkFrameAndVariableExist(interp) == True:
			argVarNames = instr.getVariableArgs()
			#promenna do ktere ulozime vysledek operace
			vysledek = interp.getFrame(argVarNames[0]['frame']).getVar(argVarNames[0]['name'])
			
			#extrakce hodnoty z 2 argumentu
			if instr.arguments[1]['type'] == 'var':
				op1Name = Variable.splitFrameAndName(instr.arguments[1]['value'])
				op1Value = interp.getFrame(op1Name['frame']).getVar(op1Name['name']).get()
			else:
				op1Value = instr.arguments[1]

			# #extrakce hodnoty z 3 argumentu
			if instr.arguments[2]['type'] == 'var':
				op2Name = Variable.splitFrameAndName(instr.arguments[2]['value'])
				op2Value = interp.getFrame(op2Name['frame']).getVar(op2Name['name']).get()
			else:
				op2Value = instr.arguments[2]

			#kontrola zda obe promenne maji prirazenou hodnotu
			if 'defined' in op1Value :
				if op1Value['defined'] == False:
					Killer(56, "Chybejici hodnota v promenne. Instrukce - " + instr.pattern['opcode'] + " order(" + str(instr.ord) + ")")
			if 'defined' in op2Value:		
				if op2Value['defined'] == False:
					Killer(56, "Chybejici hodnota v promenne. Instrukce - " + instr.pattern['opcode'] + " order(" + str(instr.ord) + ")")



			#kontrola zda jsou oba operandy typu int
			if op1Value['type'] == 'int' and op2Value['type'] == 'int':
				#kontrola zda jsou zadane hodnoty opravu cela cisla
				if Variable.checkValueIsType(op1Value) and Variable.checkValueIsType(op2Value):
					#vypocet
					vyslednaHodnota = {'type' : 'int', 'value' : int(op1Value['value'])  + int(op2Value['value'])}
					vysledek.set(vyslednaHodnota)
				else:
					Killer(53, "Spatne typy operandu. Instrukce - " +instr.pattern['opcode'] + " order("+str(instr.ord)+")" )
			else:
				Killer(53, "Spatne typy operandu. Instrukce - " +instr.pattern['opcode'] + " order("+str(instr.ord)+")" )

	@staticmethod
	def SUB(interp, instr):
		if instr.checkFrameAndVariableExist(interp) == True:
			argVarNames = instr.getVariableArgs()

			#promenna do ktere ulozime vysledek operace
			vysledek = interp.getFrame(argVarNames[0]['frame']).getVar(argVarNames[0]['name'])
			
			#extrakce hodnoty z 2 argumentu
			if instr.arguments[1]['type'] == 'var':
				op1Name = Variable.splitFrameAndName(instr.arguments[1]['value'])
				op1Value = interp.getFrame(op1Name['frame']).getVar(op1Name['name']).get()
			else:
				op1Value = instr.arguments[1]

			# #extrakce hodnoty z 3 argumentu
			if instr.arguments[2]['type'] == 'var':
				op2Name = Variable.splitFrameAndName(instr.arguments[2]['value'])
				op2Value = interp.getFrame(op2Name['frame']).getVar(op2Name['name']).get()
			else:
				op2Value = instr.arguments[2]

			#kontrola zda obe promenne maji prirazenou hodnotu
			if 'defined' in op1Value :
				if op1Value['defined'] == False:
					Killer(56, "Chybejici hodnota v promenne. Instrukce - " + instr.pattern['opcode'] + " order(" + str(instr.ord) + ")")
			if 'defined' in op2Value:		
				if op2Value['defined'] == False:
					Killer(56, "Chybejici hodnota v promenne. Instrukce - " + instr.pattern['opcode'] + " order(" + str(instr.ord) + ")")
					

			#kontrola zda jsou oba operandy typu int
			if op1Value['type'] == 'int' and op2Value['type'] == 'int':
				#kontrola zda jsou zadane hodnoty opravu cela cisla
				if Variable.checkValueIsType(op1Value) and Variable.checkValueIsType(op2Value):
					#vypocet
					vyslednaHodnota = {'type' : 'int', 'value' : int(op1Value['value'])  - int(op2Value['value'])}
					vysledek.set(vyslednaHodnota)
				else:
					Killer(53, "Spatne typy operandu. Instrukce - " +instr.pattern['opcode'] + " order("+str(instr.ord)+")" )
			else:
				Killer(53, "Spatne typy operandu. Instrukce - " +instr.pattern['opcode'] + " order("+str(instr.ord)+")" )

	@staticmethod
	def MUL(interp, instr):
		if instr.checkFrameAndVariableExist(interp) == True:
			argVarNames = instr.getVariableArgs()

			#promenna do ktere ulozime vysledek operace
			vysledek = interp.getFrame(argVarNames[0]['frame']).getVar(argVarNames[0]['name'])
			
			#extrakce hodnoty z 2 argumentu
			if instr.arguments[1]['type'] == 'var':
				op1Name = Variable.splitFrameAndName(instr.arguments[1]['value'])
				op1Value = interp.getFrame(op1Name['frame']).getVar(op1Name['name']).get()
			else:
				op1Value = instr.arguments[1]

			# #extrakce hodnoty z 3 argumentu
			if instr.arguments[2]['type'] == 'var':
				op2Name = Variable.splitFrameAndName(instr.arguments[2]['value'])
				op2Value = interp.getFrame(op2Name['frame']).getVar(op2Name['name']).get()
			else:
				op2Value = instr.arguments[2]

			#kontrola zda obe promenne maji prirazenou hodnotu
			if 'defined' in op1Value :
				if op1Value['defined'] == False:
					Killer(56, "Chybejici hodnota v promenne. Instrukce - " + instr.pattern['opcode'] + " order(" + str(instr.ord) + ")")
			if 'defined' in op2Value:		
				if op2Value['defined'] == False:
					Killer(56, "Chybejici hodnota v promenne. Instrukce - " + instr.pattern['opcode'] + " order(" + str(instr.ord) + ")")
					

			#kontrola zda jsou oba operandy typu int
			if op1Value['type'] == 'int' and op2Value['type'] == 'int':
				#kontrola zda jsou zadane hodnoty opravu cela cisla
				if Variable.checkValueIsType(op1Value) and Variable.checkValueIsType(op2Value):
					#vypocet
					vyslednaHodnota = {'type' : 'int', 'value' : int(op1Value['value'])  * int(op2Value['value'])}
					vysledek.set(vyslednaHodnota)
				else:
					Killer(53, "Spatne typy operandu. Instrukce - " +instr.pattern['opcode'] + " order("+str(instr.ord)+")" )
			else:
				Killer(53, "Spatne typy operandu. Instrukce - " +instr.pattern['opcode'] + " order("+str(instr.ord)+")" )



	@staticmethod
	def IDIV(interp, instr):
		if instr.checkFrameAndVariableExist(interp) == True:
			argVarNames = instr.getVariableArgs()

			#promenna do ktere ulozime vysledek operace
			vysledek = interp.getFrame(argVarNames[0]['frame']).getVar(argVarNames[0]['name'])
			
			#extrakce hodnoty z 2 argumentu
			if instr.arguments[1]['type'] == 'var':
				op1Name = Variable.splitFrameAndName(instr.arguments[1]['value'])
				op1Value = interp.getFrame(op1Name['frame']).getVar(op1Name['name']).get()
			else:
				op1Value = instr.arguments[1]

			# #extrakce hodnoty z 3 argumentu
			if instr.arguments[2]['type'] == 'var':
				op2Name = Variable.splitFrameAndName(instr.arguments[2]['value'])
				op2Value = interp.getFrame(op2Name['frame']).getVar(op2Name['name']).get()
			else:
				op2Value = instr.arguments[2]

			#kontrola zda obe promenne maji prirazenou hodnotu
			if 'defined' in op1Value :
				if op1Value['defined'] == False:
					Killer(56, "Chybejici hodnota v promenne. Instrukce - " + instr.pattern['opcode'] + " order(" + str(instr.ord) + ")")
			if 'defined' in op2Value:		
				if op2Value['defined'] == False:
					Killer(56, "Chybejici hodnota v promenne. Instrukce - " + instr.pattern['opcode'] + " order(" + str(instr.ord) + ")")
					
			#kontrola zda jsou oba operandy typu int
			if op1Value['type'] == 'int' and op2Value['type'] == 'int':
				#kontrola zda jsou zadane hodnoty opravu cela cisla
				if Variable.checkValueIsType(op1Value) and Variable.checkValueIsType(op2Value):
					#vypocet
					if int(op2Value['value']) != 0: #deleni 0!
						vyslednaHodnota = {'type' : 'int', 'value' : int(op1Value['value'])  // int(op2Value['value'])}
						vysledek.set(vyslednaHodnota)
					else:
						Killer(57, "Deleni 0. Instrukce - " +instr.pattern['opcode'] + " order("+str(instr.ord)+")")
				else:
					Killer(53, "Spatne typy operandu. Instrukce - " +instr.pattern['opcode'] + " order("+str(instr.ord)+")" )
			else:
				Killer(53, "Spatne typy operandu. Instrukce - " +instr.pattern['opcode'] + " order("+str(instr.ord)+")" )

	@staticmethod
	def EQ(interp, instr):
		if instr.checkFrameAndVariableExist(interp) == True:
			argVarNames = instr.getVariableArgs()

			#promenna do ktere ulozime vysledek operace
			vysledek = interp.getFrame(argVarNames[0]['frame']).getVar(argVarNames[0]['name'])
			
			#extrakce hodnoty z 2 argumentu
			if instr.arguments[1]['type'] == 'var':
				op1Name = Variable.splitFrameAndName(instr.arguments[1]['value'])
				op1Value = interp.getFrame(op1Name['frame']).getVar(op1Name['name']).get()
			else:
				op1Value = instr.arguments[1]

			# #extrakce hodnoty z 3 argumentu
			if instr.arguments[2]['type'] == 'var':
				op2Name = Variable.splitFrameAndName(instr.arguments[2]['value'])
				op2Value = interp.getFrame(op2Name['frame']).getVar(op2Name['name']).get()
			else:
				op2Value = instr.arguments[2]

			#kontrola zda obe promenne maji prirazenou hodnotu
			if 'defined' in op1Value :
				if op1Value['defined'] == False:
					Killer(56, "Chybejici hodnota v promenne. Instrukce - " + instr.pattern['opcode'] + " order(" + str(instr.ord) + ")")
			if 'defined' in op2Value:		
				if op2Value['defined'] == False:
					Killer(56, "Chybejici hodnota v promenne. Instrukce - " + instr.pattern['opcode'] + " order(" + str(instr.ord) + ")")
					

			#kontrola zda jsou oba operandy typu int
			if op1Value['type'] == 'int' and op2Value['type'] == 'int':
				#kontrola zda jsou zadane hodnoty opravu cela cisla
				if Variable.checkValueIsType(op1Value) and Variable.checkValueIsType(op2Value):
					#vypocet
					if int(op1Value['value']) == int(op2Value['value']):
						vyslednaHodnota = {'type' : 'bool', 'value' : 'true'}
					else:
						vyslednaHodnota = {'type' : 'bool', 'value' : 'false'}

					vysledek.set(vyslednaHodnota)
				else:
					Killer(53, "Spatne typy oper2andu. Instrukce - " +instr.pattern['opcode'] + " order("+str(instr.ord)+")" )

			#kontrola zda jsou oba operandy typu bool
			elif op1Value['type'] == 'bool' and op2Value['type'] == 'bool':
				#kontrola zda jsou zadane hodnoty opravdu typu bool
				if Variable.checkValueIsType(op1Value) and Variable.checkValueIsType(op2Value):
					#vypocet
					if op1Value['value'] == op2Value['value']:
						vyslednaHodnota = {'type' : 'bool', 'value' : 'true'}
					else:
						vyslednaHodnota = {'type' : 'bool', 'value' : 'false'}

					vysledek.set(vyslednaHodnota)
				else:
					Killer(53, "Spatne typy operandu. Instrukce - " +instr.pattern['opcode'] + " order("+str(instr.ord)+")" )
			
			#kontrola zda jsou oba operandy typu string
			elif op1Value['type'] == 'string' and op2Value['type'] == 'string':
				#kontrola zda jsou zadane hodnoty opravdu typu bool
				if Variable.checkValueIsType(op1Value) and Variable.checkValueIsType(op2Value):
					#vypocet
					if op1Value['value'] == op2Value['value']:
						vyslednaHodnota = {'type' : 'bool', 'value' : 'true'}
					else:
						vyslednaHodnota = {'type' : 'bool', 'value' : 'false'}

					vysledek.set(vyslednaHodnota)
				else:
					Killer(53, "Spatne typy operandu. Instrukce - " +instr.pattern['opcode'] + " order("+str(instr.ord)+")" )

			#kontrola zda jsou oba (hlavne prvni) operandy typu nil
			elif op1Value['type'] == 'nil':
				#kontrola zda jsou zadane hodnoty opravdu typu nil
				if Variable.checkValueIsType(op1Value) and Variable.checkValueIsType(op2Value):
					#vypocet
					if op1Value['value'] == op2Value['value'] and op1Value['type'] == op2Value['type']:
						vyslednaHodnota = {'type' : 'bool', 'value' : 'true'}
					else:
						vyslednaHodnota = {'type' : 'bool', 'value' : 'false'}

					vysledek.set(vyslednaHodnota)
				else:
					Killer(53, "Spatne typy operandu. Instrukce - " +instr.pattern['opcode'] + " order("+str(instr.ord)+")" )
			else:
				Killer(53, "Spatne typy operandu. Instrukce - " +instr.pattern['opcode'] + " order("+str(instr.ord)+")" )

	@staticmethod
	def LT(interp, instr):
		if instr.checkFrameAndVariableExist(interp) == True:
			argVarNames = instr.getVariableArgs()

			#promenna do ktere ulozime vysledek operace
			vysledek = interp.getFrame(argVarNames[0]['frame']).getVar(argVarNames[0]['name'])
			
			#extrakce hodnoty z 2 argumentu
			if instr.arguments[1]['type'] == 'var':
				op1Name = Variable.splitFrameAndName(instr.arguments[1]['value'])
				op1Value = interp.getFrame(op1Name['frame']).getVar(op1Name['name']).get()
			else:
				op1Value = instr.arguments[1]

			# #extrakce hodnoty z 3 argumentu
			if instr.arguments[2]['type'] == 'var':
				op2Name = Variable.splitFrameAndName(instr.arguments[2]['value'])
				op2Value = interp.getFrame(op2Name['frame']).getVar(op2Name['name']).get()
			else:
				op2Value = instr.arguments[2]

			#kontrola zda obe promenne maji prirazenou hodnotu
			if 'defined' in op1Value :
				if op1Value['defined'] == False:
					Killer(56, "Chybejici hodnota v promenne. Instrukce - " + instr.pattern['opcode'] + " order(" + str(instr.ord) + ")")
			if 'defined' in op2Value:		
				if op2Value['defined'] == False:
					Killer(56, "Chybejici hodnota v promenne. Instrukce - " + instr.pattern['opcode'] + " order(" + str(instr.ord) + ")")
					

			#kontrola zda jsou oba operandy typu int
			if op1Value['type'] == 'int' and op2Value['type'] == 'int':
				#kontrola zda jsou zadane hodnoty opravu cela cisla
				if Variable.checkValueIsType(op1Value) and Variable.checkValueIsType(op2Value):
					#vypocet
					if int(op1Value['value']) < int(op2Value['value']):
						vyslednaHodnota = {'type' : 'bool', 'value' : 'true'}
					else:
						vyslednaHodnota = {'type' : 'bool', 'value' : 'false'}

					vysledek.set(vyslednaHodnota)
				else:
					Killer(53, "Spatne typy oper2andu. Instrukce - " +instr.pattern['opcode'] + " order("+str(instr.ord)+")" )

			#kontrola zda jsou oba operandy typu bool
			elif op1Value['type'] == 'bool' and op2Value['type'] == 'bool':
				#kontrola zda jsou zadane hodnoty opravdu typu bool
				if Variable.checkValueIsType(op1Value) and Variable.checkValueIsType(op2Value):
					#vypocet
					if op1Value['value'] == 'false' and op2Value['value'] == 'true':
						vyslednaHodnota = {'type' : 'bool', 'value' : 'true'}
					else:
						vyslednaHodnota = {'type' : 'bool', 'value' : 'false'}

					vysledek.set(vyslednaHodnota)
				else:
					Killer(53, "Spatne typy operandu. Instrukce - " +instr.pattern['opcode'] + " order("+str(instr.ord)+")" )
			
			#kontrola zda jsou oba operandy typu string
			elif op1Value['type'] == 'string' and op2Value['type'] == 'string':
				#kontrola zda jsou zadane hodnoty opravdu typu bool
				if Variable.checkValueIsType(op1Value) and Variable.checkValueIsType(op2Value):
					#vypocet
					if op1Value['value'] < op2Value['value']:
						vyslednaHodnota = {'type' : 'bool', 'value' : 'true'}
					else:
						vyslednaHodnota = {'type' : 'bool', 'value' : 'false'}

					vysledek.set(vyslednaHodnota)
				else:
					Killer(53, "Spatne typy operandu. Instrukce - " +instr.pattern['opcode'] + " order("+str(instr.ord)+")" )
			else:
				Killer(53, "Spatne typy operandu. Instrukce - " +instr.pattern['opcode'] + " order("+str(instr.ord)+")" )

	@staticmethod
	def GT(interp, instr):
		if instr.checkFrameAndVariableExist(interp) == True:
			argVarNames = instr.getVariableArgs()

			#promenna do ktere ulozime vysledek operace
			vysledek = interp.getFrame(argVarNames[0]['frame']).getVar(argVarNames[0]['name'])
			
			#extrakce hodnoty z 2 argumentu
			if instr.arguments[1]['type'] == 'var':
				op1Name = Variable.splitFrameAndName(instr.arguments[1]['value'])
				op1Value = interp.getFrame(op1Name['frame']).getVar(op1Name['name']).get()
			else:
				op1Value = instr.arguments[1]

			# #extrakce hodnoty z 3 argumentu
			if instr.arguments[2]['type'] == 'var':
				op2Name = Variable.splitFrameAndName(instr.arguments[2]['value'])
				op2Value = interp.getFrame(op2Name['frame']).getVar(op2Name['name']).get()
			else:
				op2Value = instr.arguments[2]

			#kontrola zda obe promenne maji prirazenou hodnotu
			if 'defined' in op1Value :
				if op1Value['defined'] == False:
					Killer(56, "Chybejici hodnota v promenne. Instrukce - " + instr.pattern['opcode'] + " order(" + str(instr.ord) + ")")
			if 'defined' in op2Value:		
				if op2Value['defined'] == False:
					Killer(56, "Chybejici hodnota v promenne. Instrukce - " + instr.pattern['opcode'] + " order(" + str(instr.ord) + ")")
					

			#kontrola zda jsou oba operandy typu int
			if op1Value['type'] == 'int' and op2Value['type'] == 'int':
				#kontrola zda jsou zadane hodnoty opravu cela cisla
				if Variable.checkValueIsType(op1Value) and Variable.checkValueIsType(op2Value):
					#vypocet
					if int(op1Value['value']) > int(op2Value['value']):
						vyslednaHodnota = {'type' : 'bool', 'value' : 'true'}
					else:
						vyslednaHodnota = {'type' : 'bool', 'value' : 'false'}

					vysledek.set(vyslednaHodnota)
				else:
					Killer(53, "Spatne typy oper2andu. Instrukce - " +instr.pattern['opcode'] + " order("+str(instr.ord)+")" )

			#kontrola zda jsou oba operandy typu bool
			elif op1Value['type'] == 'bool' and op2Value['type'] == 'bool':
				#kontrola zda jsou zadane hodnoty opravdu typu bool
				if Variable.checkValueIsType(op1Value) and Variable.checkValueIsType(op2Value):
					#vypocet
					if op1Value['value'] == 'true' and op2Value['value'] == 'false':
						vyslednaHodnota = {'type' : 'bool', 'value' : 'true'}
					else:
						vyslednaHodnota = {'type' : 'bool', 'value' : 'false'}

					vysledek.set(vyslednaHodnota)
				else:
					Killer(53, "Spatne typy operandu. Instrukce - " +instr.pattern['opcode'] + " order("+str(instr.ord)+")" )
			
			#kontrola zda jsou oba operandy typu string
			elif op1Value['type'] == 'string' and op2Value['type'] == 'string':
				#kontrola zda jsou zadane hodnoty opravdu typu bool
				if Variable.checkValueIsType(op1Value) and Variable.checkValueIsType(op2Value):
					#vypocet
					if op1Value['value'] > op2Value['value']:
						vyslednaHodnota = {'type' : 'bool', 'value' : 'true'}
					else:
						vyslednaHodnota = {'type' : 'bool', 'value' : 'false'}

					vysledek.set(vyslednaHodnota)
				else:
					Killer(53, "Spatne typy operandu. Instrukce - " +instr.pattern['opcode'] + " order("+str(instr.ord)+")" )
			else:
				Killer(53, "Spatne typy operandu. Instrukce - " +instr.pattern['opcode'] + " order("+str(instr.ord)+")" )

	@staticmethod
	def AND(interp, instr):
		if instr.checkFrameAndVariableExist(interp) == True:
			argVarNames = instr.getVariableArgs()

			#promenna do ktere ulozime vysledek operace
			vysledek = interp.getFrame(argVarNames[0]['frame']).getVar(argVarNames[0]['name'])
			
			#extrakce hodnoty z 2 argumentu
			if instr.arguments[1]['type'] == 'var':
				op1Name = Variable.splitFrameAndName(instr.arguments[1]['value'])
				op1Value = interp.getFrame(op1Name['frame']).getVar(op1Name['name']).get()
			else:
				op1Value = instr.arguments[1]

			# #extrakce hodnoty z 3 argumentu
			if instr.arguments[2]['type'] == 'var':
				op2Name = Variable.splitFrameAndName(instr.arguments[2]['value'])
				op2Value = interp.getFrame(op2Name['frame']).getVar(op2Name['name']).get()
			else:
				op2Value = instr.arguments[2]

			#kontrola zda obe promenne maji prirazenou hodnotu
			if 'defined' in op1Value :
				if op1Value['defined'] == False:
					Killer(56, "Chybejici hodnota v promenne. Instrukce - " + instr.pattern['opcode'] + " order(" + str(instr.ord) + ")")
			if 'defined' in op2Value:		
				if op2Value['defined'] == False:
					Killer(56, "Chybejici hodnota v promenne. Instrukce - " + instr.pattern['opcode'] + " order(" + str(instr.ord) + ")")
					

			
			#kontrola zda jsou oba operandy typu bool
			if op1Value['type'] == 'bool' and op2Value['type'] == 'bool':
				
				#kontrola zda jsou zadane hodnoty opravdu typu bool
				if Variable.checkValueIsType(op1Value) and Variable.checkValueIsType(op2Value):
					#vypocet
					if op1Value['value'] == 'true' and op2Value['value'] == 'true':
						vyslednaHodnota = {'type' : 'bool', 'value' : 'true'}
					else:
						vyslednaHodnota = {'type' : 'bool', 'value' : 'false'}

					vysledek.set(vyslednaHodnota)
				else:
					Killer(53, "Spatne typy operandu. Instrukce - " +instr.pattern['opcode'] + " order("+str(instr.ord)+")" )

			else:
				Killer(53, "Spatne typy operandu. Instrukce - " +instr.pattern['opcode'] + " order("+str(instr.ord)+")" )

	@staticmethod
	def OR(interp, instr):
		if instr.checkFrameAndVariableExist(interp) == True:
			argVarNames = instr.getVariableArgs()

			#promenna do ktere ulozime vysledek operace
			vysledek = interp.getFrame(argVarNames[0]['frame']).getVar(argVarNames[0]['name'])
			
			#extrakce hodnoty z 2 argumentu
			if instr.arguments[1]['type'] == 'var':
				op1Name = Variable.splitFrameAndName(instr.arguments[1]['value'])
				op1Value = interp.getFrame(op1Name['frame']).getVar(op1Name['name']).get()
			else:
				op1Value = instr.arguments[1]

			# #extrakce hodnoty z 3 argumentu
			if instr.arguments[2]['type'] == 'var':
				op2Name = Variable.splitFrameAndName(instr.arguments[2]['value'])
				op2Value = interp.getFrame(op2Name['frame']).getVar(op2Name['name']).get()
			else:
				op2Value = instr.arguments[2]


			#kontrola zda obe promenne maji prirazenou hodnotu
			if 'defined' in op1Value :
				if op1Value['defined'] == False:
					Killer(56, "Chybejici hodnota v promenne. Instrukce - " + instr.pattern['opcode'] + " order(" + str(instr.ord) + ")")
			if 'defined' in op2Value:		
				if op2Value['defined'] == False:
					Killer(56, "Chybejici hodnota v promenne. Instrukce - " + instr.pattern['opcode'] + " order(" + str(instr.ord) + ")")
					
			
			#kontrola zda jsou oba operandy typu bool
			if op1Value['type'] == 'bool' and op2Value['type'] == 'bool':
				
				#kontrola zda jsou zadane hodnoty opravdu typu bool
				if Variable.checkValueIsType(op1Value) and Variable.checkValueIsType(op2Value):
					#vypocet
					if op1Value['value'] == 'true' or op2Value['value'] == 'true':
						vyslednaHodnota = {'type' : 'bool', 'value' : 'true'}
					else:
						vyslednaHodnota = {'type' : 'bool', 'value' : 'false'}

					vysledek.set(vyslednaHodnota)
				else:
					Killer(53, "Spatne typy operandu. Instrukce - " +instr.pattern['opcode'] + " order("+str(instr.ord)+")" )

			else:
				Killer(53, "Spatne typy operandu. Instrukce - " +instr.pattern['opcode'] + " order("+str(instr.ord)+")" )

	@staticmethod
	def NOT(interp, instr):
		if instr.checkFrameAndVariableExist(interp) == True:
			argVarNames = instr.getVariableArgs()

			#promenna do ktere ulozime vysledek operace
			vysledek = interp.getFrame(argVarNames[0]['frame']).getVar(argVarNames[0]['name'])
			
			#extrakce hodnoty z 2 argumentu
			if instr.arguments[1]['type'] == 'var':
				op1Name = Variable.splitFrameAndName(instr.arguments[1]['value'])
				op1Value = interp.getFrame(op1Name['frame']).getVar(op1Name['name']).get()
			else:
				op1Value = instr.arguments[1]

			
			#kontrola zda obe promenne maji prirazenou hodnotu
			if 'defined' in op1Value :
				if op1Value['defined'] == False :
					Killer(56, "Chybejici hodnota v promenne. Instrukce - " + instr.pattern['opcode'] + " order(" + str(instr.ord) + ")")


			#kontrola zda jsou oba operandy typu bool
			if op1Value['type'] == 'bool':
				
				#kontrola zda jsou zadane hodnoty opravdu typu bool
				if Variable.checkValueIsType(op1Value):
					#vypocet
					if op1Value['value'] == 'true':
						vyslednaHodnota = {'type' : 'bool', 'value' : 'false'}
					else:
						vyslednaHodnota = {'type' : 'bool', 'value' : 'true'}

					vysledek.set(vyslednaHodnota)
				else:
					Killer(53, "Spatne typy operandu. Instrukce - " +instr.pattern['opcode'] + " order("+str(instr.ord)+")" )

			else:
				Killer(53, "Spatne typy operandu. Instrukce - " +instr.pattern['opcode'] + " order("+str(instr.ord)+")" )


	@staticmethod
	def INT2CHAR(interp, instr):
		if instr.checkFrameAndVariableExist(interp) == True:
			argVarNames = instr.getVariableArgs()

			#promenna do ktere ulozime vysledek operace
			vysledek = interp.getFrame(argVarNames[0]['frame']).getVar(argVarNames[0]['name'])
			
			#extrakce hodnoty z 2 argumentu
			if instr.arguments[1]['type'] == 'var':
				op1Name = Variable.splitFrameAndName(instr.arguments[1]['value'])
				op1Value = interp.getFrame(op1Name['frame']).getVar(op1Name['name']).get()
			else:
				op1Value = instr.arguments[1]

			
			#kontrola zda obe promenne maji prirazenou hodnotu
			if 'defined' in op1Value :
				if op1Value['defined'] == False :
					Killer(56, "Chybejici hodnota v promenne. Instrukce - " + instr.pattern['opcode'] + " order(" + str(instr.ord) + ")")


			#kontrola zda je operand typu int
			if op1Value['type'] == 'int':
				
				#kontrola zda je operand skutecne typu int
				if Variable.checkValueIsType(op1Value):
					#vypocet
					try:
						vyslednaHodnota = {'type' : 'string', 'value' : chr(int(op1Value['value']))}
						vysledek.set(vyslednaHodnota)
					except:
						Killer(58, "Pokus prevedeni neplatne celociselne hodnoty na znak. Instrukce - " +instr.pattern['opcode'] + " order("+str(instr.ord)+")" )

				else:
					Killer(53, "Spatne typy operandu. Instrukce - " +instr.pattern['opcode'] + " order("+str(instr.ord)+")" )

			else:
				Killer(53, "Spatne typy operandu. Instrukce - " +instr.pattern['opcode'] + " order("+str(instr.ord)+")" )


	@staticmethod
	def STRI2INT(interp, instr):
		if instr.checkFrameAndVariableExist(interp) == True:
			argVarNames = instr.getVariableArgs()

			#promenna do ktere ulozime vysledek operace
			vysledek = interp.getFrame(argVarNames[0]['frame']).getVar(argVarNames[0]['name'])
			
			#extrakce hodnoty z 2 argumentu
			if instr.arguments[1]['type'] == 'var':
				op1Name = Variable.splitFrameAndName(instr.arguments[1]['value'])
				op1Value = interp.getFrame(op1Name['frame']).getVar(op1Name['name']).get()
			else:
				op1Value = instr.arguments[1]

			#extrakce hodnoty z 3 argumentu
			if instr.arguments[2]['type'] == 'var':
				op2Name = Variable.splitFrameAndName(instr.arguments[2]['value'])
				op2Value = interp.getFrame(op2Name['frame']).getVar(op2Name['name']).get()
			else:
				op2Value = instr.arguments[2]


			#kontrola zda obe promenne maji prirazenou hodnotu
			if 'defined' in op1Value :
				if op1Value['defined'] == False:
					Killer(56, "Chybejici hodnota v promenne. Instrukce - " + instr.pattern['opcode'] + " order(" + str(instr.ord) + ")")
			if 'defined' in op2Value:		
				if op2Value['defined'] == False:
					Killer(56, "Chybejici hodnota v promenne. Instrukce - " + instr.pattern['opcode'] + " order(" + str(instr.ord) + ")")
					


			#kontrola zda je 2.operand typu string a 3.operand typu int
			if op1Value['type'] == 'string' and op2Value['type'] == 'int':
				
				#kontrola zda jsou hodnoty operandu skutecne hodnoty odpovidajici jejich typum
				if Variable.checkValueIsType(op1Value) and Variable.checkValueIsType(op2Value):
					#vypocet
					try:
						vyslednaHodnota = {'type' : 'int', 'value' : ord(op1Value['value'][int(op2Value['value'])])}
						vysledek.set(vyslednaHodnota)
					except:
						Killer(58, "Pokus prevedeni znaku mimo pozici v retezci na cislo. Instrukce - " +instr.pattern['opcode'] + " order("+str(instr.ord)+")" )

				else:
					Killer(53, "Spatne typy operandu. Instrukce - " +instr.pattern['opcode'] + " order("+str(instr.ord)+")" )

			else:
				Killer(53, "Spatne typy operandu. Instrukce - " +instr.pattern['opcode'] + " order("+str(instr.ord)+")" )


	@staticmethod
	def READ(interp, instr):
		#kontrola ramce a existence promenne
		if instr.checkFrameAndVariableExist(interp) == True:
			#promenna pro ulozeni vstup 
			vysledekName = Variable.splitFrameAndName(instr.arguments[0]['value'])
			vysledek = interp.getFrame(vysledekName['frame']).getVar(vysledekName['name'])

			#zda mam nacitat ze souboru
			if hasattr(interp, 'input') == True:
				try: 
					vstup = interp.input[0]
					del interp.input[0]
				except:
					vstup = 'nil'
			#zda mam nacitat z stdin
			else:
				vstup = input()

			#konverze na specifikovany typ
			vysledekHodnota = {'type' : 'nil', 'value' : 'nil'}
			if instr.arguments[1]['value'] == 'int':			
				try:
					vysledekHodnota = {'type' : 'int', 'value' : int(vstup)}
				except:
					vysledekHodnota

			elif instr.arguments[1]['value'] == 'string':
				try:
					vysledekHodnota = {'type' : 'string', 'value' : str(vstup)}
				except:
					vysledekHodnota

			elif instr.arguments[1]['value'] == 'bool':
				if vstup.upper() == "TRUE" :
					vysledekHodnota = {'type' : 'bool', 'value' : 'true'}
				else:
					vysledekHodnota = {'type' : 'bool', 'value' : 'false'}

			#prirazeni hodnoty do promenne
			vysledek.set(vysledekHodnota)

	@staticmethod
	def WRITE(interp, instr):

		def transformSpecCharacters(str):
			
			specCharsTable = {
				"\\010" : "\n",
				"\\032" : ' ',
				"\\111" : "/"
			}

			newStr = str
			for c in specCharsTable:
				newStr = newStr.replace(c, specCharsTable[c])
			return newStr			

		#kontrola existence ramce a promenne
		if instr.checkFrameAndVariableExist(interp) == True:

			#extrakce hodnoty z 1.argumentu
			if instr.arguments[0]['type'] == 'var':
				op1Name = Variable.splitFrameAndName(instr.arguments[0]['value'])
				op1Value = interp.getFrame(op1Name['frame']).getVar(op1Name['name']).get()
			else:
				op1Value = instr.arguments[0]


			#kontrola zda je promenna deklarovana
			if 'defined' in op1Value:
				if op1Value['defined'] == False:
					Killer(56, "Chybejici hodnota v promenne. Instrukce - " + instr.pattern['opcode'] + " order(" + str(instr.ord) + ")")

			#rozhodnuti co vypsat podle datoveho typu
			if op1Value['type'] == 'string':
				print(transformSpecCharacters(op1Value['value']), end='')
			elif op1Value['type'] == 'int':
				print(op1Value['value'], end='')				
			elif op1Value['type'] == 'bool':
				print(op1Value['value'].lower(), end='')
			elif op1Value['type'] == 'nil':
				print('', end='')

	@staticmethod
	def CONCAT(interp, instr):
		#kontrola existence ramcu a promennych
		if instr.checkFrameAndVariableExist(interp) == True:

			#ziskani promenne pro ulozeni vysledku
			vysledekName = Variable.splitFrameAndName(instr.arguments[0]['value'])
			vysledek = interp.getFrame(vysledekName['frame']).getVar(vysledekName['name'])

			#extrakce hodnoty z 2 argumentu
			if instr.arguments[1]['type'] == 'var':
				op1Name = Variable.splitFrameAndName(instr.arguments[1]['value'])
				op1Value = interp.getFrame(op1Name['frame']).getVar(op1Name['name']).get()
			else:
				op1Value = instr.arguments[1]

			#extrakce hodnoty z 3 argumentu
			if instr.arguments[2]['type'] == 'var':
				op2Name = Variable.splitFrameAndName(instr.arguments[2]['value'])
				op2Value = interp.getFrame(op2Name['frame']).getVar(op2Name['name']).get()
			else:
				op2Value = instr.arguments[2]

			#kontrola zda obe promenne maji prirazenou hodnotu
			if 'defined' in op1Value :
				if op1Value['defined'] == False:
					Killer(56, "Chybejici hodnota v promenne. Instrukce - " + instr.pattern['opcode'] + " order(" + str(instr.ord) + ")")
			if 'defined' in op2Value:		
				if op2Value['defined'] == False:
					Killer(56, "Chybejici hodnota v promenne. Instrukce - " + instr.pattern['opcode'] + " order(" + str(instr.ord) + ")")
					

			#vypocet
			if op1Value['type'] == 'string' and op2Value['type'] == 'string':
				
				vysledek.set({'type' : 'string', 'value' : str(op1Value['value']) + str(op2Value['value']) })
			else:
				Killer(53, "Spatne typy operandu. Instrukce - " +instr.pattern['opcode'] + " order("+str(instr.ord)+")" )

	@staticmethod
	def STRLEN(interp, instr):
		#kontrola existence ramcu a promennych
		if instr.checkFrameAndVariableExist(interp) == True:

			#ziskani promenne pro ulozeni vysledku
			vysledekName = Variable.splitFrameAndName(instr.arguments[0]['value'])
			vysledek = interp.getFrame(vysledekName['frame']).getVar(vysledekName['name'])

			#extrakce hodnoty z 2 argumentu
			if instr.arguments[1]['type'] == 'var':
				op1Name = Variable.splitFrameAndName(instr.arguments[1]['value'])
				op1Value = interp.getFrame(op1Name['frame']).getVar(op1Name['name']).get()
			else:
				op1Value = instr.arguments[1]

					
			#kontrola zda promenna je deklarovana
			if 'defined' in op1Value :
				if op1Value['defined'] == False :
					Killer(56, "Chybejici hodnota v promenne. Instrukce - " + instr.pattern['opcode'] + " order(" + str(instr.ord) + ")")
			
			#vypocet
			if op1Value['type'] == 'string':
				
				vysledek.set({'type' : 'int', 'value' : len(op1Value['value']) })
			else:
				Killer(53, "Spatne typy operandu. Instrukce - " +instr.pattern['opcode'] + " order("+str(instr.ord)+")" )

	@staticmethod
	def GETCHAR(interp, instr):
		#kontrola existence ramcu a promennych
		if instr.checkFrameAndVariableExist(interp) == True:

			#ziskani promenne pro ulozeni vysledku
			vysledekName = Variable.splitFrameAndName(instr.arguments[0]['value'])
			vysledek = interp.getFrame(vysledekName['frame']).getVar(vysledekName['name'])

			#extrakce hodnoty z 2 argumentu
			if instr.arguments[1]['type'] == 'var':
				op1Name = Variable.splitFrameAndName(instr.arguments[1]['value'])
				op1Value = interp.getFrame(op1Name['frame']).getVar(op1Name['name']).get()
			else:
				op1Value = instr.arguments[1]

			#extrakce hodnoty z 2 argumentu
			if instr.arguments[2]['type'] == 'var':
				op2Name = Variable.splitFrameAndName(instr.arguments[2]['value'])
				op2Value = interp.getFrame(op2Name['frame']).getVar(op2Name['name']).get()
			else:
				op2Value = instr.arguments[2]
					
			#kontrola zda obe promenne maji prirazenou hodnotu
			if 'defined' in op1Value :
				if op1Value['defined'] == False:
					Killer(56, "Chybejici hodnota v promenne. Instrukce - " + instr.pattern['opcode'] + " order(" + str(instr.ord) + ")")
			if 'defined' in op2Value:		
				if op2Value['defined'] == False:
					Killer(56, "Chybejici hodnota v promenne. Instrukce - " + instr.pattern['opcode'] + " order(" + str(instr.ord) + ")")
					

			#vypocet
			if op1Value['type'] == 'string' and op2Value['type'] == 'int':
				
				if int(op2Value['value']) < len(op1Value['value']) and int(op2Value['value']) >= 0:
					vysledek.set({'type' : 'string', 'value' : op1Value['value'][int(op2Value['value'])] })
				else:
					Killer(58, "Pokus o ziskani znaku z retezce mimo hranice retezce. Instrukce - " +instr.pattern['opcode'] + " order("+str(instr.ord)+")" )

			else:
				Killer(53, "Spatne typy operandu. Instrukce - " +instr.pattern['opcode'] + " order("+str(instr.ord)+")" )

	@staticmethod
	def SETCHAR(interp, instr):
		#kontrola existence ramcu a promennych
		if instr.checkFrameAndVariableExist(interp) == True:

			#ziskani promenne pro ulozeni vysledku
			vysledekName = Variable.splitFrameAndName(instr.arguments[0]['value'])
			vysledek = interp.getFrame(vysledekName['frame']).getVar(vysledekName['name'])
			op0Value = vysledek.get()

			#extrakce hodnoty z 2 argumentu
			if instr.arguments[1]['type'] == 'var':
				op1Name = Variable.splitFrameAndName(instr.arguments[1]['value'])
				op1Value = interp.getFrame(op1Name['frame']).getVar(op1Name['name']).get()
			else:
				op1Value = instr.arguments[1]

			#extrakce hodnoty z 2 argumentu
			if instr.arguments[2]['type'] == 'var':
				op2Name = Variable.splitFrameAndName(instr.arguments[2]['value'])
				op2Value = interp.getFrame(op2Name['frame']).getVar(op2Name['name']).get()
			else:
				op2Value = instr.arguments[2]
					
			#kontrola zda obe promenne maji prirazenou hodnotu
			if 'defined' in op1Value :
				if op1Value['defined'] == False:
					Killer(56, "Chybejici hodnota v promenne. Instrukce - " + instr.pattern['opcode'] + " order(" + str(instr.ord) + ")")
			if 'defined' in op2Value:		
				if op2Value['defined'] == False:
					Killer(56, "Chybejici hodnota v promenne. Instrukce - " + instr.pattern['opcode'] + " order(" + str(instr.ord) + ")")
					

			#vypocet
			if op0Value['type'] == 'string' and op1Value['type'] == 'int' and op2Value['type'] == 'string':
				
				if int(op1Value['value']) < len(op0Value['value']) and len(op2Value['value']) > 0 :
					newString = op0Value['value'][:int(op1Value['value'])] + op2Value['value'][0] + op0Value['value'][int(op1Value['value'])+1:]
					vysledek.set({'type' : 'string', 'value' : newString })
				else:
					Killer(58, "Pokus o nastaveni znaku retezce mimo hranice retezce nebo nastaveni znaku na prazdny znak.\n Instrukce - " +instr.pattern['opcode'] + " order("+str(instr.ord)+")" )

			else:
				Killer(53, "Spatne typy operandu. Instrukce - " +instr.pattern['opcode'] + " order("+str(instr.ord)+")" )

	@staticmethod
	def TYPE(interp, instr):
		#kontrola existence ramcu a promennych
		if instr.checkFrameAndVariableExist(interp) == True:

			#ziskani promenne pro ulozeni vysledku
			vysledekName = Variable.splitFrameAndName(instr.arguments[0]['value'])
			vysledek = interp.getFrame(vysledekName['frame']).getVar(vysledekName['name'])

			#extrakce hodnoty z 2 argumentu
			if instr.arguments[1]['type'] == 'var':
				op1Name = Variable.splitFrameAndName(instr.arguments[1]['value'])
				op1Value = interp.getFrame(op1Name['frame']).getVar(op1Name['name']).get()
			else:
				op1Value = instr.arguments[1]
	
			#kontrola zda je promenna deklarovana
			if 'defined' in op1Value :
				if op1Value['defined'] == False:
					typeValue = ''					
				else:
					typeValue = op1Value['type']
			else:
				typeValue = op1Value['type']
			
			#ulozeni hodnoty
			vysledek.set({'type' : 'string', 'value' : typeValue})			

	@staticmethod
	def LABEL(interp, instr):

		for i in range(1, len(interp.prog)):
			if instr == interp.prog[i]:
				interp.labels[instr.arguments[0]['value']]['index'] = i #prirazeni labelu index ve skutecne posloupnosti instrukci
				# print(interp.labels[instr.arguments[0]['value']])

	@staticmethod
	def JUMP(interp, instr):
		#kontrola zda je navesti definovane
		try:

			dalsiInstrukce = interp.labels[instr.arguments[0]['value']]['index']
			if  dalsiInstrukce < len(interp.prog):
				interp.nextInstr = dalsiInstrukce
			else:
				Killer(99, "Vnitrni chyba pokus na skok na instrukci mimo definovane pole. Instrukce - " +instr.pattern['opcode'] + " order("+str(instr.ord)+")")			
		except:
			Killer(52, "Pokus o skok na nedefinovane navesti. Instrukce - " +instr.pattern['opcode'] + " order("+str(instr.ord)+")")

	def JUMPIFEQ(interp, instr):
		
		#kontrola existence ramcu a promennych
		if instr.checkFrameAndVariableExist(interp) == True:

			skoc = False

			#extrakce hodnoty z 2 argumentu
			if instr.arguments[1]['type'] == 'var':
				op1Name = Variable.splitFrameAndName(instr.arguments[1]['value'])
				op1Value = interp.getFrame(op1Name['frame']).getVar(op1Name['name']).get()
			else:
				op1Value = instr.arguments[1]

			#extrakce hodnoty z 3 argumentu
			if instr.arguments[2]['type'] == 'var':
				op2Name = Variable.splitFrameAndName(instr.arguments[2]['value'])
				op2Value = interp.getFrame(op2Name['frame']).getVar(op2Name['name']).get()
			else:
				op2Value = instr.arguments[2]

			#kontrola zda obe promenne maji prirazenou hodnotu
			if 'defined' in op1Value :
				if op1Value['defined'] == False:
					Killer(56, "Chybejici hodnota v promenne. Instrukce - " + instr.pattern['opcode'] + " order(" + str(instr.ord) + ")")
			if 'defined' in op2Value:		
				if op2Value['defined'] == False:
					Killer(56, "Chybejici hodnota v promenne. Instrukce - " + instr.pattern['opcode'] + " order(" + str(instr.ord) + ")")
					


			#kontrola zda jsou oba operandy typu int
			if op1Value['type'] == 'int' and op2Value['type'] == 'int':
				#kontrola zda jsou zadane hodnoty opravu cela cisla
				if Variable.checkValueIsType(op1Value) and Variable.checkValueIsType(op2Value):
					#vypocet
					if int(op1Value['value']) == int(op2Value['value']):
						skoc = True
				
				else:
					Killer(53, "Spatne typy oper2andu. Instrukce - " +instr.pattern['opcode'] + " order("+str(instr.ord)+")" )

			#kontrola zda jsou oba operandy typu bool
			elif op1Value['type'] == 'bool' and op2Value['type'] == 'bool':
				#kontrola zda jsou zadane hodnoty opravdu typu bool
				if Variable.checkValueIsType(op1Value) and Variable.checkValueIsType(op2Value):
					#vypocet
					if op1Value['value'] == op2Value['value']:
						skoc = True

				else:
					Killer(53, "Spatne typy operandu. Instrukce - " +instr.pattern['opcode'] + " order("+str(instr.ord)+")" )
			
			#kontrola zda jsou oba operandy typu string
			elif op1Value['type'] == 'string' and op2Value['type'] == 'string':
				#kontrola zda jsou zadane hodnoty opravdu typu bool
				if Variable.checkValueIsType(op1Value) and Variable.checkValueIsType(op2Value):
					#vypocet
					if op1Value['value'] == op2Value['value']:
						skoc = True
				else:
					Killer(53, "Spatne typy operandu. Instrukce - " +instr.pattern['opcode'] + " order("+str(instr.ord)+")" )
			
			#kontrola zda jsou oba operandy typu nil
			elif op1Value['type'] == 'nil' and op2Value['type'] == 'nil' : 
				#kontrola zda jsou zadane hodnoty opravdu typu bool
				if Variable.checkValueIsType(op1Value) and Variable.checkValueIsType(op2Value):
					#vypocet
					if op1Value['value'] == op2Value['value']:
						skoc = True
				else:
					Killer(53, "Spatne typy operandu. Instrukce - " +instr.pattern['opcode'] + " order("+str(instr.ord)+")" )
			
			#kontrola zda je pouze jeden z operandu nil
			elif op1Value['type'] == 'nil' or op2Value['type'] == 'nil':
				skoc = False
			else:
				Killer(53, "Spatne typy operandu. Instrukce - " +instr.pattern['opcode'] + " order("+str(instr.ord)+")" )

		#pokud ma dojit ke skoku
		if skoc == True:
			#kontrola zda je navesti definovane
			try:
				dalsiInstrukce = interp.labels[instr.arguments[0]['value']]['index']
				if  dalsiInstrukce < len(interp.prog):
			
					interp.nextInstr = dalsiInstrukce
				else:
					Killer(99, "Vnitrni chyba pokus na skok na instrukci mimo definovane pole. Instrukce - " +instr.pattern['opcode'] + " order("+str(instr.ord)+")")			

			except:
				Killer(52, "Pokus o skok na nedefinovane navesti. Instrukce - " +instr.pattern['opcode'] + " order("+str(instr.ord)+")")

		#pokud nedojde ke skoku pokracuje se dalsi instrukci
		else:
			interp.nextInstr += 1


	def JUMPIFNEQ(interp, instr):
		
		#kontrola existence ramcu a promennych
		if instr.checkFrameAndVariableExist(interp) == True:

			skoc = False

			#extrakce hodnoty z 2 argumentu
			if instr.arguments[1]['type'] == 'var':
				op1Name = Variable.splitFrameAndName(instr.arguments[1]['value'])
				op1Value = interp.getFrame(op1Name['frame']).getVar(op1Name['name']).get()
			else:
				op1Value = instr.arguments[1]

			#extrakce hodnoty z 3 argumentu
			if instr.arguments[2]['type'] == 'var':
				op2Name = Variable.splitFrameAndName(instr.arguments[2]['value'])
				op2Value = interp.getFrame(op2Name['frame']).getVar(op2Name['name']).get()
			else:
				op2Value = instr.arguments[2]

			#kontrola zda obe promenne maji prirazenou hodnotu
			if 'defined' in op1Value :
				if op1Value['defined'] == False:
					Killer(56, "Chybejici hodnota v promenne. Instrukce - " + instr.pattern['opcode'] + " order(" + str(instr.ord) + ")")
			if 'defined' in op2Value:		
				if op2Value['defined'] == False:
					Killer(56, "Chybejici hodnota v promenne. Instrukce - " + instr.pattern['opcode'] + " order(" + str(instr.ord) + ")")
					


			#kontrola zda jsou oba operandy typu int
			if op1Value['type'] == 'int' and op2Value['type'] == 'int':
				#kontrola zda jsou zadane hodnoty opravu cela cisla
				if Variable.checkValueIsType(op1Value) and Variable.checkValueIsType(op2Value):
					#vypocet
					if int(op1Value['value']) != int(op2Value['value']):
						skoc = True
				
				else:
					Killer(53, "Spatne typy oper2andu. Instrukce - " +instr.pattern['opcode'] + " order("+str(instr.ord)+")" )

			#kontrola zda jsou oba operandy typu bool
			elif op1Value['type'] == 'bool' and op2Value['type'] == 'bool':
				#kontrola zda jsou zadane hodnoty opravdu typu bool
				if Variable.checkValueIsType(op1Value) and Variable.checkValueIsType(op2Value):
					#vypocet
					if op1Value['value'] != op2Value['value']:
						skoc = True

				else:
					Killer(53, "Spatne typy operandu. Instrukce - " +instr.pattern['opcode'] + " order("+str(instr.ord)+")" )
			
			#kontrola zda jsou oba operandy typu string
			elif op1Value['type'] == 'string' and op2Value['type'] == 'string':
				#kontrola zda jsou zadane hodnoty opravdu typu bool
				if Variable.checkValueIsType(op1Value) and Variable.checkValueIsType(op2Value):
					#vypocet
					if op1Value['value'] != op2Value['value']:
						skoc = True
				else:
					Killer(53, "Spatne typy operandu. Instrukce - " +instr.pattern['opcode'] + " order("+str(instr.ord)+")" )
			
			#kontrola zda jsou oba operandy typu nil
			elif op1Value['type'] == 'nil' and op2Value['type'] == 'nil' : 
				#kontrola zda jsou zadane hodnoty opravdu typu bool
				if Variable.checkValueIsType(op1Value) and Variable.checkValueIsType(op2Value):
					#vypocet
					if op1Value['value'] != op2Value['value']:
						skoc = True
				else:
					Killer(53, "Spatne typy operandu. Instrukce - " +instr.pattern['opcode'] + " order("+str(instr.ord)+")" )
			
			#kontrola zda je pouze jeden z operandu nil
			elif op1Value['type'] == 'nil' or op2Value['type'] == 'nil':
				skoc = False
			else:
				Killer(53, "Spatne typy operandu. Instrukce - " +instr.pattern['opcode'] + " order("+str(instr.ord)+")" )

		#pokud ma dojit ke skoku
		if skoc == True:
			#kontrola zda je navesti definovane
			try:
				dalsiInstrukce = interp.labels[instr.arguments[0]['value']]['index']
				if  dalsiInstrukce < len(interp.prog):
			
					interp.nextInstr = dalsiInstrukce
				else:
					Killer(99, "Vnitrni chyba pokus na skok na instrukci mimo definovane pole. Instrukce - " +instr.pattern['opcode'] + " order("+str(instr.ord)+")")			

			except:
				Killer(52, "Pokus o skok na nedefinovane navesti. Instrukce - " +instr.pattern['opcode'] + " order("+str(instr.ord)+")")

		#pokud nedojde ke skoku pokracuje se dalsi instrukci
		else:
			interp.nextInstr += 1


	@staticmethod
	def EXIT(interp, instr):
		#kontrola existence ramcu a promennych
		if instr.checkFrameAndVariableExist(interp) == True:

			#ziskani hodnoty navratoveho kodu
			if instr.arguments[0]['type'] == 'var':
				op1Name = Variable.splitFrameAndName(instr.arguments[0]['value'])
				op1Value = interp.getFrame(op1Name['frame']).getVar(op1Name['name']).get()
			else:
				op1Value = instr.arguments[0]


			#kontrola zda ma argument prirazenou hodnotu
			if 'defined' in op1Value :
				if op1Value['defined'] == False:
					Killer(56, "Chybejici hodnota v promenne. Instrukce - " + instr.pattern['opcode'] + " order(" + str(instr.ord) + ")")

			#kontrola zda je operand typu int
			if op1Value['type'] == 'int':
				if int(op1Value['value']) >= 0 and int(op1Value['value']) <= 49:
					exit(int(op1Value['value']))
				else:
					Killer(57, "Ukonceni programu s nevalidni ciselnou hodnotou mimo 0-49.  Instrukce - " +instr.pattern['opcode'] + " order("+str(instr.ord)+")")
			else:
				Killer(53, "Spatny typ operandu. Podporovan poze typ int. Instrukce - " +instr.pattern['opcode'] + " order("+str(instr.ord)+")")

	################################################################################################################################
	@classmethod
	def validOrder(cls, i):
		if int(i) <= 0:
			return False
		for o in cls.order:
			if o == i:
				return False
		return True
	
	@classmethod
	def addOrder(cls, i):
		cls.order.append(i)

	#################################################################################################################################

	def __init__(self, xmlDom):

		self.xmlDom = xmlDom
		self.checkOpCode()	#kontrola validni opcode instrukce
		self.checkOrder()	#kontrola validniho order instrukce
		self.extractArguments()	#extrakce argumentu
		self.checkStaticArgsType()
		
		# self.prnt()	#tisk vytvorene instrukce	
		# print(self.retVariableArgs())

	# zkontroluje existenci promennych a ramcu v paratetrech instrukce
	# vraci True nebo ukoncuje prislusnou chybou
	def checkFrameAndVariableExist(self, interp):
		varArgs = self.getVariableArgs()
		for var in varArgs:
			frame = interp.getFrame(var['frame'])
			if frame != None:
				if frame.existVar(var['name']) == False:
					Killer(54, "Pristup k neexstujici promenne - "  + var['frame'] + "@" + var['name'] + " instrukce - " + self.pattern['opcode'] + " order("+ str(self.ord) + ")" )
			else:
				Killer(55, "Neexistujici ramec - " + var['frame'] + " instrukce - " + self.pattern['opcode'] + " order("+ str(self.ord) + ")")
		return True


	#zkontroluje zda je validni opcode, ulozi pattern instrukce
	def checkOpCode(self):
		instrType = Instruction.getMethodType(self.xmlDom.getAttribute('opcode'))
		if instrType == None:
			Killer(32, "Neznamy operacni kod instrukce")
		else:
			self.pattern = instrType

	#kontrola zda poradi instrukce neni duplicitni
	def checkOrder(self):
		order = self.xmlDom.getAttribute('order')
		if  Instruction.validOrder(order) == True:
			Instruction.addOrder(order)
			self.ord = int(order)
		else:
			Killer(32, "Duplicitni nebo zaporny argument 'order' " + order +" instrukce - " +self.pattern['opcode'])

	#vyjme z xml argumenty a ulozi je
	def extractArguments(self):
		argTags = ['', 'arg1', 'arg2', 'arg3']
		argOrd = []
		validArgOrd = False
		arguments = []
		self.arguments = []


		for i in range(1,4):
			arg = self.xmlDom.getElementsByTagName(argTags[i])


			if len(arg) == 1:
				# ulozeni hodnot
				try:
					arguments.append({'type': arg[0].attributes['type'].value, 'value': arg[0].firstChild.data})

				except:
					arguments.append({'type': arg[0].attributes['type'].value, 'value': '' })

				#kontrola zda zadany typ v argumentu odpovida zadane hodnote
				if Variable.checkValueIsType(arguments[-1]) == False:
					Killer(32, "Zadany typ argumentu instrukce se neshoduje s typem v argumentu. Instrukce - "+self.pattern['opcode']+" order("+str(self.ord)+"), argument - " + argTags[i])
				argOrd.append(True)

			elif len(arg) == 0:
				argOrd.append(False)
			elif len(arg) > 1:
				Killer(32, "Chyba opakovane zadan argument instrukce. Instrukce - "+self.pattern['opcode']+" order("+str(self.ord)+"), argument - " + argTags[i])
			
			#prosel jsem vsechny mozne xml argumenty, ukladam nactene 
			# if i == 3:
			# 	#kontrola zda poradi argumentu odpovida jejich jmenum 
			# 	#dodelat
			# 	self.arguments = arguments
			# 	arguments = []
		
		#konrola zda argumenty jsou v radnem poradi
		if argOrd[0] and not argOrd[1] and not argOrd[2]:
			validArgOrd = True
		elif argOrd[0] and argOrd[1] and not argOrd[2]:
			validArgOrd = True
		elif argOrd[0] and argOrd[1] and argOrd[2]:
			validArgOrd = True
		elif not argOrd[0] and not argOrd[1] and not argOrd[2]:
			validArgOrd = True

		if validArgOrd:
			self.arguments = arguments
			arguments = []
		else:
			Killer(32, "Chybne argumenty instrukce, poradi a pocet argumentu nesedi. Instrukce - "+self.pattern['opcode']+" order("+str(self.ord)+")")
			


	#zkontroluje spravny typ a pocet jednotlivych argumentu, ne obsah promenych a datovych typu konstant - chyba 53
	def checkStaticArgsType(self):
		validni = []	#pole obsahujici True|False jednotlivych arg
		argTags = ['arg1', 'arg2', 'arg3']
		#kontrola zda se pocet nactenych a ocekavanych argumentu rovna
		if(len(self.arguments) == len(self.pattern['args'])):
			
			for i in range(0,len(self.arguments)):
				
				#zda skutecny argument je opravdu promenna
				if self.pattern['args'][i][argTags[i]]['aType'] == 'var' and self.arguments[i]['type'] == 'var':
					#kontrola zda promenna je spravne zapsana
					if 'GF' in self.arguments[i]['value'] or 'TF' in self.arguments[i]['value'] or 'LF' in self.arguments[i]['value']:
						True
					else:
						Killer(32, "Chybne zapsana promenna, chybny ramec. Promenna - " + self.arguments[i]['value'] + ", instrukce - " + self.pattern['opcode'] + " order("+str(self.ord) + ")")
					
					validni.append(True)

				elif self.pattern['args'][i][argTags[i]]['aType'] == 'var' and self.arguments[i]['type'] != 'var':
					validni.append(False)
				
				#zda skutecny argument je opravdu label
				if self.pattern['args'][i][argTags[i]]['aType'] == 'label' and self.arguments[i]['type'] == 'label':
					validni.append(True)
				elif self.pattern['args'][i][argTags[i]]['aType'] == 'label' and self.arguments[i]['type'] != 'label':
					validni.append(False)

				#zda skutecny argument je opravdu type
				if self.pattern['args'][i][argTags[i]]['aType'] == 'type' and self.arguments[i]['type'] == 'type':
					validni.append(True)
				elif self.pattern['args'][i][argTags[i]]['aType'] == 'type' and self.arguments[i]['type'] != 'type':
					validni.append(False)

				#zda skutecny argument je opravdu symbol - int, string, int, nil, var
				if self.pattern['args'][i][argTags[i]]['aType'] == 'symb':
					if self.arguments[i]['type'] == 'int' or self.arguments[i]['type'] == 'string' or self.arguments[i]['type'] == 'bool' or self.arguments[i]['type'] == 'nil' or self.arguments[i]['type'] == 'var':
						if self.arguments[i]['type'] == 'var':
							#kontrola zda promenna je spravne zapsana
							if 'GF' in self.arguments[i]['value'] or 'TF' in self.arguments[i]['value'] or 'LF' in self.arguments[i]['value']:
								True
							else:
								Killer(32, "Chybne zapsana promenna, chybny ramec. Promenna - " + self.arguments[i]['value'] + ", instrukce - " + self.pattern['opcode'] + " order("+str(self.ord) + ")")
						validni.append(True)
					else:
						validni.append(False)

			#pokud instrukce je skutecne bez argumentu
			if len(self.arguments) == 0:
				validni.append(True)
			
			vyslValid = True
			for bol in validni:
				vyslValid = vyslValid and bol
			
			#nektery z argumentu je chybny -> chyba 53
			if vyslValid == False:
				Killer(53, "Spatne typy operandu u instrukce - " + self.pattern['opcode'] + " order("+str(self.ord)+")")
		else:
			#vyjimka pokud jsou zasobnikove instrukce zadany bez argumentu
			if self.pattern['opcode'] == 'PUSHS' and len(self.arguments) == 0:	
				True
			elif self.pattern['opcode'] == 'POPS' and len(self.arguments) == 0: 
				True
			else:
				Killer(32, "Instrukce ma neocekavany pocet argumentu: " + self.pattern['opcode'] + " order("+str(self.ord)+")")

	#vraci pole promenych v argumentech instrukce
	#kazda polozka {'frame': ramec, 'name': jmeno_promenne}
	def getVariableArgs(self):
		variables = []
		for arg in self.arguments:
			if arg['type'] == 'var':
				splited = arg['value'].split('@')
				#kontrola zda je promenna lexikalne validni
				if len(splited) == 2:
					#kontrola zda je validni nazev ramce GF|TF|LF ne jakykoliv jiny
					if splited[0] == 'TF' or splited[0] == 'GF' or splited[0] == 'LF':
						variables.append({'frame': splited[0], 'name': splited[1]})
					else:
						Killer(32, "Neznamy nazev ramce promenne v argumentu instrukce - " + self.pattern['opcode'] + " order("+self.ord+")")
				else:
					Killer(32, "Chybny zapis promenne v argumentu instrukce - " + self.pattern['opcode'] + " order("+self.ord+")")

		return variables

	#spusteni vykonavani instrukce
	def run(self, interp):
		opcode = self.pattern['opcode']
		# print(opcode + " " + str(self.ord))

		if opcode == "MOVE":
			Instruction.MOVE(interp, self)

		if opcode == "CREATEFRAME":
			Instruction.CREATEFRAME(interp)

		if opcode == "PUSHFRAME":
			Instruction.PUSHFRAME(interp)

		if opcode == "POPFRAME":
			Instruction.POPFRAME(interp)

		if opcode == "DEFVAR":
			Instruction.DEFVAR(interp, self)

		if opcode == "CALL":
			Instruction.CALL(interp, self)

		if opcode == "RETURN":
			Instruction.RETURN(interp)

		if opcode == "PUSHS":
			Instruction.PUSHS(interp, self)

		if opcode == "POPS":
			Instruction.POPS(interp, self)

		if opcode == "ADD":
			Instruction.ADD(interp, self)

		if opcode == "SUB":
			Instruction.SUB(interp, self)

		if opcode == "MUL":
			Instruction.MUL(interp, self)

		if opcode == "IDIV":
			Instruction.IDIV(interp, self)

		if opcode == "LT":
			Instruction.LT(interp, self)

		if opcode == "EQ":
			Instruction.EQ(interp, self)

		if opcode == "GT":
			Instruction.GT(interp, self)

		if opcode == "AND":
			Instruction.AND(interp, self)

		if opcode == "OR":
			Instruction.OR(interp, self)

		if opcode == "NOT":
			Instruction.NOT(interp, self)

		if opcode == "INT2CHAR":
			Instruction.INT2CHAR(interp, self)

		if opcode == "STRI2INT":
			Instruction.STRI2INT(interp, self)

		if opcode == "READ":
			Instruction.READ(interp, self)

		if opcode == "WRITE":
			Instruction.WRITE(interp, self)

		if opcode == "CONCAT":
			Instruction.CONCAT(interp, self)

		if opcode == "STRLEN":
			Instruction.STRLEN(interp, self)

		if opcode == "GETCHAR":
			Instruction.GETCHAR(interp, self)

		if opcode == "SETCHAR":
			Instruction.SETCHAR(interp, self)

		if opcode == "TYPE":
			Instruction.TYPE(interp, self)

		if opcode == "LABEL":
			Instruction.LABEL(interp, self)

		if opcode == "JUMP":
			Instruction.JUMP(interp, self)

		if opcode == "JUMPIFEQ":
			Instruction.JUMPIFEQ(interp, self)


		if opcode == "JUMPIFNEQ":
			Instruction.JUMPIFNEQ(interp, self)

		if opcode == "EXIT":
			Instruction.EXIT(interp, self)

	#tisk instrukce
	def prnt(self):
		print('--------------------------------------------')
		if hasattr(self, 'pattern'):
			print("Predpis Instrukce: ")
			print("  ", end=" ")
			print(self.pattern)

		if hasattr(self, 'ord'):
			print("Poradi Instrukce: ", end=" ")
			print(self.ord)

		if hasattr(self, 'arguments'):
			print("Argumenty Instrukce: ", end=" "),
			print(self.arguments)
		print('--------------------------------------------')
