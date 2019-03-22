# -*- coding: utf-8 -*-
#import paramiko
from datetime import datetime
from shell import *

def get_vpn_users(host, username, key):
    comando = connect_ssh(host, username, key, 'sudo cat /etc/openvpn/openvpn-status.log')
    retorno = None
    if comando:
        try:
            comando = comando[3:]
            nova_lista=[]
            for i in comando:
                #Remover a quebra de linha    
                i = str(i)[:-1]
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

def logged_users(host, username, key):
    usuarios_logados = {}
    datetime_now = datetime.utcnow()
    dict_users = get_vpn_users(host, username, key)

    if dict_users:
        try:
            for key, value in dict_users.items():
                try:
                    datetime_object = datetime.strptime(value, '%a %b %d %H:%M:%S %Y')
                except:
                    datetime_object = datetime.utcnow()
                d3 = (datetime_now - datetime_object)
                if d3.seconds <= 300:
                    usuarios_logados[key] = value
                else:
                    print ('Nao esta logado {}'.format(key))
        except Exception as e:
            usuarios_logados = {'Erro conexao': str(e)}
    return (usuarios_logados)
        
        
def adicionar_user(host, username, key, user_add):
    comando = connect_ssh(host, username, key, 'cd /etc/openvpn/ && sudo /etc/openvpn/create_user.sh {}'.format(user_add))
    print (comando)
    if (comando):
        print ("Entrou no comando de adicionar usuario")
        content = ""
        comando = connect_ssh(host, username, key, 'sudo cat /etc/openvpn/user_configs/files/{}.ovpn'.format(user_add))
        for linha in comando:
            print (linha)
            content+=str(linha)
        return content
    else:
        return False
    
    
    
    
