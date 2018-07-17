#!/usr/bin/python
# -*- coding: utf-8 -*-
"""

"""
# Zona para fazer imports

import sys, socket as s
import time, argparse,select,pickle,struct
import lock_pool38
from sock_utils import *
# Programa principal

class LockSkel:
    def __init__(self):
        self.resposta=[]

    def processMessage(self,rbytes,recurso,args):
        rec = deserialize(rbytes)
        if(rec[0]==10):
            try:
                if len(rec) !=3:
                    raise
                if int(rec[2]) >= 0 and int(rec[2]) < len(recurso.l):
                    response=recurso.lock(int(rec[1]), int(rec[2]), args.time_block)
                    if response:
                        self.resposta=[11,True]
                    else:
                        self.resposta=[11,False]
                else:
                    self.resposta=[11,None]
            except:
                self.resposta=[11,None]
        elif(rec[0]==20):
            try:
                if len(rec)!=3:
                    raise
                if int(rec[2]) >= 0 and int(rec[2]) < len(recurso.l):
                    response=recurso.release(int(rec[1]), int(rec[2]))
                    if response:
                        self.resposta=[21,True]
                    else:
                        self.resposta=[21,False]
                else:
                    self.resposta=[21,None]
            except:
                self.resposta=[21,None]
        elif(rec[0]==30):
            try:
                if len(rec) !=2:
                    raise
                if int(rec[1]) >= 0 and int(rec[1]) < len(recurso.l):
                    response=recurso.test(int(rec[1]))
                    if response:
                        self.resposta=[31,True]
                    else:
                        self.resposta=[31,False]
                else:
                    self.resposta=[31,None]
            except:
                self.resposta=[31,None]
        elif(rec[0]==40):
            try:
                if len(rec)!=2:
                    raise
                if int(rec[1]) >= 0 and int(rec[1]) < len(recurso.l):
                    n=recurso.stat(int(rec[1]))
                    self.resposta=[41,n]
                else:
                    self.resposta=[41,None]
            except:
                self.resposta=[41,None]

        elif(rec[0]==50):   #possivel exceção

                n=recurso.stat_y()
                self.resposta=[51,n]

        elif(rec[0]==60):

                n=recurso.stat_n()
                self.resposta=[61,n]

        else:
            self.resposta=[None]

        return self.resposta
