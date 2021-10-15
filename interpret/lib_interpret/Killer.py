#!/usr/bin/env

import sys

#ukonci beh scriptu, vrati navrotovy kod - errcode, na stderr tiskne hlasku err
def Killer(errcode, err):
	sys.stderr.write("INTERPRET ERR: "+str(errcode)+": "+ err+"\n")
	sys.exit(errcode)	
