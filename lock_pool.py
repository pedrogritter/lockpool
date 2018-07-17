#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Aplicaçoes distribuidas - Projeto 2 - lock_skeleton.py
Grupo: 22
Numeros de aluno: 44964, 46579
"""
# Zona para fazer imports

import socket as s
import sock_utils as util
import sys, time
from threading import BoundedSemaphore


#Lock_Resource class
class resource_lock:

    def __init__(self, K):
        """
        Define e inicializa as características de um LOCK num recurso.
        """

        self.is_blocked = 0  # resource status ( mudar nome de variavel )
        self.client_id = 0  # client id
        self.blocked_count = 0  # number times resource as been blocked
        self.block_limit = K  # number of times a resource can be blocked
        self.expiration = None  # expiration variable


    def lock(self, client_id, time_limit):
        """
        Bloqueia o recurso se este não estiver bloqueado ou inativo, ou mantém o bloqueio
        se o recurso estiver bloqueado pelo cliente client_id. Neste caso renova
        o bloqueio do recurso até time_limit.
        Retorna True se bloqueou o recurso ou False caso contrário.
        """
        # if self.blocked_count < self.block_limit:
        #     if not self.test():
        #         self.is_blocked = 1
        #         self.blocked_count += 1
        #         self.expiration = time.time() + time_limit
        #         self.client_id = client_id
        #         return True
        #
        #     elif self.is_blocked == 1 and self.client_id == client_id:
        #         self.expiration = time.time() + time_limit
        #         return True
        # else:
        #     return False
        state = self.test()
        if self.blocked_count < self.block_limit:
            if state == "UNLOCKED":
                self.is_blocked = 1
                self.client_id = client_id
                self.blocked_count += 1
                self.expiration = time.time() + time_limit

                return True

            elif state == "LOCKED" and self.client_id == int(client_id):
                # renova lock time
                self.blocked_count += 1
                self.expiration = time.time() + time_limit
                return True

            else:
                return False

        elif state == "DISABLED":
            return False

        else:
            self.is_blocked = 2
            return False

    def urelease(self):
        """
        Liberta o recurso incondicionalmente, alterando os valores associados
        ao bloqueio.
        """
        self.is_blocked = 0
        self.client_id = None
        self.expiration = 0

    def release(self, client_id):
        """
        Liberta o recurso se este foi bloqueado pelo cliente client_id,
        retornando True nesse caso. Caso contrário retorna False.
        """

        if self.client_id == client_id:
            self.is_blocked = 0
            return True
        else:
            return False

    def test(self):
        """
        Retorna o estado de bloqueio do recurso ou inativo, caso o recurso se
        encontre inativo.
        """

        if self.is_blocked == 0:
            return "UNLOCKED"
        elif self.is_blocked == 1:
            return "LOCKED"
        elif self.is_blocked == 2:
            return "DISABLED"

    def stat(self):
        """
        Retorna o número de vezes que este recurso já foi bloqueado em k.
        """
        return self.blocked_count

    def disable(self):
        """
        Coloca o recurso inativo/indisponível incondicionalmente, alterando os
        valores associados à sua disponibilidade.
        """

        self.is_blocked = 2

#################################################
                #Lock_pool Class
##################################################

class lock_pool:
    def __init__(self, N, K, Y, T):
        """
        Define um array com um conjunto de locks para N recursos. Os locks podem
        ser manipulados pelos métodos desta classe.
        Define K, o número máximo de bloqueios permitidos para cada recurso. Ao
        atingir K, o recurso fica indisponível/inativo.
        Define Y, o número máximo permitido de recursos bloqueados num dado
        momento. Ao atingir Y, não é possível realizar mais bloqueios até que um
        recurso seja libertado.
		Define T, o tempo máximo de concessão de bloqueio.
        """

        self.all_lockresources = [resource_lock(K) for x in xrange(N)]  # acabar
        self.all_lockR_number = N
        self.n_locked_PR = K  #
        self.n_locked_allowed = Y
        self.block_time = T
        self.blockednow = 0  # Number of locked resources
        self.disablednow = 0  # Number of disabled resources

    def clear_expired_locks(self):
        """
        Verifica se os recursos que estão bloqueados ainda estão dentro do tempo
        de concessão do bloqueio. Liberta os recursos caso o seu tempo de
        concessão tenha expirado.
        """
        for lr in self.all_lockresources:
            if lr.is_blocked:
                if lr.expiration <= time.time():
                    lr.urelease()

    def lock(self, resource_id, client_id, time_limit):
        """
        Tenta bloquear o recurso resource_id pelo cliente client_id, até ao
        instante time_limit.
        O bloqueio do recurso só é possível se o recurso estiver ativo, não
        bloqueado ou bloqueado para o próprio requerente, e Y ainda não foi
        excedido. É aconselhável implementar um método __try_lock__ para
        verificar estas condições.
        Retorna True em caso de sucesso e False caso contrário.
        """

        for i in range(self.all_lockR_number):
            if self.blockednow < self.n_locked_allowed:
                if resource_id <= self.all_lockR_number and resource_id > 0:
                    resource = self.all_lockresources[resource_id-1]
                    if resource.stat() < self.n_locked_PR:
                        self.blockednow += 1
                        return resource.lock(client_id,time_limit)
                    else:
                        #Limit lock for this resource reached
                        self.disablednow += 1
                        return resource.lock(client_id,time_limit)
                else:
                    #No resource with that id
                    return False
            else:
                #Limit of locked r at a given time reached
                return False

    def release(self, resource_id, client_id):
        """
        Liberta o bloqueio sobre o recurso resource_id pelo cliente client_id.
        True em caso de sucesso e False caso contrário.
        """

        if resource_id <= self.all_lockR_number and resource_id > 0:
            self.blockednow -= 1
            return self.all_lockresources[resource_id-1].release(client_id)
        else:
            False

    def test(self,resource_id):
        """
        Retorna True se o recurso resource_id estiver bloqueado e False caso
        esteja bloqueado ou inativo.
        """

        if resource_id <= self.all_lockR_number and resource_id > 0:
            if self.all_lockresources[resource_id-1].test() == "LOCKED":
                return True
            else:
                return False
        else:
            #self.disablednow += 1
            return False

    def stat(self,resource_id):
        """
        Retorna o número de vezes que o recurso resource_id já foi bloqueado, dos
        K bloqueios permitidos.
        """

        resource = self.all_lockresources[resource_id - 1]
        stat = resource.stat()
        return stat

    def stat_y(self):
        """
        Retorna o número de recursos bloqueados num dado momento do Y permitidos.
        """
        return self.blockednow

    def stat_n(self):
        """
        Retorna o número de recursos disponíneis em N.
        """
        return self.all_lockR_number - self.disablednow

    def __repr__(self):
        """
        Representação da classe para a saída standard. A string devolvida por
        esta função é usada, por exemplo, se uma instância da classe for
        passada à função print.
        """

        output = ""
        #
        # Acrescentar na output uma linha por cada recurso bloqueado, da forma:
        # recurso <número do recurso> bloqueado pelo cliente <id do cliente> até
        # <instante limite da concessão do bloqueio>
        #
        # Caso o recurso não esteja bloqueado a linha é simplesmente da forma:
        # recurso <número do recurso> desbloqueado
        # Caso o recurso não esteja inativo a linha é simplesmente da forma:
        # recurso <número do recurso> inativo
        #
        output = ""
        #
        # Acrescentar na output uma linha por cada recurso bloqueado, da forma:
        # recurso <número do recurso> bloqueado pelo cliente <id do cliente> até
        # <instante limite da concessão do bloqueio>
        #
        # Caso o recurso não esteja bloqueado a linha é simplesmente da forma:
        # recurso <número do recurso> desbloqueado
        #
        for item in range(self.all_lockR_number):
            lock = self.all_lockresources[item]
            test = lock.test()
            if test == "LOCKED":
                output += 'Recurso %s => LOCKED por: %s; Tempo limite: %s\n' % (
                item + 1, lock.client_id, time.ctime(lock.expiration))
            elif test == "DISABLED":
                output += 'Recurso %s => DISABLED\n' % (item + 1)

            else:
                output += 'Recurso %s => UNLOCKED\n' % (item + 1)
        return output