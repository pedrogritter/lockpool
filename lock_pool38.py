#!/usr/bin/python
# -*- coding: utf-8 -*-
"""

"""



# Zona para fazer importação

from threading import BoundedSemaphore
import time

###############################################################################
#Classe que serve para bloquear recursos
class resource_lock:
    def __init__(self, K):
        """
        Define e inicializa as características de um LOCK num recurso.
        """
        self.r_lock=BoundedSemaphore(K)
        self.k=K
        self.n_block=0
        self.client_info= {}

        
    def lock(self, client_id, time_limit):
        """
        Bloqueia o recurso se este não estiver bloqueado ou mantém o bloqueio
        se o recurso estiver bloqueado pelo cliente client_id. Neste caso renova
        o bloqueio do recurso até time_limit.
        Retorna True se bloqueou o recurso ou False caso contrário.
        """
        if(client_id in self.client_info.keys()):
            self.n_block+=1
            self.client_info[client_id]=time.time()+time_limit
            return True
        elif (self.r_lock.acquire(False)):
            self.n_block+=1
            self.client_info[client_id]=time.time()+time_limit
            return True
        else:
            return False
            
            
    def urelease(self):
        """
        Liberta o recurso incondicionalmente, alterando os valores associados
        ao bloqueio.
        """
        self.r_lock.release()

    def release(self, client_id):
        """
        Liberta o recurso se este foi bloqueado pelo cliente client_id,
        retornando True nesse caso. Caso contrário retorna False.
        """
        if(client_id in self.client_info.keys()):
            self.r_lock.release()
            self.client_info.pop(client_id)
            return True
        return False
    
    def test(self):
        """
        Retorna o estado de bloqueio do recurso.
        """
        if len(self.client_info)-self.k == 0:
            return True
        return False
    
    def stat(self):
        """
        Retorna o número de vezes que este recurso já foi bloqueado.
        """
        return self.n_block
    
    def stat_k(self):
        """
        Retorna o número de bloqueios em simultâneo em K.
        """
        return len(self.client_info)
    
###############################################################################

class lock_pool:
    def __init__(self, N, K):
        """
        Define um array com um conjunto de locks para N recursos. Os locks podem
        ser manipulados pelos métodos desta classe.
        """
        self.lock_list=[]
        for i in range(N):
            self.lock_list.append(resource_lock(K))
        
    def clear_expired_locks(self):
        """
        Verifica se os recursos que estão bloqueados ainda estão dentro do tempo
        de concessão do bloqueio. Liberta os recursos caso o seu tempo de
        concessão tenha expirado.
        """
        for lock in self.lock_list:
            for i in lock.client_info.keys():
                if time.time() > lock.client_info[i]:
                    lock.client_info.pop(i)
                    lock.urelease()

    def lock(self, client_id,resource_id, time_limit):
        """
        Tenta bloquear o recurso resource_id pelo cliente client_id, até ao
        instante time_limit. Retorna True em caso de sucesso e False caso
        contrário.
        """
        return self.lock_list[resource_id].lock(client_id, time_limit)

    def release(self, client_id,resource_id):
        """
        Tenta libertar o recurso resource_id pelo cliente client_id. Retorna
        True em caso de sucesso e False caso contrário.
        """
        return self.lock_list[resource_id].release(client_id)

    def test(self,resource_id):
        """
        Retorna True se o recurso resource_id estiver bloqueado e False caso
        contrário.
        """
        return self.lock_list[resource_id].test()

    def stat(self,resource_id):
        """
        Retorna o número de vezes que o recurso resource_id já foi bloqueado.
        """
        return self.lock_list[resource_id].stat()

    def stat_k(self, resource_id):
        """
        Retorna o número de bloqueiossimultâneosno recursoresource_id.
        """
        return self.lock_list[resource_id].stat_k()


    def __repr__(self):
        """
        Representação da classe para a saída standard. A string devolvida por
        esta função é usada, por exemplo, se uma instância da classe for
        passada à função print.
        """
        output = ""
        for i in range(len(self.lock_list)):
            l = self.lock_list[i].client_info
            if len(l)!=0:
                output+="recurso:"+str(i)+" bloqueado pelos clientes: "+str(map(lambda x:str(x)+" ate: "+time.ctime(l[x]),l))+"\n"
            else:
                output+="recurso:"+str(i)+" desbloqueado \n"
        return output

