#!/usr/bin/python
# -*- coding: utf-8 -*-
"""

"""
# Zona para fazer imports

import sys, socket as s
import pickle
import struct
from sock_utils import *

# Programa principal

class LockStub:

	def __init__(self):
		self.msg=[]

	def lock(self,ncliente,nrecurso):
		try:
			self.msg = [10,ncliente,nrecurso]
			self.msg = serialize(self)
			msgsize = struct.pack('!i',len(self.msg))
			return (self.msg,msgsize)
		except:
			print "Erro de serelisacao msg nao enviada!"

	def release(self,ncliente,nrecurso):
		try:
			self.msg = [20,ncliente,nrecurso]
			self.msg = serialize(self)
			msgsize = struct.pack('!i',len(self.msg))
			return (self.msg,msgsize)
		except:
			print "Erro de serelisacao msg na enviada!"

	def test(self,nrecurso):
		try:
			self.msg = [30,nrecurso]
			self.msg = serialize(self)
			msgsize = struct.pack('!i',len(self.msg))
			return (self.msg,msgsize)
		except:
			print "Erro de serelisacao msg na enviada!"

	def stats(self,nrecurso):
		try:
			self.msg = [40,nrecurso]
			self.msg = serialize(self)
			msgsize = struct.pack('!i',len(self.msg))
			return (self.msg,msgsize)
		except:
			print "Erro de serelisacao msg na enviada!"

	def stats_y(self):
		try:
			self.msg = [50]
			self.msg = serialize(self)
			msgsize = struct.pack('!i',len(self.msg))
			return (self.msg,msgsize)
		except:
			print "Erro de serelisacao msg na enviada!"

	def stats_n(self):
		try:
			self.msg = [60]
			self.msg = serialize(self)
			msgsize = struct.pack('!i',len(self.msg))
			return (self.msg,msgsize)
		except:
			print "Erro de serelisacao msg na enviada!"
