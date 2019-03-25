# -*- coding: utf-8 -*-
#import paramiko
from datetime import datetime

from shell import connect_ssh

class Vpn:
    
    def __init__(self, host, username, key):
        self.host = host
        self.username = username
        self.key = key

    #def get_vpn_users(self, host, username, key):
    def get_vpn_users(self):
        comando = connect_ssh(self.host, self.username, self.key, 'sudo cat /etc/openvpn/openvpn-status.log')
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

    def logged_users(self):
        usuarios_logados = {}
        datetime_now = datetime.utcnow()
        dict_users = self.get_vpn_users()

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
            
            
    def adicionar_user(self, user_add):
        comando = connect_ssh(self.host, self.username, self.key, 'cd /etc/openvpn/ && sudo /etc/openvpn/create_user.sh {}'.format(user_add))
        print (comando)
        if (comando):
            print ("Entrou no comando de adicionar usuario")
            content = ""
            comando = connect_ssh(self.host, self.username, self.key, 'sudo cat /etc/openvpn/user_configs/files/{}.ovpn'.format(user_add))
            for linha in comando:
                print (linha)
                content+=str(linha)
            return content
        else:
            return False
        
        
    def remover_user(self, user_remove, pki_path):
        print (user_remove)
        pem_value = connect_ssh(self.host, self.username, self.key, "sudo ls {}/certs_by_serial/ | grep $(sudo cat {}/index.txt | grep -i '{}' | awk '{{print $3}}')".format(pki_path, pki_path, user_remove))
        if len(pem_value) > 0 and pem_value != None:
            commands = {'issued': 'crt', 'private' : 'key', 'reqs':'req'}
            pem_value = pem_value[0].strip('\n')

            for folder, vpn_file in commands.items():
                connect_ssh(self.host, self.username, self.key, 'sudo rm -f {}/{}/{}.{}'.format(pki_path, folder, user_remove, vpn_file))

            connect_ssh(self.host, self.username, self.key, "sudo rm -f {}/certs_by_serial/{} ".format(pki_path, pem_value))
            connect_ssh(self.host, self.username, self.key, 'sudo sed -i "/\\b\({}\)\\b/d" {}/index.txt'.format(user_remove, pki_path))
            
            #Remove specif user files configuration
            file_to_delete = { 'keys_REMOVE':'key', 'files':'ovpn', 'keys':'crt' }
            for folder, vpn_file in file_to_delete.items():
                folder = folder.replace("_REMOVE", "")
                print (folder, vpn_file)
                connect_ssh(self.host, self.username, self.key, 'sudo rm -f /etc/openvpn/user_configs/{}/{}.{}'.format(folder, user_remove, vpn_file))
            return True
        else:
            print ('Nao encontrei para deletar')
            return False
    
    def list_existing_users(self, pki_path):
        users = []
        comando = connect_ssh(self.host, self.username, self.key, "sudo cat {}/index.txt | awk '{{print $5}}' | cut -d '/' -f 7 | grep -v 'server'".format(pki_path))
        for usuarios in comando:
            usuarios = usuarios.strip('\n').replace("CN=", "")
            users.append(usuarios)
        return users