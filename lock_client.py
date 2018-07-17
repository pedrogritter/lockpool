#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Aplicaçoes distribuidas - Projeto 2 - lock_skeleton.py
Grupo: 22
Numeros de aluno: 44964, 46579
"""
# Zona para fazer imports
import argparse
import net_client
import lock_stub as lstub
import random


#Program lock_client.py

parser = argparse.ArgumentParser(description="Argument Parser For lock_server.py")
parser.add_argument('host', type=str, help="Server host ip")
parser.add_argument('port', type=int, help="Server socket port")
args = parser.parse_args()

client_id = random.randint(1,100)

connected = True

socket = net_client.server(args.host, args.port)
socket.connect()

while connected:
    #Call lock_stub.py

    try:
        lstub = lstub.LockStub()
        command = raw_input("Comando > ")
        command = command.split(" ")

        #Command Exit, exits command prompt
        if command[0] == "EXIT":
            connected = False

        #If given empty set of commands return this
        elif len(command) == 0:
            print "UNKOWN COMMAND"

        elif command[0] == 'LOCK' or command[0] =='RELEASE':
            if len(command) != 2:
                print 'NOT ENOUGH ARGUMENTS'

            elif command[0] == "LOCK":
                comm = socket.send_receive(lstub.lock(client_id, int(command[1])))
                print comm

            elif command[0] == "RELEASE":
                comm = socket.send_receive(lstub.release(client_id, int(command[1])))
                print comm

        elif command[0] == "TEST" or command[0] == "STATS":

            if len(command) != 1:
                print 'NOT ENOUGH ARGUMENTS'

            elif command[0] == "TEST":
                comm = socket.send_receive(lstub.test(int(command[1])))
                print comm

            elif command[0] == "STATS":
                comm = socket.send_receive(lstub.stats(int(command[1])))
                print comm
        else:
            if command[0] == "STATS-Y":
                comm = socket.send_receive(lstub.stats_y())
                print comm

            elif command[0] == "STATS-N":
                comm = socket.send_receive(lstub.stats_n())
                print comm

    except:
        print "ERROR: Socket Closed!"
        connected = False

socket.close()
