#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Aplicaçoes distribuidas - Projeto 2 - lock_skeleton.py
Grupo: 22
Numeros de aluno: 44964, 46579
"""
# Zona para fazer imports
import sock_utils as util

# definição da classe server
class server:
    """
    Classe para abstrair uma ligação a um servidor TCP. Implementa métodos
    para estabelecer a ligação, para envio de um comando e receção da resposta,
    e para terminar a ligação
    """
    def __init__(self, address, port):
        """
        Inicializa a classe com parâmetros para funcionamento futuro.
        """
        self.sock=0
        self.adr=address
        self.port=port

    def connect(self):
        """
        Estabelece a ligação ao servidor especificado na inicialização do
        objeto.
        """
        self.sock=util.create_tcp_client_socket(self.adr,self.port)

    def send_receive(self,(data,datasize)):
        # type: (object) -> object
        """
        Envia os dados contidos em data para a socket da ligação, e retorna a
        resposta recebida pela mesma socket.
        :rtype: object
        """
        #Send a request to server
        self.sock.sendall(datasize)
        self.sock.sendall(data)

        #Get answer from server and interpret it
        sizebytes = self.sock.recv(4)
        size = util.size_unpack(sizebytes)
        message_recv = util.receive_all(self.sock, size)
        message = util.deserialize(message_recv)

        return message

        size = struct.unpack('!i',sizebytes)[0]
        recbytes = receive_all38(self.sock,size)
        rec = pickle.loads(recbytes)
        return rec

    def close(self):
        """
        Termina a ligação ao servidor.
        """
        self.sock.close()
