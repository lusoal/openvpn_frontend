# -*- coding: utf-8 -*-
import paramiko
from datetime import datetime

class Network():
    def __init__(self, host, user, key):
        self.host = host
        self.user = user
        self.key = key

    def connect_ssh(self, command):
        try:
            client = paramiko.client.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(self.host, username=self.user, key_filename=self.key, timeout=2)
            stdin, stdout, stderr = client.exec_command(command)
            stdout = stdout.readlines()
            client.close()
            return stdout
        except Exception as e:
            print ("Erro problema de conexao {}".format(e))
            return None

    def vpn_users(self):
        comando = self.connect_ssh('sudo cat /etc/openvpn/openvpn-status.log')
        retorno = None
        print (comando)
        if comando:
            try:
                comando = comando[3:]
                print (comando)
                nova_lista=[]
                for i in comando:
                    print (i)
                    i = str(i)[:-1]
                    print (i)
                    nova_lista.append(i)
    
                dict_usuarios = {}
                for vpn_info in nova_lista:
                    if '10' in vpn_info:
                        user_info = str(vpn_info).split(',')[1]
                        time_info = str(vpn_info).split(',')[3]
                        dict_usuarios[user_info] = time_info
                retorno = dict_usuarios
            except:
                retorno = None    
        return retorno
    
    def logged_users(self):
        usuarios_logados = {}
        datetime_now = datetime.utcnow()
        dict_users = self.vpn_users()
        print (dict_users)
        if dict_users:
            try:
                for key, value in dict_users.items():
                    try:
                        datetime_object = datetime.strptime(value, '%a %b %d %H:%M:%S %Y')
                    except:
                        datetime_object = datetime.utcnow()
                    d3 = (datetime_now - datetime_object)
                    print (key, d3.seconds)
                    if d3.seconds <= 300:
                        usuarios_logados[key] = value
                    else:
                        print ('Nao esta logado {}'.format(key))
            except Exception as e:
                usuarios_logados = {'Erro conexao': str(e)}
        
        return (usuarios_logados)


            


            
        
        
        

        
        