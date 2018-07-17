#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Aplicaçoes distribuidas - Projeto 2 - lock_skeleton.py
Grupo: 22
Numeros de aluno: 44964, 46579
"""
# Zona para fazer imports
from threading import Lock
import time, argparse, select, pickle, struct, lock_pool as lpool, lock_skel as skel
import sock_utils as util
# código do programa locl_server.py

parser = argparse.ArgumentParser(description="Argument Parser For lock_server.py")
parser.add_argument('port', type=int, help="Give the server ")
parser.add_argument('num_resources', type =int, help="Number of resources stored at the server" )
parser.add_argument('num_lock_per_resource', type=int, help="Number of locks allowed per resource")
parser.add_argument('max_lock_allowed', type=int, help="Max number of resources locked at a given time")
parser.add_argument("lock_time", type=int, help ="Lock time in seconds")
args = parser.parse_args()

#Create lock_pool a pool of lock_resource instances
pool = lpool.lock_pool(args.num_resources, args.num_lock_per_resource, args.max_lock_allowed, args.lock_time)

#Get Host ip
HOST =  util.gethostip()

#Create a tcp listener server
listener_socket = util.create_tcp_server_socket(HOST, args.port, 1)

#Create a list of active sockets
SocketList = [listener_socket]

while True:
    R, W, X = select.select(SocketList, [], [])
    for socket in R:
        if socket is listener_socket:
            (conn_sock, addr) = listener_socket.accept()
            try:
                (addr, port) = conn_sock.getpeername()
                print "New client connected: ", addr[0], ":", addr[1]
                SocketList.append(conn_sock)
            except:
                print "Socket Closed! ------ End Connection"
                SocketList.remove(conn_sock)
                conn_sock.close()
        else:
            try:
                pool.clear_expired_locks()
                message_bytes = util.receive_all(socket, 4)

                if message_bytes != "None":
                    #Get Client request
                    bytesize = util.size_unpack(message_bytes)
                    getmessage = util.receive_all(socket, bytesize)
                    print util.deserialize(getmessage)
                    #Launch server skeleton & process message
                    skeleton = skel.LockSkel()
                    answer = skeleton.ServerHelper(getmessage, pool, args)
                    # Answer must be serialized and sent
                    # answer = util.serialize(answer)
                    # answer_size = util.msg_length(answer)
                    # socket.sendall(answer_size)
                    # socket.sendall(answer)
                    util.serial_send(socket, answer)
                    #Answer sent by server to client
                else:
                    (addr, port) = socket.getpeername()
                    print "This client disconnected: ", addr[0], ':', addr[1]
                    SocketList.remove(socket)

            except:
                (addr, port) = socket.getpeername()
                print "This client disconnected: ", addr[0], ':', addr[1]
                SocketList.remove(socket)
